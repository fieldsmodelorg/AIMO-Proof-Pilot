# Output parsing: this harness vs. the gold (Yi-Chia) pipeline

This harness admits model output through a **strict full-document XML contract**
(`evaluation/harness/proof_prompts.py`). Yi-Chia Chen's gold Kaggle pipeline
(`proof_agent/parser.py`) instead **extracts sections leniently by search**. The
two disagree on which outputs are admitted. This doc records each difference,
what gold actually does (verified against her code), and the policy decided for
this repo.

## Sources

| What | Where |
|---|---|
| Strict parser (this repo) | `evaluation/harness/proof_prompts.py` — `_GENERATION`, `_VERIFICATION`, `parse_generation`, `parse_verification` |
| Continuation trigger | `evaluation/harness/proof_search.py:175` (only on `finish_reason == "length"`) |
| Gold parser | ycchen `proof-pilot-code` → `kaggle_deploy/final/proof_agent/parser.py`, `bundle.py`, `v2/pool_loop.py` |
| Shared prompt contract | `evaluation/prompts/ycchen_math_3r/{prover,verifier}.txt` (byte-identical to gold) |

## Gold's parsing philosophy (the baseline we compare to)

- **Extract, don't validate.** Every field is pulled with `re.search(...)` under
  `re.IGNORECASE`; the whole document is never required to match. Leading
  preamble, inter-section prose, and trailing text are all tolerated.
- **Never raises.** A malformed output yields `valid=False` / `score=None` and is
  filtered downstream; it never aborts.
- **Proof admission hinges only on** `error is None and finish_reason != "length"
  and len(solution) > 500` (`parser.py:105`). **`self_evaluation` and `score` are
  not required** for a proof to be admitted.
- **Verifier counts any parseable `<score>`.** `parse_verification` extracts only
  the score; `<evaluation>` and `<suggestions>` are never parsed (`parser.py:127`).

## Differences and decided policy

| # | Case | Gold | Current strict parser | Decision |
|---|---|---|---|---|
| 1 | Verifier empty `<suggestions>` | not parsed → score still counts | **rejected** (non-empty required) | **Allow empty.** Count the score. |
| 2 | Score written `1.0` / `0.0` | regex misses it → `None`, but proof stays valid | **rejected** → whole proof lost | **Parse the score as a float**, then validate the value ∈ {0, 0.5, 1}. Do not gate on the literal regex. |
| 3 | Missing `</solution>` on natural `stop` | recovered by `_lenient_solution` | **rejected**, no recovery (continuation fires only on `length`) | **Recover like gold** (see below). |
| 4 | Trailing text after `</score>` | tolerated (search takes the first block) | **rejected** (`fullmatch`) | **Tolerate** — extract by search; don't require output to end at `</score>`. |
| 5 | Leading preamble before `<solution>` | tolerated | **rejected** (`fullmatch`) | **Tolerate** (same fix as #4). |
| 6 | Tag case (`<Solution>`) | `re.IGNORECASE` | case-sensitive | **Use `re.IGNORECASE`**, matching gold. |
| 7 | `self_evaluation` required non-empty | not required (may be empty) | required non-empty | **Open** — see "self_evaluation" below. |
| 8 | Minimum solution length | `> 500` chars (`MIN_SOLUTION_CHARS`) | merely non-empty | **Keep in mind** — current is *looser*; a floor would reject degenerate outputs. |

Cases 1–6 are all directions where this repo is **stricter than gold** and the
decision is to relax toward gold. Case 8 is the one place this repo is *looser*.

The leniency (cases 3–6, plus IGNORECASE and empty self-eval/suggestions) is
gated by **`search.lenient_parsing`** (default `true` = gold). Set it `false` to
restore upstream's strict whole-document `fullmatch` (case-sensitive, all
elements required, non-empty self-eval/suggestions). The float-score fix (case 2)
applies in **both** modes — it is a bug fix, not a leniency policy.

## The score is XML `<score>`, not `\boxed{}`

The `<score>` grade (0 / 0.5 / 1, proof quality) is **not** the same as
`\boxed{answer}`, which is the final numeric answer **inside** the proof body.
Gold's parser docstring is explicit:

> Outputs use XML tags (NOT markdown / `\boxed`) so parsing is unambiguous and
> never collides with `\boxed{answer}` inside a proof.

