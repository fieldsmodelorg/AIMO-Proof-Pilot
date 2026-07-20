# Nondeterminism & duplicate generations

Why nondeterministic runs (`server.deterministic_inference: false`) occasionally
emit **byte-identical duplicate generations**, what causes it, and why we accept
it. Companion to [`CHANGES_VS_UPSTREAM.md`](../CHANGES_VS_UPSTREAM.md) and
[`DEGENERATE_FILTER.md`](DEGENERATE_FILTER.md).

**One-line summary:** with deterministic inference off (the deliberate speed
choice), SGLang **silently drops the per-request seed**, so on a *peaked/easy*
problem `top_p=0.95` collapses decoding to near-argmax and a few of the 32
generations fall onto the same deterministic trajectory and come out identical.
It is **benign for solving** (easy problems need only one correct proof) but means
**distinct per-request seeds do not guarantee distinct samples** in this mode.
`temperature=1.0`/`top_p=0.95` are fixed by decision; the clean fix is to seed the
sampler coins without paying for batch-invariant kernels (see §6).

---

## 1. The phenomenon (empirical)

Generating 32 proofs for IMO-2026 **P1** (an easy problem — the model self-scores
it 1.0), nondeterministic, `temperature=1.0`, `top_p=0.95`, DFlash on, dp=4:

| Run | unique solutions / 32 | duplicate cluster |
|---|---|---|
| `imo2026-nd-test`    | 30/32 | `r01-p0008/9/10` identical (42,119-char reasoning) |
| `imo2026-p1-uniq`    | 30/32 | `r01-p0008/9/10` identical — **same text, same hash `3b9a2b9301ee`** |
| `imo2026-nd-fixed`   | 32/32 | none |
| `imo2026-stream-test`| 32/32 | none |

Key facts about the duplicate cluster:

- **3 different seeds** (754889539 / 896284131 / 161558040), yet byte-identical
  42,119-char reasoning and identical extracted `<solution>`.
- Their raw `content` diverges only at the **tail** (first difference ~char 3997
  of ~4400); everything before that is identical.
- The trio are the **3 fastest** generations (84.9 / 85.5 / 85.9 s vs. 109 s
  next-fastest, up to 215 s) — i.e. the short, high-confidence path.
- **Reproducible across independent runs**: `nd-test` and `p1-uniq` (separate
  server processes, separate times) produced the *same three indices* with the
  *same reasoning hash*. This is the decisive fact — the collision is a
  deterministic attractor, not random batch noise.
- **Intermittent**: `nd-fixed`/`stream-test` (same config) had 0 collisions.
  Run-to-run timing jitter changes how many generations get pulled onto the
  attractor; the path itself is fixed.

A teammate's report of "16/32 unique" is almost certainly the same mechanism on a
more strongly peaked problem (or with less timing jitter) pulling more samples
onto the attractor.

## 2. Root cause

Two ingredients, both required:

1. **The per-request seed is silently dropped when `deterministic_inference:
   false`.** The harness derives a distinct seed per generation
   (`stable_seed(config.seed, problem_id, sample_id)`, `proof_search.py`) and
   sends it in every API path (`async_client.py` chat / chat_stream / native
   continuation). But SGLang builds the batch `sampling_seed` tensor **only under
   `--enable-deterministic-inference`** (runtime `sampling/sampling_batch_info.py`,
   ~L108-123); otherwise `sampling_seed=None` and both the normal sampler and the
   DFlash acceptance coins fall back to the **global** `torch.rand`. → the
   carefully-derived per-request seeds never reach the sampler.
2. **`top_p=0.95` collapses the nucleus to a single token on peaked positions.**
   On a self-score-1.0 problem the top token holds ≥95% mass at nearly every
   position, so the 0.95 nucleus contains one token → decoding is effectively
   **argmax**, independent of seed, coin, and replica. Divergence is only possible
   at the rare genuinely-flat branch positions, which cluster near the answer/tail.

Together: generations that enter the peaked attractor follow it identically to the
end and emit byte-identical text — reproducibly, because argmax is robust to the
~1e-3 numeric noise between batches/replicas/runs.

