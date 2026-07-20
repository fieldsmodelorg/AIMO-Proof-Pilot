# Changes on the `docker/container-improvements` branch vs Geremie's upstream

Master list of every change this branch makes on top of Geremie Yeo's harness
(`bogoconic1/aimo-proof-pilot-inference`, forked at `main`). Each behavior change
has a **config knob** and defaults to the gold-standard (Yi-Chia Chen's Kaggle
solution) behavior; blatant bug fixes are always on. Deeper rationale for the
parser and self-eval items lives in [`evaluation/PARSING_VS_GOLD.md`](evaluation/PARSING_VS_GOLD.md).

## Behavior knobs (all under `search:` in the config)

| Knob | Default | What it changes vs upstream | Gold standard |
|---|---|---|---|
| `verifier_sees_self_evaluation` | `true` | Feed the prover's self-eval **text** into the verifier prompt. | `true` — gold (Kaggle + training) feeds it; in-distribution. |
| `refiner_sees_self_evaluation` | `false` | Feed the parent self-eval into the refiner bundle. Upstream fed it; we drop it. | `false` — gold's Kaggle inference drops it (self-score ~92% "1", noise). |
| `refine_parents` | `4` | Parents merged per refine call (was 1). Stratified random from the top-`top_proofs` pool. | `4` = gold's `refine_inputs`. |
| `reviews_per_refine_parent` | `3` | Reviews per parent in the bundle (was 1). | `3` = gold's `verify_k` (gold includes all ≤3). |
| `refine_review_strategy` | `random_nonideal` | Which reviews: `random_nonideal` (seeded random, score<1, varied per call) or `worst` (Geremie's deterministic lowest-scoring, may include ideal). | — (a design choice; gold uses *all* reviews) |
| `lenient_parsing` | `true` | Gold search-based extraction (recover missing `</solution>`, tolerate surrounding text, ignore tag case, allow empty self-eval/suggestions) vs upstream's strict whole-document `fullmatch`. | `true` — gold parses leniently; the OPD model omits `</solution>`. |
| `filter_degenerate` | `true` | Drop generations/verifications that fell into a degenerate repetition/enumeration loop (`loop_detect.is_degenerate`), so they never enter the pool, seed a refine, or score a proof. Upstream has no such check. | `true` — re-adds Yi-Chia v2's `zlib_runaway_detector` + `loopguard`, which Geremie's fork dropped. |
| `stream_detect` | `true` | Stream generations/verifications and detect the loop **live**, aborting the request and salvaging a proof from the clean pre-loop prefix (reclaims compute + prevents the server stall). Upstream is blocking with no live detection. | `true` — Yi-Chia v2's streaming loop-detect + salvage (`stream_engine`), which Geremie's fork dropped. (Needs a live-server smoke test — see the doc.) |
| `llm_selector` / `selection_votes` / `selection_candidates` / `selection_max_tokens` / `selection_continuation_tokens` | `false` / `16` / `4` / `56000` / `2048` | **OPTIONAL** final selection stage. When on, after the last round `selection_votes` voters each see the top **`selection_candidates`** proofs (proof text only, like gold) in an independently shuffled order and pick one via `<selected_id>` (temp 0.3); the majority-voted proof is submitted (ties → higher verifier rank), with fallback to the top verifier-scored proof. A ballot that reasons past `selection_max_tokens` is **force-closed** (`</think>`+`<selected_id>`) and continued for `selection_continuation_tokens` so it still votes. When off/absent, the submission is the top verifier-scored proof (upstream behaviour, unchanged). | Re-adds Yi-Chia's gold `select-by-id` stage (`build_select_bundle`/`selector.txt`), which Geremie's fork dropped. **`selection_candidates` is decoupled from `top_proofs`** (the refinement pool): gold re-ranks only ~4 (`select_bundle_n=4`), so feeding it 16 is out-of-distribution. **Enhanced vs gold:** gold used 5 unshuffled voters with a wall-clock cap; we default to 16 with per-ballot shuffle (debias position/label) and a fixed token budget with force-close (offline analog of gold's time cap; both force-close truncated selection CoT). **Live-validated** in the `imo2026-*-2x` runs: null ballots 5–9/16 → **16/16 valid**. |

Each is validated as the right type by the strict schema (`eval_config.py`) and
present in both `config.yaml` and `config-dynamic.yaml`.

## Deployment changes (config values / env — also effectively knobs)

| Change | Where | Knob / override | Default |
|---|---|---|---|
| **Auto data-parallel width** | `config.yaml` `model.data_parallel_size` | `auto` (derive from GPU count) or an explicit int | `4` in `config.yaml`; `auto` in `config-dynamic.yaml` |
| **fp8 KV cache** | `model.kv_cache_dtype` | `fp8_e4m3` / `auto` (bf16) / `fp8_e5m2` | `auto` (bf16) in `config.yaml`; `fp8_e4m3` in `config-dynamic.yaml` |
| **Triton attention (Blackwell sm120)** | `server.attention_backend: triton` | `fa3` (Hopper) / `fa4` / `triton` (sm120) | fa3; triton in `config-blackwell.yaml`. launch_server auto-sets `FLASHINFER_CUDA_ARCH_LIST` (9.0a Hopper / 12.0f Blackwell) + `--triton-attention-num-kv-splits 32` |
| **SGLang runtime baked into the image** | `Dockerfile` (multi-stage) | build args `RUNTIME_HF_REPO`/`RUNTIME_HF_REVISION`/`RUNTIME_ARCHIVE_SHA256`; `--secret id=hf_token` at build | venv downloaded + sha256-verified + relocated + deps-installed at build, frozen at `/opt/pp` |
| **Dropped hardcoded `CUDA_VISIBLE_DEVICES`** | `Dockerfile` | — (derived from `tp*dp`) | required for auto-dp; no knob |
| **SGLang scheduler watchdog timeout** | `server.watchdog_timeout` → `--watchdog-timeout` | seconds a scheduler forward pass may make no progress before SGLang SIGQUITs the whole server | `1200`. SGLang's default is **300**, which killed the server mid-run on long/degenerate P6 generations (see below). |

`config-dynamic.yaml` is a **new profile** for sub-8-GPU nodes (auto-dp + fp8 KV);
`config-blackwell.yaml` is a **new profile** for 8× RTX PRO 6000 Blackwell (sm120,
no NVLink): triton attention (the only sink-correct backend on sm120), TP=2/auto-dp,
fp8 KV, **DFlash off** (see note). `config.yaml` stays byte-faithful to upstream's
8×H200 topology except for the knobs above defaulting to gold.

**Blackwell + DFlash limitation:** DFlash needs a triton draft backend on sm120,
but the DFlash ring worker (`dflash_worker_v2_ring.py`) hard-requires fa3/fa4 for
the draft, and Yi-Chia's triton-capable draft is TP=1-only. So TP=2 + DFlash +
triton is supported by no existing code path; `config-blackwell.yaml` runs without
speculation. Enabling it would require a triton-capable TP-sharded ring worker
(new work, unvalidated).

## Reasoning-trace upload (optional, new `traces:` section)

A new **optional** top-level `traces:` section makes `run_submission.py`
periodically push the whole artifacts tree — `problems/<id>/calls.jsonl` (every
model call, with `reasoning_content` = the `<think>` traces and `content` = the
answer), plus `prompts/`, `proofs/`, `rounds/`, `final.json` and the pinned
`test.csv`/`config.yaml` — to a HuggingFace dataset. It uploads every
`interval_seconds` and once more at shutdown (even if the search raised).

| Key | Meaning |
|---|---|
| `enabled` | Master switch. Omit the whole section (or set false) to disable. |
| `dataset_repo` | `owner/name` of the target HF dataset. |
| `secrets_file` | Path to a JSON/YAML file with an `hf_token` key, or `""` to use the ambient HF token (`HF_TOKEN` env / `hf auth login`). The token is **never** in the config. |
| `interval_seconds` | Snapshot cadence. |
| `private` | Applied only when the dataset is first **created**; an existing repo keeps its visibility. |
| `run_name` | Subfolder in the dataset; `""` derives it from the active target model's folder name, so each checkpoint uploads to its own namespace. |

Design points: init fails fast (bad token / missing secrets) so a
misconfiguration is caught before the run, but once running, individual upload
errors are logged and swallowed — a flaky network can never kill a multi-hour
proof run. Uploads run in a worker thread (search keeps serving) with only one
in flight at a time. `SECRETS.*`, `*.tmp`, and `*.token` are never uploaded even
if they sit under the artifacts dir. The section is validated strictly by
`eval_config.py` like every other; being optional, existing configs without it
stay valid. `config.yaml` ships it enabled (targeting
`chankhavu/imo-reasoning-traces`); `config-dynamic.yaml` / `config-blackwell.yaml`
omit it.

## Blatant bug fixes (always on, no knob)

| Fix | Why it's a bug, not a policy |
|---|---|
| **Float score parsing** — `<score>1.0</score>` / `0.0` accepted (`math.isclose` to {0,0.5,1}) | Upstream's literal regex rejected `1.0`, discarding the whole proof over a trailing `.0`. Applies in **both** parsing modes. |

(The empty-verifier-`<suggestions>` acceptance is part of `lenient_parsing`, not a
standalone always-on fix, since strict mode deliberately re-imposes the full
structure.)

## Refinement topology

The refinement changed from "one parent × its single worst review" to
"`refine_parents` stratified-random parents × `reviews_per_refine_parent` reviews
each". Counts, parent selection, and review strategy are all configurable:
`refine_parents`, `reviews_per_refine_parent`, and `refine_review_strategy`
(`random_nonideal` default, or `worst` for Geremie's deterministic lowest-scoring
reviews). Parent selection is always stratified-random from the top-`top_proofs`
pool. Round width is unchanged (`proofs_per_round` refine calls per round). See
the refinement section of `PARSING_VS_GOLD.md`.

## Degenerate-loop filter + server watchdog (crash fix)

A step-225 IMO-2026 run **crashed mid-P6** (server SIGQUIT, exit -3). Root cause,
from the node's server log: a **verifier generation ran away to 131k tokens over
~880s** in a degenerate enumeration loop; DFlash speculative-decode acceptance
collapsed (~0.1–0.4) so throughput fell to ~40 tok/s; a scheduler forward pass
then made no progress for >300s and SGLang's **watchdog (`watchdog_timeout=300`,
default) killed the whole server**. Not OOM (KV usage 8%), not a CUDA fault — a
liveness watchdog tripped by a pathological generation length.

Two independent, composable fixes (both config-gated):

1. **`server.watchdog_timeout: 1200`** — a legit long forward no longer trips the
   watchdog; the same runaway would complete instead of killing the server.
2. **`search.filter_degenerate: true`** — `loop_detect.py` (a faithful port of
   Yi-Chia's `zlib_runaway_detector.py` + `loopguard.py`, which Geremie's fork
   dropped) rejects degenerate output. Signal = **gzip/zlib compression ratio** of
   a sliding 12k-char window: `HARD` abort at ratio < 0.05, `SOFT` abort at
   ratio < 0.18 sustained ≥ 20 checks, plus a local-density backstop (a 25-char
   chunk recurring > 8× within 1500 chars). The persistence + locality rules spare
   legitimate long math (enumerations dip but recover); validated on our own
   traces (the 131k runaway is caught; a clean 106k-token proof is not).

**No repetition penalty:** DFlash cannot apply one (`patch_dflash_sampling.py`),
and a penalty would warp the sampling distribution and corrupt legitimately
repetitive math reasoning. Aborting/rejecting a doomed generation only truncates
it — distribution-neutral — which is why gzip detection is the right tool.

`filter_degenerate` runs **post-hoc** on finished text (backstop). `stream_detect`
adds Yi-Chia's **live** path: `async_client.chat_stream` streams the completion,
feeds the same detector, and on a loop aborts the request and salvages a proof from
the clean pre-loop prefix — reclaiming the wasted compute and preventing the stall,
not just discarding output after the fact. Both default on and compose (streaming
first, post-hoc backstop). Streaming's SSE/abort path is unit-tested against mocks
but **needs a live-server smoke test** before it is trusted in production.

Full write-up — thresholds, provenance, the post-hoc-vs-streaming limitation, and
**measured degenerate-trace stats** (flag rates per problem, 0 false positives on
clean output, token scale) — is in
[`evaluation/DEGENERATE_FILTER.md`](evaluation/DEGENERATE_FILTER.md).

## Non-code / tooling additions (no behavior change)

- `install/` — host-side installer for running the runtime outside the container
  (immutable-FS nodes). Not shipped in the image (`.dockerignore`).
- `evaluation/PARSING_VS_GOLD.md`, this file — documentation.

## To reproduce upstream (Geremie) behavior for an A/B

Set, under `search:`:

```yaml
verifier_sees_self_evaluation: true    # already gold + upstream
refiner_sees_self_evaluation: true     # upstream fed it
lenient_parsing: false                 # upstream's strict parser
filter_degenerate: false               # upstream has no loop filter
stream_detect: false                   # upstream is blocking, no live detection
refine_parents: 1                      # single-parent refine
reviews_per_refine_parent: 1           # one review per parent
refine_review_strategy: worst          # upstream's lowest-scoring review
```

This restores upstream's single-parent, single-worst-review, strict-parse
refinement. The only residual difference is the float-score fix, which is a
blatant bug fix and always applies.
