import types

from diffusers.models.attention import GEGLU

from enot_prunable_modules.replace_modules.replacer import Replacer

__all__ = [
    "PrunableGEGLU",
    "GEGLUReplacer",
]


class PrunableGEGLU(GEGLU):
    """diffusers.models.atttention.GEGLU."""

    def forward(self, hidden_states, scale: float = 1.0):
        """Replace chunk with reshape."""
        feedforward = self.proj(hidden_states, scale)
        batch, seq_length, _ = feedforward.shape
        chunk = feedforward.reshape(batch, seq_length, 2, -1)
        hidden_states, gate = chunk[..., 0, :], chunk[..., 1, :]
        return hidden_states * self.gelu(gate)


class GEGLUReplacer(Replacer):
    """GEGLU module replacer."""

    def replace(self, module: GEGLU) -> None:
        """Replace GEGLU module inplace with its prunable version."""
        module.forward = types.MethodType(PrunableGEGLU.forward, module)
        module.__class__ = PrunableGEGLU

    def revert(self, module: PrunableGEGLU) -> None:
        """Revert GEGLU module replacing."""
        module.forward = types.MethodType(GEGLU.forward, module)
        module.__class__ = GEGLU
