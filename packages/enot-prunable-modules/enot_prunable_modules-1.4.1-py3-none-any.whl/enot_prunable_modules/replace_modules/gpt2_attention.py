# pylint: disable=ungrouped-imports
from argparse import Namespace
from typing import Optional
from typing import Tuple
from typing import Union

import torch
from packaging import version
from torch import nn
from torch.cuda.amp.autocast_mode import autocast
from transformers import Conv1D
from transformers.models.gpt2.modeling_gpt2 import GPT2Attention
from transformers.pytorch_utils import find_pruneable_heads_and_indices
from transformers.pytorch_utils import prune_conv1d_layer

from enot_prunable_modules.replace_modules.replacer import Replacer

IS_AMP_AVAILABLE = version.parse(torch.__version__) >= version.parse("1.6")

__all__ = [
    "PrunableGPT2Attention",
    "GPT2AttentionReplacer",
]


class PrunableGPT2Attention(nn.Module):
    """Prunable version of GPT2Attention from transformers package."""

    bias: torch.Tensor
    masked_bias: torch.Tensor

    def __init__(
        self,
        config: Namespace,
        is_cross_attention: bool = False,
        layer_idx: Optional[int] = None,
    ):
        """Add `self.double_split_size`."""
        super().__init__()

        max_positions = config.max_position_embeddings
        self.register_buffer(
            "bias",
            torch.tril(torch.ones((max_positions, max_positions), dtype=torch.uint8)).view(
                1, 1, max_positions, max_positions
            ),
        )
        self.register_buffer("masked_bias", torch.tensor(-1e4))

        self.embed_dim = config.hidden_size
        self.num_heads = config.num_attention_heads
        self.head_dim = self.embed_dim // self.num_heads
        self.split_size = self.embed_dim
        # Modification: added `self.double_split_size`.
        self.double_split_size = self.embed_dim * 2
        if self.head_dim * self.num_heads != self.embed_dim:
            raise ValueError(
                f'"embed_dim" must be divisible by "num_heads" (got "embed_dim": {self.embed_dim} and "num_heads":'
                f" {self.num_heads})."
            )

        self.scale_attn_weights = config.scale_attn_weights
        self.is_cross_attention = is_cross_attention

        # Layer-wise attention scaling, reordering, and upcasting
        self.scale_attn_by_inverse_layer_idx = config.scale_attn_by_inverse_layer_idx
        self.layer_idx = layer_idx
        self.reorder_and_upcast_attn = config.reorder_and_upcast_attn

        if self.is_cross_attention:
            self.c_attn = Conv1D(2 * self.embed_dim, self.embed_dim)
            self.q_attn = Conv1D(self.embed_dim, self.embed_dim)
        else:
            self.c_attn = Conv1D(3 * self.embed_dim, self.embed_dim)
        self.c_proj = Conv1D(self.embed_dim, self.embed_dim)

        self.attn_dropout = nn.Dropout(config.attn_pdrop)
        self.resid_dropout = nn.Dropout(config.resid_pdrop)

        self.pruned_heads = set()

    def prune_heads(self, heads):
        """No changes."""
        if len(heads) == 0:
            return
        heads, index = find_pruneable_heads_and_indices(heads, self.num_heads, self.head_dim, self.pruned_heads)
        index_attn = torch.cat([index, index + self.split_size, index + (2 * self.split_size)])

        # Prune conv1d layers
        self.c_attn = prune_conv1d_layer(self.c_attn, index_attn, dim=1)
        self.c_proj = prune_conv1d_layer(self.c_proj, index, dim=0)

        # Update hyper params
        self.split_size = (self.split_size // self.num_heads) * (self.num_heads - len(heads))
        self.num_heads = self.num_heads - len(heads)
        self.pruned_heads = self.pruned_heads.union(heads)

    def _attn(self, query, key, value, attention_mask=None, head_mask=None):
        """No changes."""
        attn_weights = torch.matmul(query, key.transpose(-1, -2))

        if self.scale_attn_weights:
            attn_weights = attn_weights / torch.tensor(
                value.size(-1) ** 0.5, dtype=attn_weights.dtype, device=attn_weights.device
            )

        # Layer-wise attention scaling
        if self.scale_attn_by_inverse_layer_idx:
            attn_weights = attn_weights / float(self.layer_idx + 1)  # type: ignore

        if not self.is_cross_attention:
            # if only "normal" attention layer implements causal mask
            query_length, key_length = query.size(-2), key.size(-2)
            causal_mask = self.bias[:, :, key_length - query_length : key_length, :key_length].to(torch.bool)
            mask_value = torch.finfo(attn_weights.dtype).min
            # Need to be a tensor, otherwise we get error: `RuntimeError: expected scalar type float but found double`.
            # Need to be on the same device, otherwise `RuntimeError: ..., x and y to be on the same device`
            mask_value = torch.tensor(mask_value, dtype=attn_weights.dtype).to(attn_weights.device)
            attn_weights = torch.where(causal_mask, attn_weights, mask_value)

        if attention_mask is not None:
            # Apply the attention mask
            attn_weights = attn_weights + attention_mask

        attn_weights = nn.functional.softmax(attn_weights, dim=-1)

        # Downcast (if necessary) back to V's dtype (if in mixed-precision) -- No-Op otherwise
        attn_weights = attn_weights.type(value.dtype)
        attn_weights = self.attn_dropout(attn_weights)

        # Mask heads if we want to
        if head_mask is not None:
            attn_weights = attn_weights * head_mask

        attn_output = torch.matmul(attn_weights, value)

        return attn_output, attn_weights

    def _upcast_and_reordered_attn(self, query, key, value, attention_mask=None, head_mask=None):
        """No changes."""
        # Use `torch.baddbmm` (a bit more efficient w/ alpha param for scaling -- from Megatron-LM)
        bsz, num_heads, q_seq_len, channels = query.size()
        _, _, k_seq_len, _ = key.size()

        # Preallocate attn_weights for `baddbmm`
        attn_weights = torch.empty(bsz * num_heads, q_seq_len, k_seq_len, dtype=torch.float32, device=query.device)

        # Compute Scale Factor
        scale_factor = 1.0
        if self.scale_attn_weights:
            scale_factor /= float(value.size(-1)) ** 0.5

        if self.scale_attn_by_inverse_layer_idx:
            scale_factor /= float(self.layer_idx + 1)  # type: ignore

        # Upcast (turn off autocast) and reorder (Scale K by 1 / root(channels))
        if IS_AMP_AVAILABLE:
            with autocast(enabled=False):
                query, key = query.reshape(-1, q_seq_len, channels), key.transpose(-1, -2).reshape(
                    -1, channels, k_seq_len
                )
                attn_weights = torch.baddbmm(attn_weights, query.float(), key.float(), beta=0, alpha=scale_factor)
                attn_weights = attn_weights.reshape(bsz, num_heads, q_seq_len, k_seq_len)
        else:
            query, key = query.reshape(-1, q_seq_len, channels), key.transpose(-1, -2).reshape(-1, channels, k_seq_len)
            attn_weights = torch.baddbmm(attn_weights, query.float(), key.float(), beta=0, alpha=scale_factor)
            attn_weights = attn_weights.reshape(bsz, num_heads, q_seq_len, k_seq_len)

        if not self.is_cross_attention:
            # if only "normal" attention layer implements causal mask
            query_length, key_length = query.size(-2), key.size(-2)
            causal_mask = self.bias[:, :, key_length - query_length : key_length, :key_length].bool()
            mask_value = torch.finfo(attn_weights.dtype).min
            # Need to be a tensor, otherwise we get error: `RuntimeError: expected scalar type float but found double`.
            # Need to be on the same device, otherwise `RuntimeError: ..., x and y to be on the same device`
            mask_value = torch.tensor(mask_value, dtype=attn_weights.dtype).to(attn_weights.device)
            attn_weights = torch.where(causal_mask, attn_weights, mask_value)

        if attention_mask is not None:
            # Apply the attention mask
            attn_weights = attn_weights + attention_mask

        attn_weights = nn.functional.softmax(attn_weights, dim=-1)

        # Downcast (if necessary) back to V's dtype (if in mixed-precision) -- No-Op if otherwise
        if attn_weights.dtype != torch.float32:
            raise ValueError('Error with upcasting, "attn_weights" does not have dtype torch.float32')
        attn_weights = attn_weights.type(value.dtype)
        attn_weights = self.attn_dropout(attn_weights)

        # Mask heads if we want to
        if head_mask is not None:
            attn_weights = attn_weights * head_mask

        attn_output = torch.matmul(attn_weights, value)

        return attn_output, attn_weights

    def _split_heads(self, tensor, num_heads, attn_head_size):
        """Split hidden_size dim into attn_head_size and num_heads."""
        del attn_head_size
        new_shape = tensor.size()[:-1] + (num_heads, -1)
        tensor = tensor.view(new_shape)
        return tensor.permute(0, 2, 1, 3)  # (batch, head, seq_length, head_features)

    def _merge_heads(self, tensor, num_heads, attn_head_size):
        """Merge attn_head_size dim and num_attn_heads dim into hidden_size."""
        del attn_head_size, num_heads
        tensor = tensor.permute(0, 2, 1, 3).contiguous()
        new_shape = tensor.size()[:-2] + (-1,)
        return tensor.view(new_shape)

    def forward(
        self,
        hidden_states: Optional[torch.Tensor],
        layer_past: Optional[Tuple[torch.Tensor]] = None,
        attention_mask: Optional[torch.FloatTensor] = None,
        head_mask: Optional[torch.FloatTensor] = None,
        encoder_hidden_states: Optional[torch.Tensor] = None,
        encoder_attention_mask: Optional[torch.FloatTensor] = None,
        use_cache: Optional[bool] = False,
        output_attentions: Optional[bool] = False,
    ) -> Tuple[Union[torch.Tensor, Tuple[torch.Tensor]], ...]:
        """Replace split with slice."""
        if encoder_hidden_states is not None:
            if not hasattr(self, "q_attn"):
                raise ValueError(
                    'If class is used as cross attention, the weights "q_attn" have to be defined. '
                    'Please make sure to instantiate class with "GPT2Attention(..., is_cross_attention=True)".'
                )

            query = self.q_attn(hidden_states)
            # Modification: replace split with slicing. Use slices with values directly from self
            # to help integer tracing.
            key_value = self.c_attn(encoder_hidden_states)
            key = key_value[:, :, : self.split_size]
            value = key_value[:, :, self.split_size :]
            attention_mask = encoder_attention_mask
        else:
            # Modification: replace split with slicing. Use slices with values directly from self
            # to help integer tracing.
            query_key_value = self.c_attn(hidden_states)
            query = query_key_value[:, :, : self.split_size]
            key = query_key_value[:, :, self.split_size : self.double_split_size]
            value = query_key_value[:, :, self.double_split_size :]

        query = self._split_heads(query, self.num_heads, self.head_dim)
        key = self._split_heads(key, self.num_heads, self.head_dim)
        value = self._split_heads(value, self.num_heads, self.head_dim)

        if layer_past is not None:
            past_key, past_value = layer_past  # type: ignore
            key = torch.cat((past_key, key), dim=-2)
            value = torch.cat((past_value, value), dim=-2)

        if use_cache is True:
            present = (key, value)
        else:
            present = None

        if self.reorder_and_upcast_attn:
            attn_output, attn_weights = self._upcast_and_reordered_attn(query, key, value, attention_mask, head_mask)
        else:
            attn_output, attn_weights = self._attn(query, key, value, attention_mask, head_mask)

        attn_output = self._merge_heads(attn_output, self.num_heads, self.head_dim)
        attn_output = self.c_proj(attn_output)
        attn_output = self.resid_dropout(attn_output)

        outputs = (attn_output, present)
        if output_attentions:
            outputs += (attn_weights,)

        return outputs  # a, present, (attentions)


class GPT2AttentionReplacer(Replacer):
    """GPT2Attention module replacer."""

    def replace(self, module: GPT2Attention) -> PrunableGPT2Attention:
        """Replace GPT2Attention module inplace with its prunable version."""
        config = Namespace()
        config.max_position_embeddings = module.bias.shape[-1]
        config.hidden_size = module.embed_dim
        config.num_attention_heads = module.num_heads
        config.scale_attn_weights = module.scale_attn_weights
        config.scale_attn_by_inverse_layer_idx = module.scale_attn_by_inverse_layer_idx
        config.reorder_and_upcast_attn = module.reorder_and_upcast_attn
        config.attn_pdrop = module.attn_dropout.p
        config.resid_pdrop = module.resid_dropout.p

        attn = PrunableGPT2Attention(
            config=config,
            is_cross_attention=module.is_cross_attention,
            layer_idx=module.layer_idx,
        )

        # Substitute attn weights with original weights.
        attn.bias = module.bias
        attn.masked_bias = module.masked_bias

        if module.is_cross_attention:
            attn.c_attn = module.c_attn
            attn.q_attn = module.q_attn
        else:
            attn.c_attn = module.c_attn

        attn.c_proj = module.c_proj

        if module.training:
            attn.train()
        else:
            attn.eval()

        return attn

    def revert(self, module: PrunableGPT2Attention) -> GPT2Attention:
        """Revert prunable version to original one."""
        config = Namespace()
        config.max_position_embeddings = module.bias.shape[-1]
        config.hidden_size = module.embed_dim
        config.num_attention_heads = module.num_heads
        config.scale_attn_weights = module.scale_attn_weights
        config.scale_attn_by_inverse_layer_idx = module.scale_attn_by_inverse_layer_idx
        config.reorder_and_upcast_attn = module.reorder_and_upcast_attn
        config.attn_pdrop = module.attn_dropout.p
        config.resid_pdrop = module.resid_dropout.p

        attn = GPT2Attention(
            config=config,
            is_cross_attention=module.is_cross_attention,
            layer_idx=module.layer_idx,
        )

        # Substitute attn weights with original weights.
        attn.bias = module.bias
        attn.masked_bias = module.masked_bias

        if module.is_cross_attention:
            attn.c_attn = module.c_attn
            attn.q_attn = module.q_attn
        else:
            attn.c_attn = module.c_attn

        attn.c_proj = module.c_proj

        if module.training:
            attn.train()
        else:
            attn.eval()

        return attn
