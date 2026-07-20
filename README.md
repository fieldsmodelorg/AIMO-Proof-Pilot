# AIMO Proof Pilot Inference

This repository packages the generate-verify-refine proof harness as a Docker
image. The submission path reads `test.csv`, runs the selected harness, and
writes `submission.csv` without calling an external grader. The checked-in
configuration uses eight H200 GPUs as four TP2 replicas, BF16 target and draft
weights, DFlash speculative decoding, and FlashAttention 3.

## Run it directly (one command)

If you already have the runtime venv on the box (e.g. an NII node, or the baked
`/opt/pp/venv`), [`scheduler.sh`](scheduler.sh) runs a full inference end-to-end:
it starts the SGLang server, waits for health, validates the config,
**smoke-tests a real generation query**, runs the inference to completion as the
main process, then tears the server down (also on Ctrl-C or error).

```bash
# ./scheduler.sh <config> <output-dir> [input.csv]

# run all six committed IMO-2026 problems with the 2x-deploy config:
VENV=/opt/pp/venv ./scheduler.sh config-nii-2x.yaml runs/deploy-2x

# a custom problem set:
VENV=/opt/pp/venv ./scheduler.sh config.yaml runs/my-run path/to/my-problems.csv

# resolve + validate everything WITHOUT launching (fast, no GPU needed):
VENV=/opt/pp/venv ./scheduler.sh --plan config-nii-2x.yaml runs/deploy-2x
```

**Arguments**
- **`<config>`** — a config *name* from this repo (e.g. `config-nii-2x.yaml`) or a path to one.
- **`<output-dir>`** — everything for the run lands here: `submission.csv`,
  `artifacts/` (resumable search state), `server.log`, `server-validation.json`.
- **`[input.csv]`** — problems file with exactly `id,problem` columns; defaults to
  the committed IMO-2026 LaTeX set `evaluation/data/imo2026-latex-test.csv`.

**Notes**
- Point `VENV` at the runtime venv (default `/opt/pp/venv`), or `source` its
  `activate-env.sh` and set `PYTHON`.
- **No HuggingFace auth is required to run.** If the config enables trace upload,
  the token is auto-sourced from `hf auth token`; when there is none, uploads are
  simply skipped (the run still writes `submission.csv` + `artifacts/` locally).
