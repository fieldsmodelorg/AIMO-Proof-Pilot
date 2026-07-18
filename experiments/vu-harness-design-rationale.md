# Harness design rationale — prompting & refinement vs Geremie's fork (vu)

This explains the *why* behind the changes in my harness fork
(`hav4ik/imo-inference` @ `docker/container-improvements`) relative to Geremie's
upstream (`bogoconic1/aimo-proof-pilot-inference`). It pairs with the run writeup
[`vu-imo2026-deploy-r4.md`](vu-imo2026-deploy-r4.md).

## Thesis

The OPD-32B model was distilled/trained against **Yi-Chia Chen's (ycchen) Kaggle
"gold" pipeline**, not against Geremie's fork. Geremie's fork simplified several
of gold's prompting and refinement choices. **My changes move those back toward
gold** (the model's actual training distribution), plus fix two blatant parser
bugs. Everything is a config knob **defaulting to gold**, and I left Geremie's
selection/ranking backbone untouched — so a run is a clean test of "gold-aligned
harness vs Geremie's, same model, same budget."

Three reference points throughout:
- **Gold** = ycchen Kaggle pipeline (`proof_agent/parser.py`, `v2/pool_loop.py`) — what the model was tuned against.
- **Geremie** = `bogoconic1` upstream fork.
- **Ours** = this fork; each change is knob-gated, default = gold.

## 1. Prompting differences

### 1a. Verifier sees the prover's self-evaluation — KEEP (no change)
- **Gold:** feeds the candidate's `<self_evaluation>` *text* into the verifier prompt (`pool_loop.py:177`), because the verifier was **trained** with it (`opd_v2 build_verify`). In-distribution.
- **Geremie:** also feeds it. **Ours:** also feeds it (`verifier_sees_self_evaluation: true`).
- **Why it's a knob anyway:** so we can test the anchoring hypothesis (does the verifier lean on the prover's self-assessment?). Setting it false blanks the field — but that's an *off-distribution* verifier prompt, so default stays true.

### 1b. Refiner does NOT see the parent's self-evaluation — CHANGED (drop it)
- **Gold (inference):** **drops** it from the refine bundle (`pool_loop.py:196`, `with_self_eval=False`), with an explicit code comment: *"WITHOUT prover self-eval (unreliable ~92% self-score 1)."* The prover grades itself "1" ~92% of the time → it's noise for synthesis and just inflates context.
- **Geremie:** **includes** it in the refiner. **Ours:** drops it (`refiner_sees_self_evaluation: false`), matching gold's inference.
- **Subtlety worth knowing:** gold's *training* actually includes the parent self-eval in the refine bundle; gold's *Kaggle inference* drops it. So "false" is a deliberate, gold-validated train/inference split — the mirror image of the verifier (1a), where gold's inference *keeps* self-eval. This is not an oversight; it's exactly how gold runs.
- This only changes the refiner's **input**. The refiner still emits its own `<solution>/<self_evaluation>/<score>`, which feed its verification and ranking as usual.

