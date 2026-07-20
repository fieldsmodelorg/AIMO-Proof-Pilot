#!/usr/bin/env bash
# install_infervenv.sh — install the full proof-pilot inference runtime into a
# writable scratch dir (default /tmp/chankhavu/venvs/infervenv).
#
# Built for immutable-filesystem nodes (Singularity et al.) where ONLY /tmp is
# writable. Everything -- interpreter, stdlib, site-packages, humming, warm
# caches -- lands under one directory. `rm -rf $VENV` fully undoes it.
#
# The shipped venv contains ONLY site-packages; its stdlib comes from the
# bundled standalone CPython (.runtime/pybase). Relocating = rewriting
# pyvenv.cfg's `home`. Without that, `import os` dies.
#
# Usage:
#   ./install_infervenv.sh                       # download archive from HF
#   PP_ENV_ARCHIVE=/path/pp-env.bin ./install_infervenv.sh   # use local archive
#   ./install_infervenv.sh --repo /tmp/chankhavu/imo-inference
#
# Re-runnable. Steps are individually skippable via markers; --repatch reapplies
# SGLang patches only (cheap -- use after a `git pull` of your repo edits).
set -Eeuo pipefail

# ---------------------------------------------------------------- configuration
BASE="${PP_BASE:-/tmp/chankhavu}"
VENV="${VENV:-$BASE/venvs/infervenv}"
RUNTIME="$VENV/.runtime"
PYBASE="$RUNTIME/pybase"
CACHES="$RUNTIME/caches"
REPO="${REPO:-$BASE/imo-inference}"

# chankhavu/proof-pilot-env is PUBLIC -> anonymous download, no HF_TOKEN needed
# (HF_TOKEN is still honored if set, e.g. for a private fork). Revision + sha256
# are pinned to the exact runtime the Docker image bakes, so this venv matches it.
HF_REPO="${HF_REPO:-chankhavu/proof-pilot-env}"
HF_FILE="${HF_FILE:-proof-pilot-env.bin}"
HF_REVISION="${HF_REVISION:-5c0bf00bcc38c91b336f99d68aaab6b66aa93c1d}"
ARCHIVE="${PP_ENV_ARCHIVE:-}"          # local archive path; skips download
KEEP_ARCHIVE="${KEEP_ARCHIVE:-0}"      # 1 = keep the 4.6G download after extract

REPATCH_ONLY=0
SKIP_PIP="${SKIP_PIP:-0}"

# gzip'd tar of the runtime; ~4.6 GiB down, ~11 GiB extracted.
EXPECTED_ARCHIVE_BYTES=4644784760
# sha256 of proof-pilot-env.bin (same pin the Docker image verifies). Empty = skip.
EXPECTED_ARCHIVE_SHA256="${EXPECTED_ARCHIVE_SHA256:-71190f4f2554c29ec6b99ae6bda7af64f1348876b85cfbdfa1d102f9dfa8c831}"

log()  { printf '\033[1;36m[install]\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m[install] WARN:\033[0m %s\n' "$*" >&2; }
die()  { printf '\033[1;31m[install] ERROR:\033[0m %s\n' "$*" >&2; exit 1; }

usage() {
    cat <<EOF
install_infervenv.sh — proof-pilot inference runtime installer

  --repo PATH     imo-inference checkout to take SGLang patches from
                  (default: $REPO)
  --venv PATH     install target (default: $VENV)
  --repatch       reapply SGLang patches only, then exit
  --skip-pip      don't install evaluation/requirements.txt from PyPI
  -h, --help      this message

Environment:
  PP_ENV_ARCHIVE  local proof-pilot-env.bin (skips the HF download)
  HF_TOKEN        optional; $HF_REPO is public, only needed for a private fork
  KEEP_ARCHIVE=1  keep the downloaded archive after extraction
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --repo)     REPO="${2:?--repo needs a path}"; shift 2 ;;
        --venv)     VENV="${2:?--venv needs a path}"; RUNTIME="$VENV/.runtime"
                    PYBASE="$RUNTIME/pybase"; CACHES="$RUNTIME/caches"; shift 2 ;;
        --repatch)  REPATCH_ONLY=1; shift ;;
        --skip-pip) SKIP_PIP=1; shift ;;
        -h|--help)  usage; exit 0 ;;
        *)          die "unknown argument: $1 (try --help)" ;;
    esac
done

