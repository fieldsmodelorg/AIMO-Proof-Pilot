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
| [`vu-imo2026-deploy-r4`](vu-imo2026-deploy-r4.md) | `opd-32b-deploy` | node0 | ✅ done | 19.25 / 42 |
| [`vu-imo2026-step225-r4`](vu-imo2026-step225-r4.md) | `opd-32b-bf16-step-225` | node0 | ✅ done (P6 crashed→0) | **🏆 21.0 / 42** |
| [`vu-imo2026-step125-r4`](vu-imo2026-step125-r4.md) | `opd-32b-bf16-step-125` | node1 | ✅ done | 20.0 / 42 |
| (maybe) step-250 | `opd-32b-bf16-step-250` | — | not run | — |

**Result — checkpoint selection: `step-225` wins (21.0).** All three beat ycchen's
12.75 bar. Per-problem, the *entire* spread is **P5**: both step checkpoints close
deploy's Case-2 gap (deploy 5.25 → step-125 6.0 → step-225 7.0). P1/P4 are unanimous
full solves on every checkpoint; P2/P3/P6 are 0 on every checkpoint.

| checkpoint | P1 | P2 | P3 | P4 | P5 | P6 | **Total** |
|---|---|---|---|---|---|---|---|
| deploy | 7 | 0 | 0 | 7 | 5.25 | 0 | **19.25** |
| step-125 | 7 | 0 | 0 | 7 | 6.0 | 0 | **20.0** |
| **step-225** | 7 | 0 | 0 | 7 | **7.0**\* | 0† | **21.0** |

\* step-225 P5: clean 4-grader panel = 7.0; pooled over 8 graders (one dissent at 5.5) = 6.81 — either way > deploy/step-125.
† step-225 P6 **crashed mid-run** (sglang watchdog, at 5/6) and its P6 never finalized; recorded **0** by strong inference (both other checkpoints scored P6=0; P6 is effectively hopeless; step-225's P6 self-score was only ~0.3 over its 3 completed rounds). The ranking holds regardless of P6. Optional clean re-run of just P6 is pending relay recovery.

step-225 and step-125 ran **in parallel** (nodes share `/tmp/chankhavu`, so each
just needed `git pull` + launch; separate trace subfolders per run).

## Trace analysis (rollout health, all 3 runs)
Script `analyze_calls_2026.py` over all 18 (run×problem) `calls.jsonl`. **No bugs:**
0 errors (1 transient at the step-225 crash), verifier coverage = full **16/16** on
every proof that parses, all verifications `accepted`. **Truncation is confined to
P3/P6:** P1/P2/P4/P5 essentially never hit the 128k completion cap; on **P6 ~10–20%
of generations truncate** (`finish_reason=length`) → invalid XML → 0 verifications
(exact 1:1 chain — so "missing verifier" = truncated proofs correctly discarded, not
a bug). **Low checkpoint sensitivity** (P1 ≈ 21k tokens on all three; step-125
marginally most verbose). Early-stop works as designed (P1 stops after round 1; P5
step-checkpoints stop at round 3 with self=1.0 vs deploy running all 4 at 0.94). Only
suggested lever: **raise the 128k cap on P3/P6** to recover truncated-and-discarded
proofs.

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
