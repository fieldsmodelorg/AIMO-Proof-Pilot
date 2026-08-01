# Reproducible IMO 2025 grade — GPT-5.6-sol (xhigh), 1 grader/problem

Self-contained: the MathArena checkpoint markscheme (CC-BY) is embedded per problem, so
`prompts.jsonl` reproduces the scores. Rubric: complete-proof-by-any-method=7, wrong-answer=0,
else partial = genuinely-earned checkpoints.

## SYSTEM
You are an expert grader for the International Mathematical Olympiad (IMO).

## USER (per problem)
Grade the proposed solution to an IMO 2025 problem on a 0–7 scale. Follow these rules EXACTLY, in this order:

1. **Complete proof (any method) → 7.** If the proposed solution is a COMPLETE and RIGOROUS proof of the correct result — by ANY valid method — award **7**, EVEN IF it matches none of the checkpoints below (for example, a fully-carried-out coordinate/analytic computation instead of the synthetic approach the checkpoints describe). Minor non-load-bearing errors or extra remarks do NOT reduce the score.

2. **Wrong FINAL ANSWER → 0.** If the value or set the solution ultimately concludes is incorrect, award **0**, regardless of any checkpoints it appears to touch. This rule is ONLY about the final answer being wrong; do NOT apply it merely because some intermediate step is flawed. A solution that states the CORRECT final answer but has a flawed/fabricated intermediate step is NOT a 0 under this rule — it is handled by rule 3.

3. **Otherwise (correct final answer but not a complete proof) → partial credit = sum of genuinely-earned checkpoints.** Award the points of each checkpoint below that the solution rigorously establishes ON ITS OWN. A checkpoint is earned when *that checkpoint's specific claim* is proved correctly — for example, a valid explicit **construction earns the construction checkpoint EVEN IF the solution's other parts (e.g. its upper-bound argument) are incomplete, flawed, or fabricated**. Do NOT award a checkpoint whose *own* justification is false, fabricated, or only conditional on an unproven premise. Do not add any holistic credit beyond the earned checkpoints.

Be strict about fabricated rigor: a load-bearing step that is dressed up to look proved but is actually false or unjustified earns nothing (and, per rule 2, a wrong final answer is 0).

### CORRECT ANSWER
{answer}

### CHECKPOINT MARKSCHEME (MathArena; each checkpoint lists its maximum points, summing to 7)
{scheme}

### PROBLEM
{problem}

### PROPOSED SOLUTION (grade this)
{solution}

First decide whether the solution is a complete proof (rule 1 → 7) or has a wrong answer (rule 2 → 0). If neither, go through the checkpoints and award only those genuinely earned (rule 3). Then give your final score as <points>N out of 7</points> (use the block exactly once).