# ------------------------------------------------------------------- preflight
preflight() {
    log "preflight"

    mkdir -p "$BASE" 2>/dev/null || die "$BASE is not writable"
    [[ -w "$BASE" ]] || die "$BASE is not writable"

    # Extraction needs ~11G; +4.6G more if we also stage a download here.
    local need_kb=$((12 * 1024 * 1024))
    [[ -n "$ARCHIVE" ]] || need_kb=$((17 * 1024 * 1024))
    local free_kb
    free_kb="$(df -Pk "$BASE" | awk 'NR==2 {print $4}')"
    if (( free_kb < need_kb )); then
        die "need ~$((need_kb / 1024 / 1024))G free under $BASE, have $((free_kb / 1024 / 1024))G"
    fi
    log "  disk: $((free_kb / 1024 / 1024))G free under $BASE"

    for tool in tar curl sed awk find od df; do
        command -v "$tool" >/dev/null || die "missing required tool: $tool"
    done

    # launch_server.py hardcodes this path and raises FileNotFoundError without it.
    # Singularity --nv usually binds it here, but not always.
    if [[ ! -e /usr/lib/x86_64-linux-gnu/libcuda.so.1 ]]; then
        warn "/usr/lib/x86_64-linux-gnu/libcuda.so.1 is MISSING."
        warn "  evaluation/harness/launch_server.py hardcodes that path and will"
        warn "  raise FileNotFoundError at server start. Locate the real driver:"
        warn "    find / -name 'libcuda.so*' 2>/dev/null"
        warn "  (Singularity often injects it under /.singularity.d/libs/.)"
        warn "  Install proceeds -- this only bites when you launch the server."
    else
        log "  cuda driver: /usr/lib/x86_64-linux-gnu/libcuda.so.1"
    fi

    if command -v nvidia-smi >/dev/null; then
        log "  gpus: $(nvidia-smi --query-gpu=name --format=csv,noheader | paste -sd', ' -)"
    else
        warn "nvidia-smi not found; can't verify GPUs (install still works)"
    fi
}

# -------------------------------------------------------------------- download
resolve_archive() {
    if [[ -n "$ARCHIVE" ]]; then
        [[ -f "$ARCHIVE" ]] || die "PP_ENV_ARCHIVE does not exist: $ARCHIVE"
        log "using local archive: $ARCHIVE"
        return
    fi

    ARCHIVE="$BASE/$HF_FILE"
    if [[ -f "$ARCHIVE" ]] && (( $(stat -c%s "$ARCHIVE") == EXPECTED_ARCHIVE_BYTES )); then
        log "archive already downloaded: $ARCHIVE"
        return
    fi

    local url="https://huggingface.co/datasets/$HF_REPO/resolve/$HF_REVISION/$HF_FILE"
    log "downloading $HF_REPO:$HF_FILE (~4.6 GiB, resumable)"

    local auth=()
    [[ -n "${HF_TOKEN:-}" ]] && auth=(-H "Authorization: Bearer $HF_TOKEN")

    # -C - resumes a partial file; a killed download is safe to re-run.
    curl -fL -C - "${auth[@]}" -o "$ARCHIVE" "$url" \
        || die "download failed. If $HF_REPO is private, export HF_TOKEN=hf_..."
}

verify_archive() {
    local size
    size="$(stat -c%s "$ARCHIVE")"
    if (( size != EXPECTED_ARCHIVE_BYTES )); then
        warn "archive is $size bytes, expected $EXPECTED_ARCHIVE_BYTES"
        warn "  (fine if you built a custom archive; suspicious otherwise)"
    fi

    local magic
    magic="$(od -An -tx1 -N4 "$ARCHIVE" | tr -d ' \n')"
    [[ "$magic" == 1f8b* ]] \
        || die "archive is not gzip (magic=$magic). Truncated download? Delete and retry."

    # Pin the content by sha256 (same pin the Docker image bakes), so this venv is
    # byte-identical to the shipped runtime. Empty EXPECTED_ARCHIVE_SHA256 skips it.
    if [[ -n "$EXPECTED_ARCHIVE_SHA256" ]]; then
        local actual
        actual="$(sha256sum "$ARCHIVE" | awk '{print $1}')"
        [[ "$actual" == "$EXPECTED_ARCHIVE_SHA256" ]] \
            || die "archive sha256 mismatch: got $actual, expected $EXPECTED_ARCHIVE_SHA256 "\
"(runtime changed upstream; update HF_REVISION + EXPECTED_ARCHIVE_SHA256, or clear the sha)"
        log "archive verified: gzip, $((size / 1024 / 1024))MiB, sha256 OK"
    else
        log "archive verified: gzip, $((size / 1024 / 1024))MiB (sha256 check disabled)"
    fi
}

