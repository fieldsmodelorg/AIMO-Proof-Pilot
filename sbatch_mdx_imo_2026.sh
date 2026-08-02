#!/usr/bin/env bash
#SBATCH --job-name=aimo_imo_2026
#SBATCH --partition=gpu
#SBATCH --nodes=24
#SBATCH --ntasks=24
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=8
#SBATCH --cpus-per-task=32
#SBATCH --time=48:00:00
#SBATCH --output=slurm-%x-%j.out
#SBATCH --error=slurm-%x-%j.err

# Start the existing Proof Pilot SIF endpoint on all MDX nodes.
#
# Submit (example only):
#   sbatch --export=ALL,\
#AIMO_EXP_DIR=/data/IKOU/experiments/0371_aimo,\
#AIMO_SIF=/path/to/sif,\
#AIMO_SHARED_TMP=/data/IKOU/experiments/0371_aimo/tmp \
#     sbatch_mdx_imo2026.sh
set -Eeuo pipefail
umask 077

log() { printf '[mdx-endpoint] %s\n' "$*"; }
die() { printf '[mdx-endpoint] ERROR: %s\n' "$*" >&2; exit 1; }

SCRIPT_PATH="$(realpath -- "${BASH_SOURCE[0]}")"

# A batch script starts on one node only. Fan out one worker per allocated
# node; each worker receives all eight local GPUs and 32 CPU cores.
if [[ "${1:-}" != "--worker" ]]; then
    [[ -n "${SLURM_JOB_ID:-}" ]] || die "submit this launcher with sbatch"
    log "launching 24 endpoint workers"
    exec srun \
        --nodes=24 \
        --ntasks=24 \
        --ntasks-per-node=1 \
        --cpus-per-task=32 \
        --gpus-per-task=8 \
        --kill-on-bad-exit=1 \
        "$SCRIPT_PATH" --worker
fi
shift

EXP_DIR="${AIMO_EXP_DIR:-/path/to/exp}"
SIF="${AIMO_SIF:-/path/to/sif}"
SHARED_TMP="${AIMO_SHARED_TMP:-${EXP_DIR}/tmp}"
JOB_ID="${SLURM_JOB_ID:-manual-$(date -u +%Y%m%dT%H%M%SZ)}"
NODE_RANK="${SLURM_PROCID:-${SLURM_NODEID:-0}}"
NODE_HOST="$(hostname)"
JOB_ROOT="${AIMO_RUN_ROOT:-${EXP_DIR}/mdx_jobs/${JOB_ID}}"
RUN_ROOT="${JOB_ROOT}/node-${NODE_RANK}-${NODE_HOST}"
CLIENT_ID_PREFIX="${AIMO_CLIENT_ID_PREFIX:-mdx-${JOB_ID}}"
CLIENT_ID="${CLIENT_ID_PREFIX}-node${NODE_RANK}-${NODE_HOST}"

mkdir -p \
    "$RUN_ROOT/home" \
    "$RUN_ROOT/imochallenge" \
    "$RUN_ROOT/apptainer/tmp" \
    "$RUN_ROOT/apptainer/cache"

exec > >(tee -a "$RUN_ROOT/job.log") 2>&1
STATUS_FILE="$RUN_ROOT/status"
printf 'RUNNING\n' >"$STATUS_FILE"
finish() {
    local status=$?
    trap - EXIT
    printf '%s\n' "$status" >"$STATUS_FILE"
    log "finished with exit code $status; logs: $RUN_ROOT"
    exit "$status"
}
trap finish EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

log "host=$NODE_HOST job_id=$JOB_ID node_rank=$NODE_RANK"
log "sif=$SIF"
log "shared_tmp=$SHARED_TMP"
log "run_root=$RUN_ROOT"

[[ -f "$SIF" ]] || die "SIF not found: $SIF"
[[ -d "$SHARED_TMP" ]] || die "old /tmp tree not found: $SHARED_TMP"

# Match the rootless Apptainer setup from the MDX example supplied by Michal.
export PATH="$HOME/.local/bin:$HOME/apptainer-rootless/bin:$PATH"
export APPTAINER_TMPDIR="$RUN_ROOT/apptainer/tmp"
export APPTAINER_CACHEDIR="$RUN_ROOT/apptainer/cache"
export TMPDIR="$APPTAINER_TMPDIR"

RUNTIME="$(command -v singularity || command -v apptainer || true)"
[[ -n "$RUNTIME" ]] || die "singularity/apptainer is not on PATH"
"$RUNTIME" --version
nvidia-smi

VISIBLE_GPU_COUNT="$(nvidia-smi -L | wc -l | tr -d ' ')"
[[ "$VISIBLE_GPU_COUNT" == "8" ]] \
    || die "expected 8 allocated GPUs, found $VISIBLE_GPU_COUNT"

# --containall needs explicit forwarding. Export both prefixes because MDX may
# expose either the Singularity or Apptainer command name.
pass_container_env() {
    local name="$1" value="$2"
    printf -v "SINGULARITYENV_${name}" '%s' "$value"
    printf -v "APPTAINERENV_${name}" '%s' "$value"
    export "SINGULARITYENV_${name}" "APPTAINERENV_${name}"
}

pass_container_env CUDA_VISIBLE_DEVICES "${CUDA_VISIBLE_DEVICES:-0,1,2,3,4,5,6,7}"
pass_container_env NVIDIA_VISIBLE_DEVICES all
pass_container_env CLIENT_ID "$CLIENT_ID"
pass_container_env SLURM_JOB_ID "$JOB_ID"
pass_container_env SLURM_NODEID "$NODE_RANK"
pass_container_env AIMO_NODE_RANK "$NODE_RANK"
pass_container_env TMP /tmp
pass_container_env TMPDIR /tmp
pass_container_env HF_HOME /tmp/hf_home
pass_container_env HUGGINGFACE_HUB_CACHE /tmp/hf_cache
pass_container_env HF_HUB_CACHE /tmp/hf_cache
pass_container_env XDG_CACHE_HOME /tmp/xdg_cache
[[ -z "${HF_TOKEN:-}" ]] || pass_container_env HF_TOKEN "$HF_TOKEN"
[[ -z "${GITHUB_TOKEN:-}" ]] || pass_container_env GITHUB_TOKEN "$GITHUB_TOKEN"

cat >"$RUN_ROOT/metadata.txt" <<EOF
job_id=$JOB_ID
host=$NODE_HOST
node_rank=$NODE_RANK
client_id=$CLIENT_ID
sif=$SIF
shared_tmp=$SHARED_TMP
docker_socket=$([[ -S /var/run/docker.sock ]] && printf available || printf unavailable)
EOF

log "starting the SIF runscript; it remains active until walltime or scancel"
"$RUNTIME" run --nv --containall \
    --bind "$SHARED_TMP:/tmp" \
    --bind "$RUN_ROOT/imochallenge:/tmp/imochallenge" \
    --bind /dev/infiniband:/dev/infiniband \
    --bind /var/run/docker.sock:/var/run/docker.sock \
    --home "$RUN_ROOT/home:/home/guest" \
    --pwd /home/guest \
    "$SIF"
