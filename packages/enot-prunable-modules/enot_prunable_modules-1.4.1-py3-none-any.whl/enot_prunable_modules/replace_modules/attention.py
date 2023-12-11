import types
import typing
import warnings

import torch
from diffusers.models.attention_processor import Attention
from diffusers.models.attention_processor import AttnAddedKVProcessor
from diffusers.models.attention_processor import AttnAddedKVProcessor2_0
from diffusers.models.attention_processor import AttnProcessor
from diffusers.models.attention_processor import AttnProcessor2_0
from torch import nn

from enot_prunable_modules.replace_modules.replacer import Replacer

__all__ = [
    "PrunableAttention",
    "AttentionReplacer",
]


class PrunableAttention(Attention):
    """diffusers.models.attention_processor.Attention."""

    def batch_to_head_dim(self, tensor):
        """Fix reshape with accessing to channels instead of self.channels."""
        batch_size, seq_len, _ = tensor.shape
        tensor = tensor.reshape(batch_size // self.heads, self.heads, seq_len, self.enot_dim)
        tensor = tensor.permute(0, 2, 1, 3).flatten(start_dim=2)
        return tensor

    def head_to_batch_dim(self, tensor, out_dim=3):
        """Fix reshape with accessing to channels instead of self.channels."""
        batch_size, seq_len, _ = tensor.shape

        # head_to_batch_dim applies after different linear layers, so last shape can be different
        tensor = tensor.reshape(batch_size, seq_len, self.heads, -1)
        tensor = tensor.permute(0, 2, 1, 3)

        if out_dim == 3:
            tensor = tensor.reshape(batch_size * self.heads, seq_len, -1)

        return tensor

    def get_attention_scores(self, query, key, attention_mask=None):
        """Fix tensor creation in forward pass."""
        dtype = query.dtype
        if self.upcast_attention:
            query = query.float()
            key = key.float()

        if attention_mask is None:
            attention_scores = self.scale * (query @ key.transpose(-1, -2))
        else:
            attention_scores = attention_mask + self.scale * (query @ key.transpose(-1, -2))

        if self.upcast_softmax:
            attention_scores = attention_scores.float()

        attention_probs = attention_scores.softmax(dim=-1)
        del attention_scores

        attention_probs = attention_probs.to(dtype)

        return attention_probs


class PrunableAttnProcessor:
    """diffusers.models.attention_processor.AttnProcessor."""

    def __call__(
        self,
        attn: Attention,
        hidden_states,
        encoder_hidden_states=None,
        attention_mask=None,
        temb=None,
        scale=1.0,
    ):
        """Fix reshape with accessing to channels instead of self.channels."""
        residual = hidden_states

        if attn.spatial_norm is not None:
            hidden_states = attn.spatial_norm(hidden_states, temb)

        input_ndim = hidden_states.ndim

        if input_ndim == 4:
            batch_size, _, height, width = hidden_states.shape
            hidden_states = hidden_states.view(batch_size, attn.enot_inner_dim, height * width).transpose(1, 2)

        batch_size, sequence_length, _ = (
            hidden_states.shape if encoder_hidden_states is None else encoder_hidden_states.shape
        )
        attention_mask = attn.prepare_attention_mask(attention_mask, sequence_length, batch_size)

        if attn.group_norm is not None:
            hidden_states = attn.group_norm(hidden_states.transpose(1, 2)).transpose(1, 2)

        query = attn.to_q(hidden_states, scale=scale)

        if encoder_hidden_states is None:
            encoder_hidden_states = hidden_states
        elif attn.norm_cross:
            encoder_hidden_states = attn.norm_encoder_hidden_states(encoder_hidden_states)

        key = attn.to_k(encoder_hidden_states, scale=scale)
        value = attn.to_v(encoder_hidden_states, scale=scale)

        query = attn.head_to_batch_dim(query)
        key = attn.head_to_batch_dim(key)
        value = attn.head_to_batch_dim(value)

        attention_probs = attn.get_attention_scores(query, key, attention_mask)
        hidden_states = torch.bmm(attention_probs, value)
        hidden_states = attn.batch_to_head_dim(hidden_states)

        # linear proj
        hidden_states = attn.to_out[0](hidden_states, scale=scale)
        # dropout
        hidden_states = attn.to_out[1](hidden_states)

        if input_ndim == 4:
            hidden_states = hidden_states.transpose(-1, -2).reshape(batch_size, attn.enot_inner_dim, height, width)

        if attn.residual_connection:
            hidden_states = hidden_states + residual

        hidden_states = hidden_states / attn.rescale_output_factor

        return hidden_states


class PrunableAttnAddedKVProcessor:
    """diffusers.models.attention_processor.AttnAddedKVProcessor."""

    def __call__(self, attn, hidden_states, encoder_hidden_states=None, attention_mask=None):
        """Fix reshape with accessing to channels instead of self.channels."""
        residual = hidden_states
        spatial = residual.shape[2:]
        channels = attn.enot_inner_dim
        hidden_states = hidden_states.view(hidden_states.shape[0], channels, -1).transpose(1, 2)
        batch_size, sequence_length, _ = hidden_states.shape

        attention_mask = attn.prepare_attention_mask(attention_mask, sequence_length, batch_size)

        if encoder_hidden_states is None:
            encoder_hidden_states = hidden_states
        elif attn.norm_cross:
            encoder_hidden_states = attn.norm_encoder_hidden_states(encoder_hidden_states)

        hidden_states = attn.group_norm(hidden_states.transpose(1, 2)).transpose(1, 2)

        query = attn.to_q(hidden_states)
        query = attn.head_to_batch_dim(query)

        encoder_hidden_states_key_proj = attn.add_k_proj(encoder_hidden_states)
        encoder_hidden_states_value_proj = attn.add_v_proj(encoder_hidden_states)
        encoder_hidden_states_key_proj = attn.head_to_batch_dim(encoder_hidden_states_key_proj)
        encoder_hidden_states_value_proj = attn.head_to_batch_dim(encoder_hidden_states_value_proj)

        if not attn.only_cross_attention:
            key = attn.to_k(hidden_states)
            value = attn.to_v(hidden_states)
            key = attn.head_to_batch_dim(key)
            value = attn.head_to_batch_dim(value)
            key = torch.cat([encoder_hidden_states_key_proj, key], dim=1)
            value = torch.cat([encoder_hidden_states_value_proj, value], dim=1)
        else:
            key = encoder_hidden_states_key_proj
            value = encoder_hidden_states_value_proj

        attention_probs = attn.get_attention_scores(query, key, attention_mask)
        hidden_states = torch.bmm(attention_probs, value)
        hidden_states = attn.batch_to_head_dim(hidden_states)

        # linear proj
        hidden_states = attn.to_out[0](hidden_states)
        # dropout
        hidden_states = attn.to_out[1](hidden_states)

        hidden_states = hidden_states.transpose(-1, -2).reshape(batch_size, channels, *spatial)
        hidden_states = hidden_states + residual

        return hidden_states


class AttentionReplacer(Replacer):
    """Attention module replacer."""

    def replace(self, module: Attention) -> None:
        """Replace Attention module inplace with its prunable version."""
        module.__class__ = PrunableAttention

        assert isinstance(module.to_q, nn.Linear)
        setattr(module, "enot_inner_dim", module.to_q.out_features)
        setattr(module, "enot_dim", module.to_q.out_features // typing.cast(int, module.heads))

        setattr(module, "batch_to_head_dim", types.MethodType(PrunableAttention.batch_to_head_dim, module))
        setattr(module, "head_to_batch_dim", types.MethodType(PrunableAttention.head_to_batch_dim, module))
        setattr(module, "get_attention_scores", types.MethodType(PrunableAttention.get_attention_scores, module))

        setattr(module, "enot_prev_processor", module.processor)
        if isinstance(module.processor, (AttnAddedKVProcessor, AttnAddedKVProcessor2_0)):
            setattr(module, "processor", PrunableAttnAddedKVProcessor())
        elif isinstance(module.processor, (AttnProcessor, AttnProcessor2_0)):
            setattr(module, "processor", PrunableAttnProcessor())
        else:
            warnings.warn(f"Prunable module is not implemented for {module.processor}, it might be unprunable!")

    def revert(self, module: PrunableAttention) -> None:
        """Revert Attention module replacing."""
        module.__class__ = Attention
        setattr(module, "batch_to_head_dim", types.MethodType(Attention.batch_to_head_dim, module))
        setattr(module, "head_to_batch_dim", types.MethodType(Attention.head_to_batch_dim, module))
        setattr(module, "get_attention_scores", types.MethodType(Attention.get_attention_scores, module))

        delattr(module, "enot_inner_dim")
        delattr(module, "enot_dim")

        setattr(module, "processor", module.enot_prev_processor)
        delattr(module, "enot_prev_processor")