- Re-run with the same `<output-dir>` to **resume** an interrupted run.
- Teardown is surgical (the server's own process group + its exclusive port), so it
  is **safe on shared nodes** — it never touches another job's server.

## Docker usage

### Select the harness commit

The image is built on demand (a `v*` release tag or a manual **Run workflow** in
the Actions tab — the baked image is ~19 GB, so it is not built per commit) and
published to **`ghcr.io/hav4ik/imo-inference`** and the Docker Hub mirror
**`docker.io/chankhavu/imo-inference`**, each tagged `sha-<7-character-commit>`.
Set `COMMIT` to the full commit of a build that completed successfully:

```bash
export COMMIT=REPLACE_WITH_FULL_COMMIT_SHA
export IMAGE=ghcr.io/hav4ik/imo-inference:sha-${COMMIT:0:7}   # or docker.io/chankhavu/imo-inference:sha-${COMMIT:0:7}

docker pull "$IMAGE"
test "$(docker image inspect "$IMAGE" \
  --format "{{ index .Config.Labels \"org.opencontainers.image.revision\" }}")" = "$COMMIT"
```

The runtime venv (patched SGLang + kernels) is **baked into the image** at
`/opt/pp`. It is downloaded, sha256-verified, relocated, and topped with the
pinned PyPI deps once at build time (from a revision-pinned mirror), so the
final image is self-contained: **no runtime download and no `HF_TOKEN` for the
runtime**, and every image tag carries an identical, frozen SGLang. Only the
(public) model weights are fetched at boot -- so a plain
`docker run ... submission` needs no secrets at all. At boot the entrypoint just
applies the checked-in SGLang patches (fast, in-place) and resolves the models.

### Prepare persistent storage

Mount persistent storage at the internal `/workspace` path. It holds the runtime,
models, caches, `test.csv`, `submission.csv`, and resumable search artifacts.
The host path is arbitrary; these examples use `$PWD/workspace`. Allow at least
200 GB for the checked-in default model pair and runtime.

Fetch the selected commit configuration, then edit any values needed for the
run:

```bash
mkdir -p "$PWD/workspace"
curl -fsSL \
  "https://raw.githubusercontent.com/hav4ik/imo-inference/$COMMIT/config.yaml" \
  -o "$PWD/workspace/config.yaml"
```

`config.yaml` is the base (8×H200, DFlash, selector **off**). For the LLM
final-solution selector and the 2× search width used in the `imo2026-*-2x`
experiments, start from `config-nii-2x.yaml` (deploy) / `config-nii-2x-step225.yaml`
in the repo root instead, or set `search.llm_selector: true` (+ `selection_*`
knobs) in your copy. See `evaluation/EXPERIMENTS.md` and `CHANGES_VS_UPSTREAM.md`.

`CONFIG` is mandatory. The container has no fallback configuration. It validates
the supplied YAML but never copies, rewrites, clamps, or overrides its values.
All model paths in the YAML are absolute container paths. Put custom target and
draft assets at the corresponding locations under the mounted storage. The
container downloads the checked-in default model pair only when the YAML uses
the default paths and those assets are missing.

Create `$PWD/workspace/test.csv` with exactly two lowercase columns:

```csv
id,problem
0,"First complete problem statement"
1,"Second complete problem statement"
```

IDs must be nonempty and unique. Quote fields containing commas or newlines. Do
not add answers, rubrics, reference solutions, or metadata columns.

### Generate submission.csv

```bash
docker run --rm --gpus all --ipc=host --shm-size=32g \
  -v "$PWD/workspace:/workspace" \
  -e CONFIG=/workspace/config.yaml \
  "$IMAGE" submission
```

The command installs the persistent runtime if needed, resolves the configured
models, applies the selected commit patches, starts and validates SGLang, and
processes input rows sequentially. It writes exactly these columns to
`$PWD/workspace/submission.csv`:

```csv
id,proof
```

The submission workflow does not call an external grader. Multiline proofs are
CSV-quoted. After every completed search round, the current problem row is
atomically replaced with the top-ranked cumulative-pool proof; the final
selection replaces it once more when the search completes.

## Configuration

The selected commit YAML is the complete runtime contract. Candidate labels
identify harness policy, not model identity; record the target and draft model
revisions separately when comparing model pairs.

The current `main` defaults are:

| Setting | Value |
|---|---|
| Hardware | 8 x NVIDIA H200 |
| Model mode | BF16 target and BF16 DFlash draft |
| Parallelism | TP2 x DP4 |
| Attention | FA3, page size 1, deterministic inference |
| Server context | 262,144 tokens |
| Server concurrency | 64 running requests per DP replica |
| Search concurrency | 96 requests cluster-wide |
| Search policy | 32 proofs, 16 verifications per proof, top 8, 4 refinements, up to 16 rounds |
| Sampling | temperature 1.0, top-p 0.95 |
| First output segment | 128,000 tokens |
| Solution continuation | 16,384 tokens |
| Verifier continuation | 16,384 tokens |

Users may change every YAML value. Validation retains type, range, schema, and
implementation compatibility checks, including:

```text
top_proofs * refinements_per_proof = proofs_per_round
analyses_per_refinement = refinements_per_proof
analyses_per_refinement <= min_valid_verifications <= verifications_per_proof
FA3: page_size=1 and deterministic_inference=true
FA4: page_size=128 and deterministic_inference=false
```

The configured server context is a total input-plus-output limit.

### Budget presets

The `config-model-{deploy,step225}-budget-{medium,high,xhigh}.yaml` configs are a
matrix that varies **only the search budget**. `refine_parents` (4) ×
`reviews_per_refine_parent` (3) — the training limit — and everything else (server
topology, sampling, the LLM selector) are held constant, so runs differ only by
compute. Pick one by name with `scheduler.sh` (or as the container `CONFIG`).

| preset | proofs_per_round | verifications_per_proof | top_proofs | refine_parents | reviews/parent | max_rounds |
|---|---|---|---|---|---|---|
| **medium** | 32 | 16 | 8 | 4 | 3 | 4 |
| **high** | 64 | 32 | 16 | 4 | 3 | 8 |
| **xhigh** | 128 | 64 | 32 | 4 | 3 | 8 |

- `medium` is the original run policy (`config-nii-r4`).
- `proofs_per_round` is both the round-1 prover count and the per-round refinement
  count; `top_proofs` is the pool refinement parents are stratified-sampled from.
- `refine_review_strategy` is `random_nonideal` (each refine parent is paired with 3
  reviews drawn from its `<1`-score verifications).
- `max_rounds` counts round 1 (generation): `4` = 1 gen + 3 refine, `8` = 1 gen + 7 refine.
- Two checkpoints (`deploy`, `step225`) × three budgets = the six configs.

## Resume and outputs

Search state is stored in `/workspace/submission_artifacts`. If a run stops
before its configured final round, `submission.csv` retains the top proof from
the latest completed round. Re-run the same
image, YAML, `test.csv`, and command to reuse completed work and retry missing or
failed work. For a different input set or policy, use a new directory:

```bash
-e ARTIFACTS_DIR=/workspace/submission_artifacts_candidate_2
```

The runner rejects mismatched inputs or configuration rather than silently
mixing runs.

## Other commands

All commands except `help` require `CONFIG`:

| Command | Purpose |
|---|---|
| `submission` | Start the server and generate `submission.csv` |
| `serve` | Start and validate only the configured SGLang server |
| `bootstrap` | Prepare the runtime and configured models without GPUs |
| `validate` | Validate an already running configured server |
| `shell` | Prepare the runtime and open a shell |
| `help` | Show entrypoint help |

The SGLang API has no application authentication. Do not publish its configured
port directly; use private networking or an authenticated reverse proxy.

## Troubleshooting

**`CONFIG is required`:** mount the YAML into the container and pass its absolute
container path with `-e CONFIG=/workspace/config.yaml`.

**Configured model is incomplete:** ensure each active model path contains
`config.json` and safetensor weights. Custom paths are never replaced or
downloaded automatically.

**CUDA device-count mismatch:** the number of visible GPUs must equal
`tensor_parallel_size * data_parallel_size` from the YAML.

**Resume input mismatch:** restore the exact image, YAML, and `test.csv`, or use a
new `ARTIFACTS_DIR`.

**Server validation reports missing DFlash markers:** inspect the complete log at
`/workspace/opd32b-eval.log` and confirm that the configured target, draft,
attention backend, and DFlash settings are compatible.
