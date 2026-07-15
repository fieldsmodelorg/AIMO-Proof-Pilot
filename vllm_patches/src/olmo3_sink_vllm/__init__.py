"""vLLM registration for Proof Pilot OLMo3Sink checkpoints."""

from __future__ import annotations

_REGISTERED = False


def register() -> None:
    """Register the OLMo3Sink target model in every vLLM process."""
    global _REGISTERED
    if _REGISTERED:
        return

    from vllm import ModelRegistry

    ModelRegistry.register_model(
        "Olmo3SinkForCausalLM",
        "olmo3_sink_vllm.model:Olmo3SinkForCausalLM",
    )
    ModelRegistry.register_model(
        "Olmo3SinkDFlashForCausalLM",
        "olmo3_sink_vllm.dflash:Olmo3SinkDFlashForCausalLM",
    )
    # Existing Proof Pilot drafts use this generic architecture name. Replace
    # vLLM's Qwen3 implementation with the trained OLMo3 post-norm/sink model.
    ModelRegistry.register_model(
        "DFlashDraftModel",
        "olmo3_sink_vllm.dflash:Olmo3SinkDFlashForCausalLM",
    )
    _REGISTERED = True


__all__ = ["register"]