So do **not** parse `\boxed{}` for the score — it would grab the problem's answer,
or collide with a `\boxed` that legitimately appears in the proof. Keep the
`<score>` XML; the only change (#2) is to relax the numeric *format* it accepts.

## Recovering a missing `</solution>` (#3)

Gold's `_lenient_solution` (`parser.py:36`): find `<solution>`, then take
everything up to whichever of these appears first — `</solution>`,
`<self_evaluation>`, `</self_evaluation>`, `<score>`, or end of text. Its comment
records why:

> this model systematically OMITS `</solution>` … Strict `<solution>…</solution>`
> then drops perfectly good proofs.

The current harness has no equivalent: `_GENERATION` requires the literal
`</solution>`, and `proof_search.py:175` only attempts a continuation when
`finish_reason == "length"`. A clean-EOS (`stop`) proof with a full body but no
closing tag is therefore discarded with **no recovery path**. Adopt gold's
bounded recovery.

## self_evaluation — does gold add it? (answering the open question)

**Yes, in both training and inference — but as soft context, never as an
admission gate.**

- **Prompted in both.** Training and inference use the same math_3r templates
  (`training/opd_v2/.../roles.py:36` imports `render_prover_prompt` etc.), and
  `prover.txt` instructs the model to emit `<solution>`, `<self_evaluation>`,
  `<score>`. So the model produces a self-evaluation in both regimes.
- **Not required for admission.** Gold parses it but a proof is valid on
  `len(solution) > 500` alone; an empty self-eval does not drop the proof.
- **Fed to the verifier, empty-tolerant.** `render_verifier_prompt` /
  `build_verify` pass the candidate's `self_eval` into the verifier prompt
  (possibly empty).
- **Withheld from the refiner in v2.** `pool_loop.py:196` builds the refine
  bundle with `with_self_eval=False`, so refinement does not see self-evaluations.

Consequently, requiring a **non-empty** `self_evaluation` for admission (current
`proof_prompts.py:110`) is stricter than gold. The gold-consistent choice is to
parse it but not gate admission on it; left open pending your call.

## What "complete XML at length" means (`proof_search.py:205`)

When the first segment ends with `finish_reason == "length"` (it hit the token
cap) **but the visible content already parses as complete valid XML**, the
harness reclassifies the result to `stop` (`xml_complete_after_length = True`)
and admits it **without** a continuation. Rationale: the model emitted the full
`<solution>` / `<self_evaluation>` / `<score>` before the cap, so nothing was
lost. This is *stricter-but-smarter* than gold, which rejects any `length` result
outright. **Keep it** — it is an improvement, not an over-strictness.

## Net (parsing)

Relaxing #1–#6 moves the parser to gold's proven, search-based admission
behavior — the behavior the OPD model was tuned against — while retaining this
harness's genuine improvements (complete-XML-at-`length` reclassification,
role-correct continuations, and the option of a min-length floor from #8). The
one open policy question is #7 (whether to keep requiring a non-empty
self_evaluation).

## Prompt composition: where the self-evaluation is routed

Separate from parsing, this is *which downstream prompts* receive the prover's
`<self_evaluation>`. Gold and this harness diverge, and both are now knobs
(`search.*`), defaulting to gold's routing.

| Consumer | Gold Kaggle (`v2/pool_loop.py`) | This harness | Knob (default) |
|---|---|---|---|
| **Verifier** | **includes** it (`:177`, `render_verifier_prompt(..., cand.self_eval)`) | includes it | `verifier_sees_self_evaluation` (**true**) |
| **Refiner** | **drops** it (`:196`, `with_self_eval=False`) | *did* include it; now drops it | `refiner_sees_self_evaluation` (**false**) |

- **Verifier keeps it** because the verifier was **trained** on it
  (`training/opd_v2 build_verify → render_verifier_prompt(..., proof.self_eval)`),
  so it is in-distribution; and gold's inference feeds it too. It is the
  self-eval *text* ("note fragile steps"), never the numeric self-score. Setting
  the knob false blanks it — an off-distribution verifier prompt.
- **Refiner drops it** to match gold's *inference*, with an explicit reason in
  gold's code: *"WITHOUT prover self-eval (unreliable ~92% self-score 1)."* The
  prover's self-grade is "1" ~92% of the time, so it is noise for synthesis and
  only inflates refiner context. When dropped, the `<self_evaluation>` element is
  **omitted** from the candidate bundle (not sent empty), matching gold's
  `build_refine_bundle`. Setting the knob true restores it.

  Note the train/inference split *inside gold*: gold **training** feeds the
  parent self-eval to the refiner (`opd_v2 roles.py` builds the bundle with
  `self_eval=p.self_eval`, and `build_refine_bundle` includes it), but gold's
  **Kaggle inference** drops it (`as_proofpkg(with_self_eval=False)`). So false
  matches gold's inference and is a deliberate, gold-validated train/inference
  choice — the mirror of the verifier, where gold's inference instead *keeps*
  self-eval (= training).

This knob only affects the refiner's **input** (the parent self-eval in the
bundle). The refiner's **output** is unchanged: it is a prover-role that emits
its own `<solution>/<self_evaluation>/<score>` (parsed by `parse_generation`), so
each refined proof still produces its own self-eval and self-score that feed its
verifier and its ranking.

Refiner topology (separate from self-eval routing): this harness now merges
**`refine_parents` (default 4) stratified-random parents** per refine call, each
contributing **`reviews_per_refine_parent` (default 3)** reviews chosen by
**`refine_review_strategy`** (`random_nonideal` default, or `worst` for Geremie's
deterministic lowest-scoring). Gold merges up to 4 candidates with *all* their
(≤3) reviews; the defaults here approximate that, with the difference that gold
includes ideal reviews too while `random_nonideal` keeps only score<1. Round
width is unchanged (`proofs_per_round` calls/round).
