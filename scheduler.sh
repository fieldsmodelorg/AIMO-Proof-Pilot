#!/usr/bin/env bash
# scheduler.sh -- one command to run a full proof-pilot inference.
#
# Starts the SGLang server, waits for it to become healthy, validates its config,
# smoke-tests a real generation query, then runs the inference to completion as
# the main process. When inference finishes (or on Ctrl-C / error) it tears the
# server down cleanly. Everything for the run lands in one output directory.
#
# Usage:
#   ./scheduler.sh <config> <output-dir> [input.csv]     # start a run
#   ./scheduler.sh --resume <output-dir>                 # continue a crashed/stopped run
#
#   <config>      a config NAME from this repo (e.g. config-model-step225-budget-xhigh.yaml) or a path
#   <output-dir>  run outputs go here: submission.csv, artifacts/, server.log, ...
#   [input.csv]   problems file (id,problem). Default: the committed IMO-2026 set
#                 evaluation/data/imo2026-latex-test.csv
#
#   -r, --resume  continue the run in <output-dir>, reusing its pinned config + input
#                 (no need to re-specify them); finished problems are skipped
#   -n, --plan    resolve + validate everything and print the plan, but do NOT launch
#   -h, --help    show this help
#
# Env overrides (all optional):
#   VENV                             runtime venv (default /opt/pp/venv); its bin/python runs everything
#   PYTHON                           python to use (default $VENV/bin/python)
#   SERVER_STARTUP_TIMEOUT_SECONDS   health-wait timeout (default 2700)
#   SMOKE_MAX_TOKENS                 tokens for the smoke query (default 32)
#   HF_TOKEN                         for trace upload; auto-sourced from `hf auth token` if unset
#
# Resume: if a run crashes or the node reboots, re-launch it with
#   ./scheduler.sh --resume <output-dir>
# It restarts the server and continues -- finished problems are skipped and a
# partially-done problem picks up from its last completed round.
set -Eeuo pipefail

REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
VENV="${VENV:-/opt/pp/venv}"
PYTHON="${PYTHON:-$VENV/bin/python}"
DEFAULT_INPUT="$REPO/evaluation/data/imo2026-latex-test.csv"
SERVER_STARTUP_TIMEOUT_SECONDS="${SERVER_STARTUP_TIMEOUT_SECONDS:-2700}"
SMOKE_MAX_TOKENS="${SMOKE_MAX_TOKENS:-32}"

SERVER_PID=
SERVER_PORT=

log() { printf '[scheduler] %s\n' "$*"; }
die() { printf '[scheduler] ERROR: %s\n' "$*" >&2; exit 1; }

usage() {
    # Print the leading comment block (help text), stripping the leading "# ".
    awk 'NR==1{next} /^#/{sub(/^# ?/,""); print; next} {exit}' "${BASH_SOURCE[0]}"
    exit "${1:-0}"
}

# --- argument parsing -------------------------------------------------------
PLAN=0
RESUME=0
while [[ "${1:-}" == -* ]]; do
    case "$1" in
        -h|--help)   usage 0 ;;
        -n|--plan)   PLAN=1;   shift ;;
        -r|--resume) RESUME=1; shift ;;
        --)          shift; break ;;
        *)           die "unknown option: $1 (see --help)" ;;
    esac
done

if [[ "$RESUME" == "1" ]]; then
    # ./scheduler.sh --resume <output-dir> : reuse the run's pinned config + input.
    OUTPUT_DIR="${1:-}"
    [[ -n "$OUTPUT_DIR" ]] || die "--resume needs the output-dir to continue: ./scheduler.sh --resume <output-dir>"
    [[ -z "${2:-}" ]] || die "--resume takes only <output-dir>; the config + input are read from its artifacts/ (you cannot change them mid-run). Got extra argument: ${2}"
    [[ -d "$OUTPUT_DIR" ]] || die "output-dir does not exist: $OUTPUT_DIR"
    OUTPUT_DIR="$(realpath "$OUTPUT_DIR")"
    CONFIG="$OUTPUT_DIR/artifacts/config.yaml"   # pinned at first launch
    INPUT="$OUTPUT_DIR/artifacts/test.csv"       # pinned at first launch
    [[ -f "$CONFIG" && -f "$INPUT" ]] || die "no resumable run in $OUTPUT_DIR (missing artifacts/config.yaml or artifacts/test.csv) -- start a fresh run: ./scheduler.sh <config> <output-dir>"
    log "resume: continuing the run in $OUTPUT_DIR (finished problems are skipped)"
else
    CONFIG_ARG="${1:-}"
    OUTPUT_DIR="${2:-}"
    INPUT_ARG="${3:-}"
    [[ -n "$CONFIG_ARG" ]] || usage 1
    [[ -n "$OUTPUT_DIR" ]] || die "output-dir is required (argument 2); see --help"
    # resolve the config: a repo config name, or a path
    if [[ -f "$CONFIG_ARG" ]]; then
        CONFIG="$(realpath "$CONFIG_ARG")"
    elif [[ -f "$REPO/$CONFIG_ARG" ]]; then
        CONFIG="$REPO/$CONFIG_ARG"
    else
        die "config not found: '$CONFIG_ARG' (looked in the current dir and the repo root). Available: $(cd "$REPO" && ls config*.yaml 2>/dev/null | tr '\n' ' ')"
    fi
    # resolve the problems file (default = committed IMO-2026 LaTeX set)
    INPUT="${INPUT_ARG:-$DEFAULT_INPUT}"
    [[ -f "$INPUT" ]] || die "problems file not found: $INPUT"
    mkdir -p "$OUTPUT_DIR"
    OUTPUT_DIR="$(realpath "$OUTPUT_DIR")"
