#!/bin/bash
# apply_patches.sh — apply the Olmo3Sink model + perf patches to the
# proof-pilot-env sglang venv (idempotent; originals backed up as *.orig).
#
# Patches (source in this dir -> target inside the venv's sglang/srt):
#   olmo2_sink_dflash.py        -> models/olmo2.py          REQUIRED: Olmo3Sink
#       target model — attention sinks computed in-kernel
#   dflash_sink.py              -> models/dflash.py         DFlash draft model
#       (speculative decoding; inert unless a draft model is served)
#   dflash_worker_v2_ring.py    -> speculative/dflash_worker_v2.py
#   fused_kv_materialize_fullnorm.py -> speculative/triton_ops/fused_kv_materialize.py
#   dflash_info_v2_swa_evict.py -> speculative/dflash_info_v2.py
#   patch_speculative_finish.py (script) earliest-stop handling and committed
#       KV-tail trimming for multi-token DFlash verify results
#   patch_canonical_greedy.py    canonical greedy near-tie resolution
#   patch_dflash_sampling.py    (script) reject unsupported probability
#       transforms and keep sampling uniforms off zero-probability boundaries
#   patch_w4a8_runtime_marker.py (script) log every successfully constructed
#       target Humming W4A8 layer and every W4A16 draft layer
#   patch_humming_target_scope.py (script) prevent the global target Humming
#       hook from converting the INT4 DFlash draft from W4A16 to W4A8
#   patch_humming_sm90_config.py (script) pin the H200 Humming helper to the
#       numerically verified M=256 kernel configuration for every row count
#
# Usage: bash apply_patches.sh <venv_path>
set -euo pipefail

VENV="${1:?usage: apply_patches.sh <venv_path>}"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SROOT="$(echo "$VENV"/lib/python*/site-packages/sglang/srt | awk '{print $1}')"
[ -d "$SROOT" ] || { echo "ERROR: sglang/srt not found under $VENV"; exit 1; }
echo "[patch] sglang srt=$SROOT"

PATCHES=(
  "olmo2_sink_dflash.py|models/olmo2.py"
  "dflash_sink.py|models/dflash.py"
  "dflash_worker_v2_ring.py|speculative/dflash_worker_v2.py"
  "fused_kv_materialize_fullnorm.py|speculative/triton_ops/fused_kv_materialize.py"
  "dflash_info_v2_swa_evict.py|speculative/dflash_info_v2.py"
)
for p in "${PATCHES[@]}"; do
  IFS='|' read -r s d <<< "$p"
  [ -f "$SROOT/$d" ] || { echo "  skip (not in this sglang): $d"; continue; }
  [ -f "$SROOT/$d.orig" ] || cp "$SROOT/$d" "$SROOT/$d.orig"
  cp "$SRC/$s" "$SROOT/$d"
  echo "  patched: $d"
done
find "$SROOT/models" "$SROOT/speculative" -name '*.pyc' -delete 2>/dev/null || true

"$VENV/bin/python" "$SRC/patch_canonical_greedy.py" "$VENV"
"$VENV/bin/python" "$SRC/patch_dflash_sampling.py" "$VENV"
"$VENV/bin/python" "$SRC/patch_speculative_finish.py" "$VENV"
"$VENV/bin/python" "$SRC/patch_w4a8_runtime_marker.py" "$VENV"
"$VENV/bin/python" "$SRC/patch_humming_target_scope.py" \
  /workspace/pp/proof-pilot/deploy/w4a8/humming_w4a8.py
"$VENV/bin/python" "$SRC/patch_humming_sm90_config.py" \
  /workspace/pp/proof-pilot/deploy/w4a8/humming_w4a8.py
echo "[patch] done"