# --------------------------------------------------------------------- extract
extract_runtime() {
    if [[ -x "$VENV/bin/python" && -x "$PYBASE/bin/python3" ]]; then
        log "runtime already extracted at $VENV"
        return
    fi
    [[ ! -e "$VENV" ]] || die "$VENV exists but is incomplete; rm -rf it and retry"

    resolve_archive
    verify_archive

    local stage="$BASE/.pp-stage.$$"
    rm -rf "$stage"; mkdir -p "$stage"
    # shellcheck disable=SC2064
    trap "rm -rf '$stage'" EXIT

    log "extracting ~11 GiB (a few minutes)"
    tar -xzf "$ARCHIVE" -C "$stage" --strip-components=1   # strips pp-env/

    [[ -x "$stage/venv/bin/python" ]]    || die "archive has no venv/bin/python"
    [[ -x "$stage/pybase/bin/python3" ]] || die "archive has no pybase/bin/python3"

    # Target layout: the venv sits exactly at $VENV; everything else it needs is
    # tucked into $VENV/.runtime so one path holds the whole install.
    log "arranging layout under $VENV"
    mkdir -p "$(dirname "$VENV")"
    mv "$stage/venv" "$VENV"
    mkdir -p "$RUNTIME"
    for d in pybase humming proof-pilot flashinfer_cache humming_cache uv; do
        [[ -e "$stage/$d" ]] && mv "$stage/$d" "$RUNTIME/$d"
    done

    rm -rf "$stage"; trap - EXIT

    if [[ "$KEEP_ARCHIVE" != "1" && -z "${PP_ENV_ARCHIVE:-}" ]]; then
        log "removing downloaded archive (KEEP_ARCHIVE=1 to keep)"
        rm -f "$ARCHIVE"
    fi
}

