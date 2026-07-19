# Experiment: `imo2026-step225-r4` (vu)

**Owner:** vu (node0) · **Started:** 2026-07-19 (UTC) · **Status:** 🟢 running · **Hardware:** 8×H200 (NII node0)

Checkpoint-selection run #2. **Identical setup to
[`vu-imo2026-deploy-r4.md`](vu-imo2026-deploy-r4.md)** (same harness, same search
budget, same LaTeX IMO-2026 problems, same rubric grading) — the **only** variable
is the model checkpoint: **`opd-32b-bf16-step-225`** instead of `opd-32b-deploy`.
Reason: `step-225` is the training checkpoint just before the step-250 gradient
spike; this run tests whether it proves better/worse than the deployed model.

## TL;DR (deltas vs the deploy baseline only)

| | |
|---|---|
| Model (target) | `fieldsmodelorg/Olmo-3.1-32B-Think-OPD-IMO` → **`opd-32b-bf16-step-225`** (bf16) |
| Draft (DFlash) | shared — `dflash-32b-draft-v2test-phaseL` |
| Config | `config-nii-step225-r4.yaml` (= `config-nii-r4.yaml` with `bf16_target` + `run_name` changed) |
| Traces | `imo2026-challenge/chankhavu-imo-reasoning-traces` → **`imo2026-step225-r4/`** |
| Outputs (node0) | `submission.csv` → `/tmp/chankhavu/out/imo2026-step225-r4/`; artifacts → `/tmp/chankhavu/artifacts/imo2026-step225-r4/` |
| Everything else | **unchanged** from `imo2026-deploy-r4` (tp2·dp4, bf16 KV, fa3, max_rounds 4, 32×16, temp 1.0, seed 0, all 4 harness knobs) |

## Launch (node0)
```bash
# server (job name sglang225 to avoid collision with a stale 'sglang' job entry)
opd-run sglang225 bash -c 'source /tmp/chankhavu/venvs/infervenv/.runtime/activate-env.sh && python /tmp/chankhavu/imo-inference/evaluation/harness/launch_server.py --config /tmp/chankhavu/imo-inference/config-nii-step225-r4.yaml'
# wait for /health=200, then:
opd-run submit225 bash -c 'export HF_TOKEN="$(hf auth token 2>/dev/null)"; source /tmp/chankhavu/venvs/infervenv/.runtime/activate-env.sh && python /tmp/chankhavu/imo-inference/evaluation/harness/run_submission.py --config /tmp/chankhavu/imo-inference/config-nii-step225-r4.yaml --input /tmp/chankhavu/imo-inference/evaluation/data/imo2026-latex-test.csv --output /tmp/chankhavu/out/imo2026-step225-r4/submission.csv --artifacts-dir /tmp/chankhavu/artifacts/imo2026-step225-r4'
```

## Grading (when finished)
Same as deploy: fetch each `problems/<row>/final.json`, grade against the
`chankhavu/IMO2026-GPT-5.6-Sol-Markscheme` rubric with a 4× opus-4.8/xhigh panel,
average. Compare per-problem and total against the deploy baseline (**19.25/42**;
P1=7, P4=7, P5=5.25, P2=P3=P6=0).

## Results — *pending*
| P1 | P2 | P3 | P4 | P5 | P6 | Total |
|---|---|---|---|---|---|---|
| — | — | — | — | — | — | **/42** |

## Notes
- The deploy baseline's mid-run SGLang crash was **not** the model/config — it was
  a `py-spy dump --native` on the scheduler tripping the watchdog. Resume is now
  self-healing (poisoned-record recovery baked into `CallStore`), so a transient
  crash here needs only: restart `sglang225` → rerun the same `submit225` command.
- Leak-audit conclusion carries over: `step-225` is from the same pre-July-2026
  training pipeline (repo pushed July 9) on the same held-out 2026 problems.
