# OLMo3Sink vLLM Plugin

This directory provides the target and DFlash draft model support required to
serve Proof Pilot OLMo3Sink checkpoints with vLLM.

## Behavior

- Registers `Olmo3SinkForCausalLM` through vLLM's `vllm.general_plugins`
  entry-point group. vLLM loads this plugin in the API, engine-core, and worker
  processes.
- Registers `Olmo3SinkDFlashForCausalLM` and redirects the existing
  `DFlashDraftModel` checkpoint architecture to it. This replaces vLLM's stock
  Qwen3 draft with the trained OLMo3 post-norm architecture.
- Passes each layer's trained per-query-head sink logits to vLLM's sink-aware
  attention backend.
- Preserves OLMo3 hybrid sliding-window attention and applies YaRN only to
  full-attention layers.
- Exposes the target hidden states selected by
  `dflash_config.target_layer_ids` through vLLM's Eagle3 interface.
- Preserves the draft's full-projection Q/K RMSNorm, learned `mask_embed`,
  512-token all-layer sliding attention, post-attention/post-MLP norms, and
  native vLLM DFlash context-KV materialization.
- Shares the target embedding and LM head because the Proof Pilot draft
  checkpoint intentionally contains neither tensor.
- Shards the checkpoint's full sink vector by tensor-parallel rank.
- Fails model loading when a local layer is missing its sink tensor or a sink
  tensor has the wrong number of heads.
- Adds `disable_above_context_len` to `--speculative-config` on vLLM `0.25.1`.
  When the largest request in a batch reaches the threshold, the V1 runner skips
  the drafter, clears pending draft tokens, and continues target-only decoding.

The target implementation supports vLLM `0.23.1rc1.dev699` through `0.25.1`.
The DFlash implementation and context cutoff target vLLM `0.25.1` V1. The CUDA
attention backend must support sinks; on H200, vLLM's FlashAttention 3 backend
provides this support.

## Install

Install into the same Python environment that owns the `vllm` executable:

```bash
bash vllm_patches/install.sh /path/to/venv
```

The script installs the local plugin without resolving dependencies, then
starts a fresh Python process to verify model registration and importability.
On vLLM `0.25.1`, it applies and verifies the context-cutoff patch before
installing the plugin. The patcher is idempotent and keeps one
`*.pre_dflash_context_cutoff` backup beside each modified vLLM source file.

Set `AIMO_VLLM_APPLY_DFLASH_CONTEXT_CUTOFF=0` to install only the model plugin.
Other vLLM versions keep the plugin behavior and skip this versioned source
patch.

To install with an explicit interpreter instead:

```bash
bash vllm_patches/install.sh /path/to/python
```

## Serve

`VLLM_PLUGINS` is optional when no plugin allowlist is configured. Setting it
explicitly makes the deployment deterministic:

```bash
VLLM_PLUGINS=olmo3_sink vllm serve /path/to/opd-32b-deploy \
  --trust-remote-code \
  --tensor-parallel-size 1 \
  --kv-cache-dtype fp8 \
  --block-size 256 \
  --reasoning-parser deepseek_v4
```

Do not rename the checkpoint architecture to `Olmo3ForCausalLM`. The stock
model has no sink parameters and would silently change every attention
distribution.

## OLMo3Sink DFlash

The trained draft has block size 11: one anchor plus 10 mask-token proposals.
Use `num_speculative_tokens=10` to match that checkpoint:

```bash
VLLM_USE_V2_MODEL_RUNNER=0 \
VLLM_PLUGINS=olmo3_sink \
vllm serve /path/to/opd-model \
  --trust-remote-code \
  --speculative-config '{
    "method": "dflash",
    "model": "/path/to/dflash-32b-draft-v2test-phaseL",
    "num_speculative_tokens": 10,
    "disable_above_context_len": 81920
  }'
```

The draft checkpoint can retain `"architectures": ["DFlashDraftModel"]`.
When this plugin is active, the installer verifies that name resolves to
`Olmo3SinkDFlashForCausalLM`, not vLLM's generic Qwen3 implementation.

## DFlash context cutoff

This repository starts vLLM with `VLLM_USE_V2_MODEL_RUNNER=0`, so the patch is
deliberately limited to the V1 runner. Configure an 80K cutoff as follows:

```bash
VLLM_USE_V2_MODEL_RUNNER=0 vllm serve /path/to/opd-model \
  --speculative-config '{
    "method": "dflash",
    "model": "/path/to/dflash-model",
    "num_speculative_tokens": 10,
    "disable_above_context_len": 81920
  }'
```

The comparison is inclusive: a batch with maximum context length `81920` or
larger runs target-only. Shorter requests in the same batch also stop drafting
until they are scheduled in a batch whose maximum context is below the cutoff.
The scheduler sets the proposal width to zero, so this remains coordinated when
`evaluation/harness_vllm/run.py` enables `--async-scheduling`. The worker retains vLLM's native K-wide
zero buffer while clearing valid drafts; that buffer is required when a mixed
batch moves from target-only decoding back to DFlash. This is a deterministic
context policy, not a live acceptance-rate controller.

To apply only this patch to an existing vLLM `0.25.1` environment:

```bash
python vllm_patches/patch_dflash_context_cutoff.py /path/to/venv
```