# -------------------------------------------------------------------- relocate
relocate_venv() {
    log "relocating venv -> $PYBASE"

    # THE load-bearing step. The venv ships site-packages only; `home` still
    # points at the build host's /.uv path. Repoint it at the bundled CPython
    # or the interpreter cannot find its stdlib.
    sed -i "s|^home = .*|home = $PYBASE/bin|" "$VENV/pyvenv.cfg"

    # Console scripts carry a stale absolute shebang baked at build time
    # (/workspace/sglang-nightly-py312-venv/bin/python3). Nothing in the harness
    # uses them -- it always calls $VENV/bin/python -m ... -- but fix them so
    # `sglang`, `flashinfer`, `hf` etc. work if you reach for them directly.
    local fixed=0 f
    for f in "$VENV"/bin/*; do
        [[ -f "$f" && -r "$f" ]] || continue
        head -c2 "$f" 2>/dev/null | grep -q '^#!' || continue
        if head -1 "$f" | grep -q '^#!.*python'; then
            sed -i "1s|^#!.*python.*|#!$VENV/bin/python3|" "$f"
            fixed=$((fixed + 1))
        fi
    done
    log "  rewrote $fixed console-script shebangs"

    "$VENV/bin/python" - <<PY || die "venv is broken after relocation"
import os, sys
assert os.path.realpath(sys.base_prefix) == os.path.realpath("$PYBASE"), \
    f"base_prefix={sys.base_prefix} != $PYBASE"
import sglang, torch
print(f"  sglang {sglang.__version__} | torch {torch.__version__} | base {sys.base_prefix}")
PY
}

# ------------------------------------------------------------------ extra deps
install_extra_deps() {
    local req="$REPO/evaluation/requirements.txt"
    if [[ "$SKIP_PIP" == "1" ]]; then
        log "skipping PyPI deps (--skip-pip)"
        return
    fi
    if [[ ! -f "$req" ]]; then
        warn "no $req -- skipping extra deps."
        warn "  Clone the repo to $REPO and re-run, or pass --repo PATH."
        return
    fi

    local hash marker uv
    hash="$(sha256sum "$req" | awk '{print $1}')"
    marker="$RUNTIME/.deps-$hash"
    if [[ -f "$marker" ]]; then
        log "extra deps already installed for this requirements.txt"
        return
    fi

    uv="$RUNTIME/uv"
    [[ -x "$uv" ]] || uv="$(command -v uv || true)"
    [[ -n "$uv" && -x "$uv" ]] || die "no uv binary (expected bundled at $RUNTIME/uv)"

    log "installing pinned deps from PyPI (flash-attn-4, cutlass-dsl, quack-kernels)"
    UV_LINK_MODE=copy UV_CACHE_DIR="$CACHES/uv" \
        "$uv" pip install --python "$VENV/bin/python" -r "$req" \
        || die "dependency install failed (PyPI reachable?). Retry, or --skip-pip."
    touch "$marker"
}

# --------------------------------------------------------------------- patches
apply_patches() {
    local patcher="$REPO/sglang_patches/apply_patches.sh"
    if [[ ! -f "$patcher" ]]; then
        warn "no $patcher -- SGLang is NOT patched."
        warn "  Clone imo-inference to $REPO and re-run: $0 --repatch"
        return 1
    fi

    local helper="$RUNTIME/proof-pilot/deploy/w4a8/humming_w4a8.py"
    [[ -f "$helper" ]] || die "humming helper missing: $helper"

    log "applying SGLang patches from $REPO"

    # Newer apply_patches.sh takes the helper path as $2 (or $W4A8_HELPER). Older
    # revisions hardcode /workspace/pp/... -- for those, run a rewritten copy of
    # the WHOLE dir: the script finds its payload relative to its own path
    # (SRC=$(dirname $BASH_SOURCE)), so copying the script alone would leave SRC
    # pointing at a dir with no patch files.
    if grep -q 'W4A8_HELPER' "$patcher"; then
        bash "$patcher" "$VENV" "$helper" || die "patch application failed"
    else
        log "  (old apply_patches.sh: rewriting hardcoded /workspace/pp path)"
        local tmp="$CACHES/tmp/sglang_patches"
        rm -rf "$tmp"; mkdir -p "$tmp"
        cp -a "$REPO/sglang_patches/." "$tmp/"
        sed -i "s|/workspace/pp/proof-pilot/deploy/w4a8/humming_w4a8.py|$helper|g" \
            "$tmp/apply_patches.sh"
        bash "$tmp/apply_patches.sh" "$VENV" || die "patch application failed"
    fi

    "$VENV/bin/python" - <<PY || die "patch verification failed"
import pathlib, sys
srt = next(pathlib.Path("$VENV/lib").glob("python*/site-packages/sglang/srt"))
checks = {
    "models/olmo2.py": "Olmo3Sink target",
    "models/dflash.py": "DFlash draft",
    "speculative/dflash_worker_v2.py": "DFlash worker",
    "speculative/dflash_info_v2.py": "DFlash SWA evict",
    "speculative/triton_ops/fused_kv_materialize.py": "fused KV materialize",
}
missing = [f"{p} ({d})" for p, d in checks.items() if not (srt / f"{p}.orig").exists()]
if missing:
    print("  NOT patched (no .orig backup):", *missing, sep="\n    ")
    sys.exit(1)
helper = pathlib.Path("$helper").read_text()
assert "HUMMING_TARGET_ONLY" in helper, "humming target-scope patch missing"
print(f"  all {len(checks)} SGLang files patched + humming helper scoped")
PY
}