fi

# --- runtime python sanity (accept a bare command name or an absolute path) -
_py="$(command -v "$PYTHON" 2>/dev/null || true)"
[[ -n "$_py" ]] || die "python not found: $PYTHON -- set VENV to the runtime venv (VENV=/path/to/venv) or 'source .../activate-env.sh' and set PYTHON"
PYTHON="$_py"; unset _py

# --- output layout ----------------------------------------------------------
SERVER_LOG="$OUTPUT_DIR/server.log"
SERVER_VALIDATION="$OUTPUT_DIR/server-validation.json"
SUBMISSION_CSV="$OUTPUT_DIR/submission.csv"
ARTIFACTS_DIR="$OUTPUT_DIR/artifacts"

# --- inspect the config for server url/port/model (validates the YAML too) --
INSPECT="$("$PYTHON" "$REPO/docker/inspect_config.py" "$CONFIG")" || die "config failed validation: $CONFIG"
read_field() { "$PYTHON" -c 'import json,sys;print(json.load(sys.stdin)[sys.argv[1]])' "$1" <<<"$INSPECT"; }
SERVER_URL="$(read_field server_url)"
SERVER_PORT="$(read_field server_port)"
TARGET_MODEL="$(read_field target_model)"
GPU_COUNT="$(read_field expected_gpu_count)"

log "config       : $CONFIG"
log "input        : $INPUT"
log "output dir   : $OUTPUT_DIR"
log "server       : $SERVER_URL (port $SERVER_PORT, expects $GPU_COUNT GPUs)"
log "target model : $TARGET_MODEL"

if [[ "$PLAN" == "1" ]]; then
    log "plan mode: resolved and validated OK; NOT launching."
    log "would: start server -> wait for health -> validate -> smoke-test -> run inference -> teardown"
    exit 0
fi

# --- models present? fail early with a clear pointer to download_models.sh ---
[[ -d "$TARGET_MODEL" && -f "$TARGET_MODEL/config.json" ]] \
    || die "target model not found at $TARGET_MODEL -- fetch the weights first with ./download_models.sh (see the README quick start)"

# --- apply the SGLang patches (idempotent) -----------------------------------
# The REQUIRED Olmo3Sink model patch is applied here, so a run that bypasses the
# container entrypoint (e.g. `docker run --entrypoint bash`) still gets it.
# apply_patches.sh backs up originals to *.orig and is a no-op if already applied.
RUNTIME_ROOT="${RUNTIME_ROOT:-${VENV%/venv}}"
_helper="$RUNTIME_ROOT/proof-pilot/deploy/w4a8/humming_w4a8.py"
if [[ -f "$REPO/sglang_patches/apply_patches.sh" ]]; then
    # apply_patches.sh present -> the REQUIRED Olmo3Sink patch MUST be applied. A
    # missing helper means RUNTIME_ROOT/VENV is not the expected baked runtime; fail
    # loudly rather than silently running UNPATCHED SGLang (no sinks -> wrong numerics).
    [[ -f "$_helper" ]] || die "SGLang patch helper not found: $_helper -- point RUNTIME_ROOT/VENV at the baked runtime; the required Olmo3Sink patch cannot be skipped"
    log "applying SGLang patches (idempotent)"
    bash "$REPO/sglang_patches/apply_patches.sh" "$VENV" "$_helper" \
        || die "SGLang patch step failed -- see output above"
else
    log "NOTE: sglang_patches/apply_patches.sh not present; assuming a pre-patched runtime"
fi
unset _helper

# --- refuse to start if the port is already taken ----------------------------
# We never adopt or kill a server we did not launch. If the port is busy, stop
# now -- this is what keeps teardown safe even on a shared node.
if "$PYTHON" -c "import socket,sys; s=socket.socket(); rc=s.connect_ex(('127.0.0.1',$SERVER_PORT)); s.close(); sys.exit(0 if rc==0 else 1)" 2>/dev/null; then
    die "port $SERVER_PORT is already in use -- another server is running there. Free it, or change server.port in the config. (Refusing to start so teardown never touches a server we did not launch.)"
fi

# --- trace-upload token: source on-box if unset, never printed --------------
if [[ -z "${HF_TOKEN:-}" ]] && command -v hf >/dev/null 2>&1; then
    _tok="$(hf auth token 2>/dev/null || true)"
    if [[ -n "$_tok" ]]; then export HF_TOKEN="$_tok"; log "HF_TOKEN sourced from 'hf auth token' (for trace upload)"; fi
    unset _tok
fi