## 3. What it is NOT (ruled out by the council)

- **NOT batch/dp co-location.** `launch_server.py` sets
  `--load-balance-method round_robin` with dp=4, so consecutive ids
  (p0008/9/10) land on **three different replicas** and cannot co-batch.
  "Consecutive" is incidental — they are simply the three that took the fast
  peaked path. Co-batching is at most a second-order amplifier.
- **NOT a DFlash defect.** The DFlash draft proposes greedily, but the verifier is
  **distribution-preserving** (enforced by `_validate_phase1_sampling_support`;
  see `sglang_patches/patch_dflash_sampling.py`) — it keeps the exact target
  marginal and does not reduce entropy vs. plain sampling. The draft ring is
  per-replica, so it cannot couple cross-replica requests.
- **NOT the seeds being "wrong".** The seeds are correct and distinct; they are a
  red herring because the server discards them in this mode.

## 4. Impact

- **Benign for solving.** Collisions only appear on easy/peaked problems, where we
  need exactly one correct proof; losing 2-3 of 32 to duplication costs nothing.
  Harder problems have flatter distributions and more timing churn → they diverge
  where diversity actually matters. It does **not** crash and is unrelated to the
  P6 runaway that the watchdog/degenerate work fixed.
- **Matters for diversity accounting and reproducibility.** Any pass@k / uniqueness
  analysis that assumes "32 seeds = 32 independent draws" is biased in this mode.
  Report unique/32, not just count.

## 5. How to measure collisions (analysis note)

Use the extracted proof text and the correct call fields:

- `proofs/rNN-pMMMM.json` → `proof` (the extracted `<solution>`), and
- `calls.jsonl` **top-level** `content` / `reasoning_content` for stage
  `round-NN/generate`.

`calls.jsonl` has **no `message` sub-object** — reading `record["message"]["content"]`
yields empty strings that trivially "collide" (this produced a false collision
report once). Hash the real fields; cross-check reasoning-hash equality across runs
to distinguish a reproducible attractor from run-specific noise.

## 6. Mitigations & decisions

| Option | Effect | Decision |
|---|---|---|
| `temperature > 1.0` | flattens distribution, breaks collapse | **Rejected** — math reasoning is inherently repetitive; no temp changes. |
| `top_p` 0.95 → 0.98–1.0 | widens nucleus, breaks collapse | **Rejected** — keep `top_p=0.95`. |
| `deterministic_inference: true` | seeds coins **and** makes math batch-invariant → guaranteed distinct, reproducible samples | **Rejected for production** — the batch-invariant kernels cost ~1.25–1.5× throughput. |
| **Seed the coins only** | populate `sampling_seed` from the per-request seed **without** batch-invariant kernels — distinct seeds drive distinct coins at every branch, at ~no throughput cost | **Documented but deferred (not implemented).** The seeded-coin path already exists (`patch_dflash_sampling.py` `make_seeded_uniforms`, keyed on `hash(seed, position)`); it is gated behind full determinism today. The remaining work is a surgical script-patch to `sampling_batch_info.py` `from_schedule_batch` to build the `sampling_seed` tensor in nondeterministic mode (behind a runtime knob, default off → byte-identical to stock). Deferred **by decision**: the collision is benign (§4) and the change touches the delicate DFlash sampler, so it isn't worth the GPU diversity-revalidation cost until diversity accounting actually bites. |

**Not yet run — confirming diagnostic (optional):** *isolation replay* — re-issue
the three colliding requests one-at-a-time (concurrency=1) with a same-seed /
different-seed matrix. Isolated-still-identical ⇒ prompt-determined argmax collapse
(batching irrelevant); same-seed-twice-differs ⇒ seed effective nowhere;
different-seeds-diverge-only-when-isolated ⇒ batching implicated. The cross-run
reproducibility in §1 already points to prompt-determined collapse.

## 7. Bottom line

Nondeterministic mode trades per-request-seed control for throughput. On peaked
problems that surfaces as a small number of reproducible duplicate generations —
understood, benign for solving, and cleanly fixable (without changing
temperature/top_p) by seeding the sampler coins if/when diversity accounting needs
it.