# ------------------------------------------------------- env activation script
write_activate() {
    local script="$RUNTIME/activate-env.sh"
    log "writing $script"

    cat > "$script" <<EOF
# activate-env.sh — source me before running anything from this venv.
#   source $RUNTIME/activate-env.sh
#
# GENERATED by install_infervenv.sh. Re-running the installer overwrites this.
#
# Every var below exists because this node's \$HOME is READ-ONLY. Each of these
# libraries defaults to writing under ~ and will hard-fail without a redirect:
#   triton  -> ~/.triton      sglang -> ~/.cache/sglang
#   torch   -> ~/.cache/torch flashinfer -> ~/.cache/flashinfer

export VENV="$VENV"
export PATH="$VENV/bin:\$PATH"

# The bundled CPython is a RELOCATED standalone build, so libpython3.12.so.1.0
# is not on the default loader path. Without this, flashinfer silently degrades:
#   "flashinfer.comm allreduce_fusion API is not available
#    (libpython3.12.so.1.0: cannot open shared object file)
#    ... falling back to standard implementation"
# That is the FUSED ALL-REDUCE path -- it matters on a TP>1 run. Verified: adding
# this flips flashinfer.comm allreduce_fusion back to available.
export LD_LIBRARY_PATH="$PYBASE/lib\${LD_LIBRARY_PATH:+:\$LD_LIBRARY_PATH}"

# --- writable scratch (HOME itself is a fallback net for anything we missed) ---
export HOME="\${PP_FAKE_HOME:-$CACHES/home}"
export TMPDIR="$CACHES/tmp"
export XDG_CACHE_HOME="$CACHES/xdg"
export XDG_CONFIG_HOME="$CACHES/xdg-config"

# --- per-library cache redirects (each verified against this venv) ---
export TRITON_HOME="$CACHES/triton"
export TRITON_CACHE_DIR="$CACHES/triton/.triton/cache"
export SGLANG_CACHE_DIR="$CACHES/sglang"
export TORCHINDUCTOR_CACHE_DIR="$CACHES/torchinductor"
export TORCH_HOME="$CACHES/torch"
export OUTLINES_CACHE_DIR="$CACHES/outlines"
export CUDA_CACHE_PATH="$CACHES/nv"
export HF_HOME="$CACHES/hf"
export UV_CACHE_DIR="$CACHES/uv"

# FLASHINFER_CACHE_DIR is derived as \$FLASHINFER_WORKSPACE_BASE/.cache/flashinfer,
# so set the BASE (setting the CACHE_DIR alone does not take effect).
export FLASHINFER_WORKSPACE_BASE="$CACHES/flashinfer_base"

# --- humming (W4A8) ---
# HUMMING_PATH must be the dir CONTAINING the humming/ package: the w4a8 glue
# does sys.path.insert(HUMMING_PATH); import humming.
export HUMMING_PATH="$RUNTIME"
export W4A8_HELPER_DIR="$RUNTIME/proof-pilot/deploy/w4a8"
export HUMMING_CACHE_DIR="$CACHES/humming"
export HUMMING_TMP_DIR="$CACHES/tmp/humming"

# --- runtime knobs the harness expects (mirrors ycchen's bootstrap) ---
export FLASHINFER_USE_CUDA_NORM=1
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

mkdir -p "\$HOME" "\$TMPDIR" "\$XDG_CACHE_HOME" "\$XDG_CONFIG_HOME" \\
         "\$TRITON_HOME" "\$TRITON_CACHE_DIR" "\$SGLANG_CACHE_DIR" \\
         "\$TORCHINDUCTOR_CACHE_DIR" "\$TORCH_HOME" "\$OUTLINES_CACHE_DIR" \\
         "\$CUDA_CACHE_PATH" "\$HF_HOME" "\$UV_CACHE_DIR" \\
         "\$FLASHINFER_WORKSPACE_BASE/.cache/flashinfer" \\
         "\$HUMMING_CACHE_DIR" "\$HUMMING_TMP_DIR" 2>/dev/null

echo "[proof-pilot] venv=\$VENV  python=\$(command -v python)"
EOF
    chmod 0644 "$script"
}

seed_caches() {
    log "seeding warm JIT caches (skips first-call compiles)"
    local fi_dst="$CACHES/flashinfer_base/.cache/flashinfer"
    local hm_dst="$CACHES/humming"
    mkdir -p "$fi_dst" "$hm_dst"
    [[ -d "$RUNTIME/flashinfer_cache" ]] && cp -rn "$RUNTIME/flashinfer_cache/." "$fi_dst/" 2>/dev/null
    [[ -d "$RUNTIME/humming_cache" ]]    && cp -rn "$RUNTIME/humming_cache/." "$hm_dst/" 2>/dev/null
    return 0
}

# ------------------------------------------------------------------------ main
main() {
    if (( REPATCH_ONLY )); then
        [[ -x "$VENV/bin/python" ]] || die "no venv at $VENV -- run a full install first"
        apply_patches || exit 1
        log "repatch done."
        exit 0
    fi

    preflight
    extract_runtime
    relocate_venv
    install_extra_deps
    write_activate
    seed_caches
    local patched=1
    apply_patches || patched=0

    cat <<EOF

$(log "install complete")

  venv     $VENV
  python   $VENV/bin/python
  runtime  $RUNTIME
  patches  $( ((patched)) && echo "applied from $REPO" || echo "NOT APPLIED -- see warning above")

Next:

  source $RUNTIME/activate-env.sh

After editing SGLang patches on GitHub and pulling to $REPO:

  cd $REPO && git pull && $0 --repatch

EOF
}

main "$@"