# --- teardown: stop ONLY the server WE launched ------------------------------
# The server runs in its own process group (setsid), so the group kill is
# surgical. The fuser-by-port backstop runs ONLY after we confirmed OUR server
# bound the port (SERVER_BOUND=1); combined with the pre-flight "port already in
# use -> refuse to start" check above, it can never hit another job's server.
SERVER_BOUND=0
teardown() {
    local status=$?
    trap - EXIT INT TERM
    if [[ -n "$SERVER_PID" ]] && kill -0 "$SERVER_PID" 2>/dev/null; then
        log "stopping server (pid=$SERVER_PID)"
        kill -TERM "$SERVER_PID" 2>/dev/null || true
        kill -TERM -"$SERVER_PID" 2>/dev/null || true   # its process group, if leader
        for _ in $(seq 1 15); do kill -0 "$SERVER_PID" 2>/dev/null || break; sleep 1; done
        kill -KILL "$SERVER_PID" 2>/dev/null || true
        kill -KILL -"$SERVER_PID" 2>/dev/null || true
    fi
    if [[ "$SERVER_BOUND" == "1" && -n "$SERVER_PORT" ]] && command -v fuser >/dev/null 2>&1; then
        fuser -k -9 "${SERVER_PORT}/tcp" 2>/dev/null || true   # our port (we bound it) -> reap a lingering worker
    fi
    log "finished (exit $status); outputs in $OUTPUT_DIR"
    exit "$status"
}

# --- start the server in its own process group ------------------------------
: > "$SERVER_LOG"
log "starting SGLang server (log: $SERVER_LOG)"
setsid "$PYTHON" -u "$REPO/evaluation/harness/launch_server.py" --config "$CONFIG" \
    >"$SERVER_LOG" 2>&1 </dev/null &
SERVER_PID=$!
trap teardown EXIT INT TERM

# --- wait for health, failing fast if the server dies -----------------------
log "waiting for server health (timeout ${SERVER_STARTUP_TIMEOUT_SECONDS}s; tail -f $SERVER_LOG)"
deadline=$(( SECONDS + SERVER_STARTUP_TIMEOUT_SECONDS ))
until "$PYTHON" -c "import urllib.request; urllib.request.urlopen('$SERVER_URL/health', timeout=5)" 2>/dev/null; do
    kill -0 "$SERVER_PID" 2>/dev/null || die "server exited before becoming healthy -- see $SERVER_LOG"
    (( SECONDS < deadline )) || die "server not healthy within ${SERVER_STARTUP_TIMEOUT_SECONDS}s -- see $SERVER_LOG"
    sleep 5
done
# our own process must be the one that became healthy (belt-and-braces with the
# pre-flight port check: never run inference against a server we did not launch)
kill -0 "$SERVER_PID" 2>/dev/null \
    || die "$SERVER_URL answered but our server process is gone -- refusing to use a foreign server; see $SERVER_LOG"
SERVER_BOUND=1
log "server healthy"

# --- strict config validation (same checks as the container path) -----------
log "validating server config -> $SERVER_VALIDATION"
"$PYTHON" "$REPO/evaluation/harness/validate_server.py" \
    --url "$SERVER_URL" --config "$CONFIG" \
    --output "$SERVER_VALIDATION" --server-log "$SERVER_LOG" \
    || die "server config validation failed -- see $SERVER_VALIDATION and $SERVER_LOG"

# --- generation smoke test: a real chat completion must produce tokens ------
log "smoke-testing a generation query"
if ! SMOKE_URL="$SERVER_URL" SMOKE_MODEL="$TARGET_MODEL" SMOKE_MAX_TOKENS="$SMOKE_MAX_TOKENS" \
    "$PYTHON" - <<'PY'
import json, os, sys, urllib.request
url = os.environ["SMOKE_URL"].rstrip("/") + "/v1/chat/completions"
body = json.dumps({
    "model": os.environ["SMOKE_MODEL"],
    "messages": [{"role": "user", "content": "Reply with the single word: ready."}],
    "max_tokens": int(os.environ["SMOKE_MAX_TOKENS"]),
    "temperature": 0,
}).encode()
req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req, timeout=180) as r:
    data = json.load(r)
choice = (data.get("choices") or [{}])[0]
msg = choice.get("message") or {}
produced = (msg.get("content") or "") + (msg.get("reasoning_content") or "")
if not produced.strip():
    sys.stderr.write("empty generation: " + json.dumps(data)[:400] + "\n")
    sys.exit(1)
print("[scheduler] smoke ok: finish_reason=%s, produced %d chars" % (choice.get("finish_reason"), len(produced)))
PY
then
    die "generation smoke test failed -- server is up but not generating; see $SERVER_LOG"
fi

# --- run the inference to completion, as the main (foreground) process ------
log "running inference over all problems in $(basename "$INPUT")"
"$PYTHON" -u "$REPO/evaluation/harness/run_submission.py" \
    --config "$CONFIG" \
    --input "$INPUT" \
    --output "$SUBMISSION_CSV" \
    --artifacts-dir "$ARTIFACTS_DIR"

log "inference complete -> $SUBMISSION_CSV"
# teardown() runs on EXIT and stops the server.
