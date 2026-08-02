# IMO 2026 model submissions — graded artefacts

Model-generated solutions to IMO 2026 Problems 1–6, independently graded. This
folder collects the graded artefacts for public sharing.

## Contents

```
solutions/   # per-problem solution text, verbatim raw model output
             #   <submission>/<submission>_problem_<n>.txt
pdfs/        # typeset PDF of each full submission
raw/         # the original submission CSVs (id, proof) as downloaded
scores.csv   # machine-readable per-problem scores (with uncertainty notes)
README.md    # this file
```

## Submissions

| Submission | Model / setting | Problems | Config | Source |
| --- | --- | --- | --- | --- |
| `imo2026-deploy-budget-high-tournament` | Proof Pilot (high budget) | 1–6 | [deploy high](../config-model-deploy-budget-high.yaml) | [submission.csv](https://huggingface.co/datasets/imo2026-challenge/chankhavu-imo-reasoning-traces/blob/main/imo2026-deploy-budget-high-tournament/submission.csv) |
| `imo2026-step225-budget-high-tournament` | IMO step225 (high budget) | 1–6 | [step225 high](../config-model-step225-budget-high.yaml) | [submission.csv](https://huggingface.co/datasets/imo2026-challenge/chankhavu-imo-reasoning-traces/blob/main/imo2026-step225-budget-high-tournament/submission.csv) |
| `step225_run2` | IMO step225 (xhigh budget, rerun) | 1, 4, 5 | [step225 xhigh](../config-model-step225-budget-xhigh.yaml) | [submission.csv](https://huggingface.co/datasets/imo2026-challenge/chankhavu-imo-reasoning-traces/blob/main/imo2026-step225-budget-xhigh-P1P4P5/submission.csv) |
| `step225_run3` | IMO step225 (xhigh budget, rerun) | 5 | [step225 xhigh](../config-model-step225-budget-xhigh.yaml) | [submission.csv](https://huggingface.co/datasets/imo2026-challenge/chankhavu-imo-reasoning-traces/blob/main/imo2026-step225-budget-xhigh-P5/submission.csv) |

## Grading methodology

The submissions have been graded according to broad IMO standards. We have not
had access to the official IMO markschemes, so we cannot grade against them.
Where this creates uncertainty, it is flagged explicitly below and in
`scores.csv`. The grading was performed by a former IMO medalist.

The IMO 2026 medal boundaries were: **Bronze 16, Silver 23, Gold 29** (out
of 42).

## Scores

| Model | P1 | P2 | P3 | P4 | P5 | P6 | Total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Proof Pilot (high) | 7 | 0 | 0 | 7 | 5\* | 0† | **19** |
| IMO step225 (high) | 7 | 0 | 0 | 7 | 7 | 0† | **21** |

\* **P5, Proof Pilot** — defaulted to 5 in the total. Without access to the
official markscheme this score is uncertain: it could reasonably be as low as 2,
though it is very unlikely to be lower given the score distribution on the
actual IMO. Even at 2, the total (16) would still be a Bronze-medal score.

† **P6** — both submissions are probable 0s, but each contains some useful
work, so there is a small chance either could score 1.

Plausible ranges: Proof Pilot 16–20, IMO step225 21–22. Both reach a
Bronze-medal score, with IMO step225 close to (but not reaching) Silver.

Supplementary xhigh reruns (partial submissions, so no meaningful total):

| Submission | P1 | P4 | P5 |
| --- | --- | --- | --- |
| `step225_run2` | 7 | 7 | 7 |
| `step225_run3` | — | — | 7 |

## Per-problem commentary

- **P1** — Both main submissions are complete solutions: 7 each.
- **P2** — Both score 0. Proof Pilot mis-converts one of the angle relations
  into complex numbers at the outset. IMO step225 is correct for longer, but the
  algebra simplifying \(BC - AD = 0\) is invalid. Computational approaches to
  geometry problems are very rarely awarded partial credit unless the
  intermediate results are interpreted synthetically (i.e. back in terms of the
  diagram rather than pure algebra), so both would certainly score 0.
- **P3** — Both score 0. Neither submission goes beyond the \(n = 1\) case;
  both give the wrong answer, with no progress toward the optimal bound. The
  \(n = 1\) case is not credit-worthy at the IMO on a hard problem.
- **P4** — Both are complete solutions: 7 each. The IMO step225 write-up is
  hard to follow in places, but the IMO applies no style penalties or negative
  marking.
- **P5** — The IMO step225 solution is complete: 7. The Proof Pilot solution
  fails to handle the possibility \(f(x) - x \in \{0, c\}\) for some constant
  \(c \ge 0\), and its Case 1 argument is incorrect (the claimed inequality
  fails, e.g., for \(a = 10\), \(b = 2\), \(c = 1\)). Without the official
  markscheme the penalty for this is uncertain: the score would very likely be
  in the range 2–5, with 5 the most likely.
- **P6** — Both submissions contain fundamental errors and are incomplete,
  though each has some useful ideas (particularly IMO step225). The bar for a
  partial mark on a hard problem is usually reasonably high, but 72 contestants
  earned one this year, so there is a small chance of a 1. The most likely mark
  for both is 0.
- **xhigh reruns** — `step225_run2` (P1, P4, P5) and `step225_run3` (P5) were
  also reviewed: all are complete solutions, 7 each.

## Reproducibility

The PDFs in `pdfs/` were typeset from the raw CSVs (Markdown embedding LaTeX
math) via pandoc and `pdflatex`. The per-problem files in `solutions/` are the
verbatim raw model output, extracted unchanged from the `proof` column of the
CSVs in `raw/`.
