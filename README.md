# AIMO Proof Pilot Inference

This repository packages the generate-verify-refine proof harness as a Docker
image. The submission path reads `test.csv`, runs the selected harness, and
writes `submission.csv` without calling an external grader. The checked-in
configuration uses eight H200 GPUs as four TP2 replicas, BF16 target and draft
weights, DFlash speculative decoding, and FlashAttention 3.

## Docker usage

### Select the harness commit

Every pushed commit receives an immutable `sha-<7-character-commit>` image tag.
Set `COMMIT` to a full commit whose container workflow completed successfully:

```bash
export COMMIT=REPLACE_WITH_FULL_COMMIT_SHA
export IMAGE=ghcr.io/bogoconic1/aimo-proof-pilot-inference:sha-${COMMIT:0:7}

docker pull "$IMAGE"
test "$(docker image inspect "$IMAGE" \
  --format "{{ index .Config.Labels \"org.opencontainers.image.revision\" }}")" = "$COMMIT"
```

The image and runtime dataset are public. No registry, GitHub, Kaggle, OpenAI,
or other credentials are required for submission generation.

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
  "https://raw.githubusercontent.com/bogoconic1/aimo-proof-pilot-inference/$COMMIT/config.yaml" \
  -o "$PWD/workspace/config.yaml"
```

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
