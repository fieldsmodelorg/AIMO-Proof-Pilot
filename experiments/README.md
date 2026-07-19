# vu's IMO-2026 experiments — index

Checkpoint-selection campaign: run the OPD-32B generate–verify–refine harness
(`hav4ik/imo-inference` @ `docker/container-improvements`) on the 6 **IMO-2026**
problems (LaTeX), grade each against the `chankhavu/IMO2026-GPT-5.6-Sol-Markscheme`
rubric, and compare checkpoints. Reference bar: ycchen's original OPD = **12.75/42**.

## The "why" (read first)
[`vu-harness-design-rationale.md`](vu-harness-design-rationale.md) — the prompting
+ refinement-topology changes vs Geremie's fork, gold-aligned, with evidence.

## Runs

| Experiment | Checkpoint | Node | Status | Score (markscheme) |
|---|---|---|---|---|
| [`vu-imo2026-deploy-r4`](vu-imo2026-deploy-r4.md) | `opd-32b-deploy` | node0 | ✅ done | **19.25 / 42** |
| [`vu-imo2026-step225-r4`](vu-imo2026-step225-r4.md) | `opd-32b-bf16-step-225` | node0 | 🟢 running | pending |
| [`vu-imo2026-step125-r4`](vu-imo2026-step125-r4.md) | `opd-32b-bf16-step-125` | node1 | 🟢 running | pending |
| (maybe) step-250 | `opd-32b-bf16-step-250` | — | not started | — |

step-225 and step-125 run **in parallel** (nodes share `/tmp/chankhavu`, so each
just needed `git pull` + launch; separate trace subfolders per run).

### Deploy baseline detail (19.25/42)
| P1 | P2 | P3 | P4 | P5 | P6 |
|---|---|---|---|---|---|
| **7** | 0 | 0 | **7** | **5.25** | 0 |
Two real full solves (P1, P4), a strong partial (P5, Case-2 gap), three wrong.
**Past the 12.75 bar** on genuinely held-out problems.

## How grading works (auditable)
Per problem, a **panel of 4 independent opus-4.8 sub-agents at xhigh reasoning**
grades the model's `final.json` proof against the dataset's exact `grading_scheme`
(byte-identical), verifying the crux themselves; the 4 scores are averaged.
Everything the solver sees is the problem statement only — reference solutions &
markschemes are judge-side (contestant regime).

## Leak audit — clean (no IMO-2026 contamination, high confidence)
A 3-angle opus-xhigh audit confirmed the model never saw IMO-2026 problems/
solutions/markschemes: training IMO data is `imo_data_1959_2024.csv` (no 2026);
all base/teacher cutoffs predate the July 15–16 2026 papers (training repo pushed
July 9); and the P1/P4 reasoning traces show genuine derivation (P4 derives the
*wrong* answer, then self-corrects — impossible under recall).

## Where things live
- Harness + configs: `hav4ik/imo-inference` @ `docker/container-improvements`
  (`config-nii-{r4,step225-r4,step125-r4}.yaml`, `evaluation/data/imo2026-latex-test.csv`).
- Traces: `imo2026-challenge/chankhavu-imo-reasoning-traces/<run_name>/` — the full
  artifacts tree per run (`calls.jsonl`, `proofs/`, `rounds/`, `final.json`,
  `submission.csv`).
