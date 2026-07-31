# IMO 2025 — step225 (high budget)

Evaluation of the Proof-Pilot **step225** checkpoint (high inference budget) on the six
**IMO 2025** problems, each graded 0–7 against the
[MathArena](https://matharena.ai) `imo_2025` checkpoint markscheme.

Inference was run with the **step225 high** production config
([`config-model-step225-budget-high.yaml`](../../config-model-step225-budget-high.yaml)).

## Headline

| Problem | Majority /7 | Mean /7 | Grader distribution |
|---|--:|--:|---|
| P1 | **4** | 3.75 | `3`×2 `4`×6 |
| P2 | **2** | 2.00 | `2`×8 |
| P3 | **2** | 2.00 | `2`×8 |
| P4 | **7** | 7.00 | `7`×8 |
| P5 | **7** | 7.00 | `7`×8 |
| P6 | **1** | 1.00 | `1`×8 |
| **Total** | **23 / 42** | 22.75 / 42 | — |

**Majority-vote total: 23 / 42 (54.8%)** (arithmetic mean: 22.75/42).

The 2025 IMO medal boundaries were Bronze 19 / Silver 28 / Gold 35, so **23 is a
Bronze-medal score**.

## Grading methodology

Graded with **GPT-5.6-sol** as the autograder against the MathArena `imo_2025`
markscheme (see `grading/prompt_template.md`):

- **Checkpoint scheme, scale 0–7.** Each problem's grading scheme is a set of
  checkpoints with point values that sum to 7; the grader awards points per checkpoint
  and sums. This is MathArena's grading method, not a holistic 0–7 judgement.
- The grader is given the **problem, the model's proof, and the per-problem grading
  scheme**; it emits per-checkpoint analysis ending in a single
  `<points>N out of 7</points>` block.
- **8 graders per problem**, aggregated by **majority vote** (modal score). Reasoning
  effort **high**.

**Grader stability.** The autograder is near-deterministic: 5 of 6 problems are
unanimous across all 8 judgments; only P1 is split (six of eight gave 4). The
arithmetic-mean total (22.75/42) and majority-vote total (23/42) agree to
within rounding. This measures grader *self-consistency*, not correctness against a
human.

## Contents

- `solutions.csv` — the 6 model proofs with their majority and mean scores
  (`Problem ID, score_majority, score_mean_8, proof`).
- `grading/SUMMARY.md` — the table above plus per-problem grader distributions.
- `grading/scores.json` — machine-readable aggregates + per-problem scores and
  distributions.
- `grading/prompt_template.md` — the exact system + user prompt template and run config.
- `grading/prompts.jsonl` — one line per problem (`{problem_id, messages}`): the exact
  `[system, user]` input sent to the grader, embedding the problem, the grading scheme,
  and the model's solution (reproducibility).

The problems and grading schemes are from
[MathArena/imo_2025](https://huggingface.co/datasets/MathArena/imo_2025) (see the dataset
page for licensing).

## Caveats

- Numbers are the **GPT-5.6-sol autograder**, not verified human grades.
- One rollout per problem (step225, high budget); generation variance is not captured.
