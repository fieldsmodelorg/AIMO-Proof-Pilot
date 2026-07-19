# Experiment: `imo2026-step125-r4` (vu)

**Owner:** vu · **Node:** **node1 (hnode061)** · **Started:** 2026-07-19 (UTC) · **Status:** 🟢 running · **Hardware:** 8×H200

Checkpoint-selection run #3, running **in parallel** with `imo2026-step225-r4`
(node0). **Identical setup to
[`vu-imo2026-deploy-r4.md`](vu-imo2026-deploy-r4.md)** — same harness, search
budget, LaTeX IMO-2026 problems, and rubric grading. The **only** variable is the
model checkpoint: **`opd-32b-bf16-step-125`** (the earliest of the three step
checkpoints — a "how early is good enough?" data point).

## TL;DR (deltas vs deploy baseline only)

| | |
|---|---|
| Model (target) | `fieldsmodelorg/Olmo-3.1-32B-Think-OPD-IMO` → **`opd-32b-bf16-step-125`** (bf16) |
| Node | **node1 (hnode061)** — free `bogo` node, team-coordinated use |
| Config | `config-nii-step125-r4.yaml` |
| Traces | `imo2026-challenge/chankhavu-imo-reasoning-traces` → **`imo2026-step125-r4/`** |
| Outputs | `/tmp/chankhavu/{out,artifacts}/imo2026-step125-r4/` (shared FS) |
| Jobs (node1) | server `sglang125`, submit `submit125` |
| Everything else | **unchanged** from `imo2026-deploy-r4` |

**Shared filesystem:** node0 and node1 share `/tmp/chankhavu` (venv, models, repo,
configs), so no reinstall/redownload was needed — just `git pull` + launch on
node1. The two runs write to **separate** trace subfolders and artifacts dirs, so
they don't collide.

## Launch (node1)
```bash
cd /tmp/chankhavu/imo-inference && git pull
opd-run sglang125 bash -c 'source /tmp/chankhavu/venvs/infervenv/.runtime/activate-env.sh && python /tmp/chankhavu/imo-inference/evaluation/harness/launch_server.py --config /tmp/chankhavu/imo-inference/config-nii-step125-r4.yaml'
# wait /health=200, then:
opd-run submit125 bash -c 'export HF_TOKEN="$(hf auth token 2>/dev/null)"; source /tmp/chankhavu/venvs/infervenv/.runtime/activate-env.sh && python /tmp/chankhavu/imo-inference/evaluation/harness/run_submission.py --config /tmp/chankhavu/imo-inference/config-nii-step125-r4.yaml --input /tmp/chankhavu/imo-inference/evaluation/data/imo2026-latex-test.csv --output /tmp/chankhavu/out/imo2026-step125-r4/submission.csv --artifacts-dir /tmp/chankhavu/artifacts/imo2026-step125-r4'
```

## Grading (when finished)
Same 4× opus-4.8/xhigh panel vs the `chankhavu/IMO2026-GPT-5.6-Sol-Markscheme`
rubric, averaged. Compare per-problem + total against deploy (**19.25/42**) and
step-225.

## Results — *pending*
| P1 | P2 | P3 | P4 | P5 | P6 | Total |
|---|---|---|---|---|---|---|
| — | — | — | — | — | — | **/42** |

## Notes
- If sglang125 crashes: **clean-stop first** — `pkill -9 -f sglang.launch_server`
  on node1 (killing only the opd-run wrapper leaves the main server orphaned and
  holding port 30000), then restart + rerun the same `submit125` command. Resume
  is self-healing (poisoned-record recovery in `CallStore`).
