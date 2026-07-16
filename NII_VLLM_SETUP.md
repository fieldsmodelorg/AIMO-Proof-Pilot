# NII vLLM 0.25.1 setup

This runbook prepares the eight NII H200 nodes for the standalone multi-node
`evaluation/harness_vllm/run.py` pipeline. It is safe to execute while training is active because setup
uses CPU, network, and the shared `/tmp` filesystem only. Do not start a vLLM
server or run a CUDA/NCCL smoke until the training job has stopped.

## Observed NII runtime

The current SIF exposes the same environment on all eight nodes:

- Python 3.12.3 at `/usr/bin/python3`.
- PyTorch 2.11.0+cu130.
- vLLM 0.23.1 dev under the read-only user site.
- Eight H200 GPUs per node.
- A shared, writable `/tmp` mount.

The setup overlays vLLM 0.25.1 in a shared virtual environment rather than
changing the SIF or the existing user site. Rank 0 performs the install and
model download once; the other ranks wait for readiness markers and then run
their own import check.

## Install and download

Submit the checked-in setup script to all nodes through the durable GitHub
operator. It preserves `/app/entrypoint.sh`, operator processes, relay daemons,
and the active training process.

```bash
python ../aimo-proof-pilot/scripts/operator_client.py \
  --backend github \
  --repo nguyen599/command \
  --nodes 0,1,2,3,4,5,6,7 \
  send --file scripts/setup_nii_vllm.sh
```

Defaults:

```text
runtime checkout: /tmp/aimo-proof-pilot-inference-runtime/repo
venv:             /tmp/aimo-proof-pilot-inference-runtime/venv-vllm-0.25.1
target model:     /tmp/models/olmo3-opd-sft-425
vLLM model view:  /tmp/models/olmo3-opd-sft-425-vllm
draft model:      /tmp/models/dflash-32b-draft-v2test-phaseL
```

The `-vllm` directory is a zero-copy view. All weight files are symlinks to the
downloaded checkpoint; only `config.json` is copied and changes
`model_type=olmo3_sink` to `model_type=olmo3`. The architecture remains
`Olmo3SinkForCausalLM`, so the local vLLM plugin still owns model execution.

Override defaults through environment variables at the start of the submitted
script, for example `NII_DOWNLOAD_TARGET_MODEL=0` to validate an existing
runtime without downloading the target checkpoint.

The setup does not place tokens in commands or logs. It uses the node's cached
Hugging Face authentication and sets `HF_XET_HIGH_PERFORMANCE=0` for this
checkpoint download.

## Safe eight-node smoke

While training is active, test only the controller path. This imports vLLM and
the OLMo3Sink plugin, creates the same short-lived Gloo group as the vLLM harness,
validates the shared startup records, and exits. It never loads model weights
and never creates a CUDA tensor.

Choose one new run ID and submit the command to every node:

```bash
SMOKE_ID="nii-vllm0251-$(date -u +%Y%m%dT%H%M%SZ)"
python ../aimo-proof-pilot/scripts/operator_client.py \
  --backend github \
  --repo nguyen599/command \
  --nodes 0,1,2,3,4,5,6,7 \
  send --command "cd /tmp/aimo-proof-pilot-inference-runtime/repo && \
NII_SMOKE_RUN_ID=$SMOKE_ID bash scripts/smoke_nii_multinode.sh"
```

Every node must print one JSON object with `"status": "ok"`, the same run ID,
`world_size: 8`, and its own candidate assignment. Rank 0 should report
candidate IDs `[0, 8]`; rank 7 should report `[7]`.

This smoke validates inter-node controller communication, not vLLM GPU worker
communication. The production design starts one independent local vLLM server
per node (`TP=2, DP=4`); vLLM does not form a cross-node tensor-parallel group.

## Validated NII result

The setup was validated on all eight H200 nodes on 2026-07-16 while the existing
SFT job remained active:

- vLLM 0.25.1 and all three OLMo3Sink/DFlash plugin architectures imported on
  every node from the shared venv.
- `nguyen599/olmo3-opd-sft-425` downloaded to `/tmp/models`, and all 14
  safetensor shards passed an open/read validation.
- Controller smoke `nii-vllm0251-20260715T205900Z` completed on ranks 0-7 with
  `world_size=8`; rank 0 received candidate IDs `[0, 8]` and rank 7 received
  `[7]`.
- GPU memory stayed in the pre-existing training range (about 102.7 GiB per
  H200). No vLLM engine or model weights were loaded by the smoke.

The vLLM patch installer intentionally preserves the venv `bin/python` symlink.
Resolving that symlink to `/usr/bin/python3` would bypass the venv and patch the
read-only image's older vLLM installation instead.

## Production launch after training

After confirming that the training processes have exited and all GPUs are free,
use the shared venv and paths with the launch contract in
[`RUN_PY_MULTINODE.md`](RUN_PY_MULTINODE.md):

```bash
export PATH=/tmp/aimo-proof-pilot-inference-runtime/venv-vllm-0.25.1/bin:$PATH
export VLLM_PLUGINS=olmo3_sink
export AIMO_MODEL_PATH=/tmp/models/olmo3-opd-sft-425-vllm
export AIMO_DFLASH_MODEL_PATH=/tmp/models/dflash-32b-draft-v2test-phaseL
```

Use a new `AIMO_DISTRIBUTED_RUN_ID` for each launch. Do not wrap the harness in
`torchrun`; each node runs one controller, and each controller starts its own
local TP2/DP4 vLLM server.

## Verification and cleanup

Inspect the shared setup marker:

```bash
cat /tmp/aimo-proof-pilot-inference-runtime/markers/setup-*-vllm-0.25.1-olmo3-opd-sft-425.ready
```

Run a single-node import check without loading weights:

```bash
VLLM_PLUGINS=olmo3_sink \
  /tmp/aimo-proof-pilot-inference-runtime/venv-vllm-0.25.1/bin/python \
  -c 'import vllm; print(vllm.__version__, vllm.__file__)'
```

Runtime files can be removed after inference is complete:

```bash
rm -rf /tmp/aimo-proof-pilot-inference-runtime
```

Do not remove `/tmp/models` or active training directories.