### 1c. Lenient, search-based parsing — CHANGED (relax toward gold)
- **Geremie:** strict whole-document `fullmatch` — the entire output must be exactly `<solution>…</solution><self_evaluation>…</self_evaluation><score>…</score>`, case-sensitive, non-empty fields, ends at `</score>`.
- **Gold:** *extract, don't validate* — every field pulled with `re.search(..., IGNORECASE)`; admits a proof on `finish_reason != "length" and len(solution) > 500`; tolerates preamble/trailing text; **recovers a missing `</solution>`** (gold's comment: *"this model systematically OMITS `</solution>`"*).
- **Ours (`lenient_parsing: true`):** gold's behavior — recover missing `</solution>`, tolerate surrounding text, `IGNORECASE` tags, allow empty self-eval/suggestions.
- **Why it matters — measured on Geremie's own IMO-2025 runs:** of **498** cleanly-finished generations, strict admits 487 (97.8%), lenient admits **all 498**. The **11 recovered** proofs are full solutions (6k–43k chars, median ~20k; none below gold's 500-char floor), discarded by strict *only* over a missing close-tag / surrounding text. Zero degenerate recoveries. More valid candidates in the pool can only help selection — the ranking is unchanged. (On this data the verifier-side leniency made no difference: strict and lenient both parsed 100% of finished verifications. It's the generation side that benefits.)

### 1d. Float score `1.0`/`0.0` accepted — CHANGED (blatant bug fix, always on)
Geremie's literal regex only matched `0`/`0.5`/`1`, so `<score>1.0</score>` → the **whole proof was dropped** over a trailing `.0`. We parse the number and validate the *value* ∈ {0, 0.5, 1}. This is a bug fix, so it applies in **both** parse modes (not gated).

> The score is the XML `<score>` (proof quality 0/0.5/1), **not** `\boxed{}` (the answer inside the proof). We never parse `\boxed{}` for the score — that would grab the problem's answer.

## 2. Refinement topology

### What Geremie does
Each round takes the top-8 verified proofs; for each parent it selects its **4 worst
(lowest-scoring) reviews**; and it emits **one refine call per (parent, single
review)** → 8 × 4 = 32 single-parent / single-review refine calls.

### What gold does
Merges up to **4 candidates** into one refine bundle, each with up to **3** of its
reviews — i.e. the refiner sees *several* partial proofs and their critiques at
once and synthesizes. This multi-parent merge is where gold's method draws its
strength.

### What we do
32 refine calls (round width unchanged), each merging **`refine_parents: 4`
stratified-random parents** from the top-8 pool, each contributing up to
**`reviews_per_refine_parent: 3`** reviews. This restores gold's merge shape.

- **Stratified parent selection:** a seeded permutation of the pool + rotating
  window, so every top-8 proof is used ~equally across the 32 calls (even
  coverage, reproducible) — not the same parent repeatedly.
- **`refine_review_strategy: random_nonideal` (default):** sample the parent's
  reviews with **score < 1**, varied per call. Rationale: an *ideal* (score-1)
  review says "nothing to fix" → no improvement signal for the refiner; the
  non-ideal reviews are exactly the "here's what's wrong" that a refinement should
  act on. Varying per call adds diversity across the 32 refinements. The
  alternative `worst` reproduces Geremie's deterministic lowest-scoring picks
  (which can include ideal reviews when a proof has few non-ideal ones).

### What we deliberately did NOT change
The **pool** (cumulative top-`top_proofs` verified proofs from all earlier rounds)
and the **final selection** (best proof by mean verifier score across *all* rounds,
checkpointed every round) are **Geremie's, unchanged**. So the comparison isolates
prompting + refine-bundle composition, on top of his ranking backbone.

### Capacity — does 4 parents × 3 reviews fit?
Yes, comfortably. The bundle embeds the **parsed proof text + analysis text**, not
the `<think>` reasoning (which is ~95% of a generation). Measured on the IMO-2025
traces: proof text ~9.5k chars median, analysis ~1.3k. So a 4-parent/12-review
bundle is ~15k prompt tokens typically, ≤~80k in the pathological case (four
max-length proofs) — well under the 262k context even alongside a full 128k
generation. The binding constraint is the generation budget, never the bundle.
(If the bundle ever embedded parent *reasoning*, 4 parents would blow past 262k —
it correctly uses proof+analysis only.)

## 3. Supporting evidence (from Geremie's IMO-2025 traces)

- **Output lengths:** solutions median ~68k tokens (95% of it `<think>` reasoning;
  32% hit the old 81,920 cap), refinements ~31k, verifications ~11k. Informs the
  128k completion budget and the capacity analysis above.
- **Parse recovery:** the 11-proof recovery in §1c.
- **Verifier can be confidently wrong:** on IMO-2025 P6 (a very hard problem), the
  self-verifier gave one proof a **unanimous 16/16 score-1**, triggering early-stop
  after round 1 on an almost-certainly-wrong proof — even though the verifier was
  discriminating in aggregate (44% of all its scores were 0). Takeaway: the
  internal mean-verifier-score is **not** a reliable solve signal on hard problems;
  the markscheme grade (judge-side) is the real arbiter. This is why we grade
  externally rather than trusting the pool's self-report.

## 4. Why the baseline is a fair test

The deploy run uses **Geremie's exact deployment + search budget** (tp2/dp4, bf16,
fa3, bf16 KV, ctx 262144, 128k completion, 32×16, min_valid 4, seed 0,
**max_rounds 4**). The *only* moving parts are the four harness changes above. So
"our score vs Geremie's" measures the harness, and "vs ycchen's 12.75/42" measures
the whole stack against the known bar.

### Reproduce Geremie exactly (A/B knob recipe)
```yaml
search:
  verifier_sees_self_evaluation: true    # already gold + Geremie
  refiner_sees_self_evaluation: true     # Geremie fed it
  lenient_parsing: false                 # Geremie's strict parser
  refine_parents: 1                      # single-parent refine
  reviews_per_refine_parent: 1
  refine_review_strategy: worst          # Geremie's lowest-scoring
```
The only residual difference is the float-score fix (a bug fix, always on).

## References
- `hav4ik/imo-inference`: `CHANGES_VS_UPSTREAM.md` (knob table), `evaluation/PARSING_VS_GOLD.md` (parser detail with gold line refs), `config-nii-r4.yaml`.
- Gold: ycchen `proof-pilot-code` → `kaggle_deploy/final/proof_agent/{parser,bundle}.py`, `v2/pool_loop.py`.
