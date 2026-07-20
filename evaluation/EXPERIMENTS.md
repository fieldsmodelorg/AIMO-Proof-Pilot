# Experiment log

Running log of IMO-2026 inference experiments (newest first). Each entry pins the
model, config, problem selection, node, code commit, and the exact HF trace
directory so a run is reproducible and its outputs are findable. Companion to
[`NONDETERMINISM.md`](NONDETERMINISM.md), [`DEGENERATE_FILTER.md`](DEGENERATE_FILTER.md),
and [`../CHANGES_VS_UPSTREAM.md`](../CHANGES_VS_UPSTREAM.md).

---

## `imo2026-*-2x` — "2x" scaled search + LLM selector (deploy vs step-225 A/B)

- **Started:** 2026-07-20 ~04:16 UTC · **Nodes:** node0 (`hnode495`) deploy, node1 (`hnode061`) step-225 · both 8×H200 · **Status:** halted mid-run (compute node stopped during P3–P4); finalized problems recovered from the HF trace mirror.
- **Purpose:** (1) stress the harness at 2× search width; (2) first production exercise of the re-added **LLM final-solution selector** (shuffled-ballot majority vote); (3) A/B the **deploy** checkpoint against **step-225** on identical config.
- **Models:** node0 = `opd-32b-deploy` (Yi-Chia's live IMO checkpoint); node1 = `opd-32b-bf16-step-225`. Shared DFlash draft `dflash-32b-draft-v2test-phaseL`.
- **Config:** [`../config-nii-2x.yaml`](../config-nii-2x.yaml) (deploy) / [`../config-nii-2x-step225.yaml`](../config-nii-2x-step225.yaml) (step-225) — identical except `models.bf16_target` + `traces.run_name`. **2×** every search width vs `config-nii-r4.yaml`: `proofs_per_round 64`, `verifications_per_proof 32`, `top_proofs 16`, `refine_parents 8`, `max_rounds 8` (`reviews_per_refine_parent 3`, `min_valid_verifications 4`, `temperature 1.0`/`top_p 0.95`, nondeterministic, `filter_degenerate`+`stream_detect` on, `watchdog_timeout 1200`, tp2×dp4, ctx 262144). These committed files are verified byte-value-identical to the config pinned in each HF trace dir.
- **LLM selector (new this run):** `llm_selector: true`, `selection_votes: 16`, `selection_candidates: 4`, `selection_max_tokens: 56000`, `selection_continuation_tokens: 2048`. 16 voters each see the top **4** proofs (decoupled from `top_proofs`; the model was trained to re-rank a small set) in an independently shuffled order and pick via `<selected_id>` at temp 0.3; majority vote, ties → higher verifier rank, fallback to top verifier-scored proof. A ballot that reasons past 56k is **force-closed** (`</think>`+`<selected_id>`) and continued so it still votes (fixes null ballots — see the crash+force-close commits below). Live P1 re-selection went from 5–9/16 null ballots to **16/16 valid** on both nodes.
- **Problems:** all 6 — input `evaluation/data/imo2026-latex-test.csv`. Artifacts index by position: `row-0000`=P1 … `row-0005`=P6.
- **HF traces:** `imo2026-challenge/chankhavu-imo-reasoning-traces` : **`imo2026-deploy-2x-20260720-041639`** (deploy) and **`imo2026-step225-2x-20260720-042144`** (step-225).
- **Code:** branch `feature/streaming-loop-abort` @ `9702365` (selector force-close), on top of `963a112` (selector length-crash fix) and `a120077` (top-4 cap).

### Results (finalized before the halt; recovered from HF)

step-225 reached **P3** (its round 8 finalized just before the halt); deploy reached **P2** (its P3 was mid-round-5). Scores below: `mean_verifier_score` from the run, and an independent **grade /7** vs the official markscheme (`chankhavu/IMO2026-GPT-5.6-Sol-Markscheme`) by a multi-grader panel (from-scratch + markscheme, route-neutral).

| Problem | deploy verifier | step-225 verifier | grade /7 | notes |
|---|---|---|---|---|
| P1 (gcd/lcm board) | 1.00 | 1.00 | **7** | fully correct on both; `M = ∏ p^{gcd_i ν_p}` matches markscheme |
| P2 (prove OM=ON) | 0.12 | 0.20 | **1** | true theorem but **fabricated** proofs (asserted/false lemmas); verifier correctly distrusted |
| P3 (stick game, step-225 only) | — | 0.578 | **0–1** | **wrong answer** for n≥2 (claims ½; correct `c_n = 2ⁿ/(2ⁿ⁺¹−1)`); flaw: upper-bound step ignores Liu's own cuts |

**Key finding:** the self-verifier/selector were reliable where confident (P1 high, P2 low both justified) but **over-optimistic on the confidently-wrong P3** (0.578 + a 10/16 selector majority for an incorrect answer). The LLM selector cannot catch this — it only compares proofs to each other, so a pool that converges on a wrong answer yields the "best wrong" pick. An **answer-consistency gate** (for "determine the value" problems) would have caught P3; the selector would not. See the recovered proofs + grade report for detail.

### Note on reproducibility

The two `config-nii-2x*.yaml` files were **node-local and uncommitted** during the run; they are now reconstructed from the r4 base + the HF-pinned copies and committed here. Launch mirrors the `bugfix-p145` recipe below (server via `launch_server.py`, submission via `run_submission.py` with `--input evaluation/data/imo2026-latex-test.csv` and no `--problems` filter = all 6); set a fresh timestamped `traces.run_name` per launch.

---

## `imo2026-bugfix-p145` — P1/P4/P5 full-search on the bugfix merge

- **Started:** 2026-07-19 23:22 UTC · **Node:** node0 (`hnode495`), 8×H200 · **Status:** running
- **Purpose:** first full-search production run on the hardened harness — validate
  the merged production checkpoint on a representative quick-benchmark subset
  (P1 easy; P4/P5 harder) with streaming loop-abort + salvage, watchdog bump, and
  the gzip degenerate filter all active, plus the new `--problems` selector.
- **Model:** `opd-32b-bf16-merged-125-to-225-bugfix` (HF `fieldsmodelorg/Olmo-3.1-32B-Think-OPD-IMO`, subdir `opd-32b-bf16-merged-125-to-225-bugfix`) + DFlash draft `dflash-32b-draft-v2test-phaseL`.
- **Config:** [`config-nii-bugfix-p145.yaml`](../config-nii-bugfix-p145.yaml) — full production search: `max_rounds 4`, `proofs_per_round 32`, `verifications_per_proof 16`, `top_proofs 8`, `refine_parents 4`, `reviews_per_refine_parent 3`, `min_valid_verifications 4`; `temperature 1.0` / `top_p 0.95`; **nondeterministic** (`deterministic_inference: false`); `filter_degenerate: true`, `stream_detect: true`, `watchdog_timeout: 1200`; `seed 0`; tp2×dp4, fa3, ctx 262144.
- **Problems:** P1, P4, P5 — selected at run time via `--problems 1,4,5` (the new
  selector; nothing baked into the config). Input = the full 6-problem
  `evaluation/data/imo2026-latex-test.csv` (verified byte-identical to the
  `imo2026-deploy-r4` pinned input for P1/P4/P5). Artifacts index by position:
  `row-0000`=P1, `row-0001`=P4, `row-0002`=P5.
- **HF traces:** `imo2026-challenge/chankhavu-imo-reasoning-traces` : **`imo2026-bugfix-p145-20260719-231751`** (unique timestamped run_name).
- **Code:** branch `feature/streaming-loop-abort` @ `2635f51` (harness + SGLang patches from this repo).

### Launch (reproduce)

Server (node0):
```bash
opd-run sglp145 bash -c 'source /tmp/chankhavu/venvs/infervenv/.runtime/activate-env.sh && \
  exec python /tmp/chankhavu/imo-inference/evaluation/harness/launch_server.py \
    --config /tmp/chankhavu/imo-inference/config-nii-bugfix-p145.yaml'
```
Submission (after server healthy; `HF_TOKEN` exported before `activate-env.sh` so
the file-based `hf auth login` token survives the `HF_HOME` redirect):
```bash
opd-run subp145 bash -c 'export HF_TOKEN="$(hf auth token 2>/dev/null)"; \
  source /tmp/chankhavu/venvs/infervenv/.runtime/activate-env.sh && \
  exec python /tmp/chankhavu/imo-inference/evaluation/harness/run_submission.py \
    --config /tmp/chankhavu/imo-inference/config-nii-bugfix-p145.yaml \
    --input  /tmp/chankhavu/imo-inference/evaluation/data/imo2026-latex-test.csv \
    --output /tmp/chankhavu/out/imo2026-bugfix-p145-20260719-231751/submission.csv \
    --artifacts-dir /tmp/chankhavu/artifacts/imo2026-bugfix-p145-20260719-231751 \
    --problems 1,4,5'
```
Note: for a *unique* HF trace dir per run, set `traces.run_name` in the config to a
timestamped value (here `imo2026-bugfix-p145-20260719-231751`) and match the
`--output`/`--artifacts-dir` paths.

### Results

_To be filled in on completion (per-problem best self-verifier score; the runner
processes problems sequentially P1 → P4 → P5)._

| Problem | rounds | best mean_verifier_score | notes |
|---|---|---|---|
| P1 | — | — | in progress |
| P4 | — | — | pending |
| P5 | — | — | pending |
