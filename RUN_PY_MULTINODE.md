# Multi-node vLLM inference

`evaluation/harness_vllm/run.py` supports one controller process per node. Each
controller starts an independent local vLLM server, and candidate pipelines are split across nodes
by their global candidate ID.

For 14 candidates and eight nodes, assignments are:

| Node rank | Candidate IDs |
|---|---|
| 0 | 0, 8 |
| 1 | 1, 9 |
| 2 | 2, 10 |
| 3 | 3, 11 |
| 4 | 4, 12 |
| 5 | 5, 13 |
| 6 | 6 |
| 7 | 7 |

Each candidate remains a complete local pipeline, including proof,
verification, meta-verification, and refinement calls. Rank 0 merges candidates
in global ID order, runs final selection, and writes the submission. Other
ranks never write the final CSV.

## Launch

Run the same command once on every node. Set `GLOBAL_RANK` to `0` through `7`;
all other values must match. Do not export `RANK` and do not wrap this command
in `torchrun`: vLLM owns the local GPU worker processes.

```bash
export GLOBAL_RANK="${GLOBAL_RANK:?set the node rank from 0 through 7}"
export WORLD_SIZE=8
export MASTER_ADDR="${MASTER_ADDR:?set the rank-0 host or IP}"
export MASTER_PORT="${MASTER_PORT:-29500}"
unset RANK LOCAL_RANK LOCAL_WORLD_SIZE

export NVIDIA_VISIBLE_DEVICES=all
export NCCL_IB_HCA=mlx5_ibn1,mlx5_ibn2,mlx5_ibn3,mlx5_ibn4,mlx5_ibn5,mlx5_ibn6,mlx5_ibn7,mlx5_ibn8
export NCCL_IB_PCI_RELAXED_ORDERING=1
export NCCL_CROSS_NIC=1
export AIMO_NUM_GPUS=8
export AIMO_GPUS=0,1,2,3,4,5,6,7
export AIMO_TENSOR_PARALLEL_SIZE=2
export AIMO_DATA_PARALLEL_SIZE=4
export AIMO_REQUESTS_PER_GPU=32

# Use the same unique ID and shared writable directory on all nodes.
export AIMO_DISTRIBUTED_RUN_ID="imo-2025-final-v1"
export AIMO_DISTRIBUTED_ROOT=/tmp/aimo-proof-pilot-inference/distributed

export AIMO_MODEL_PATH=/tmp/models/olmo3-opd-sft-200
export AIMO_DFLASH_MODEL_PATH=/tmp/models/dflash-32b-draft-v2test-phaseL
export AIMO_INPUT_PATH=/tmp/aimo-proof-pilot-inference/test.csv

# In distributed mode, omitting these keeps all generated files under /tmp.
unset AIMO_LOGDIR AIMO_OUTPUT_PATH

export TMP=/tmp
export TMPDIR=/tmp
export HF_HOME=/tmp/hf_home
export HUGGINGFACE_HUB_CACHE=/tmp/hf_cache
export HF_HUB_CACHE=/tmp/hf_cache
export TRANSFORMERS_CACHE=/tmp/hf_cache
export XDG_CACHE_HOME=/tmp/xdg_cache
export HF_XET_CACHE=/tmp/hf_xet
export HF_HUB_DISABLE_XET=1
mkdir -p \
  /tmp/hf_home \
  /tmp/hf_cache \
  /tmp/xdg_cache/huggingface/xet/logs \
  /tmp/hf_xet

python -m evaluation.harness_vllm.run
```

`max_concurrent_requests` defaults to `AIMO_REQUESTS_PER_GPU` multiplied by
the selected local GPU count. The example therefore allows 256 local scheduler
requests per node. Set `AIMO_MAX_CONCURRENT_REQUESTS` to a positive integer to
override the computed value. This scheduler limit is separate from vLLM's
`max_num_seqs` execution limit, so excess requests wait in the local queue.

The initial Gloo group only exchanges the run ID and validates that all nodes
have the same inference configuration. It is destroyed before local vLLM
servers start. External rank and rendezvous variables are removed from each
vLLM child environment, so the local `TP=2, DP=4` server cannot accidentally
join the eight-node controller world.

`AIMO_DISTRIBUTED_ROOT` must resolve to the same shared filesystem on every
node. Startup validation fails before inference if rank 0 cannot read every
rank's marker.

## Outputs

With the example run ID, the shared files are:

```text
/tmp/aimo-proof-pilot-inference/distributed/runs/imo-2025-final-v1/
  manifest.json
  submission.csv
  startup/
  problems/
  logs/rank_0000/run.log
  logs/rank_0000/vllm_server_0.log
  logs/rank_0001/run.log
  ...
```

Rank payloads are written atomically under `problems/`. A rank failure is
published under `errors/`, and waiting ranks abort instead of silently
producing a partial candidate set.

Use a new `AIMO_DISTRIBUTED_RUN_ID` for every launch. To intentionally replace
an existing run directory, set `AIMO_DISTRIBUTED_OVERWRITE=1` on every node.
The default wait limit is 48 hours; override it with
`AIMO_DISTRIBUTED_TIMEOUT_SECONDS` when needed.
