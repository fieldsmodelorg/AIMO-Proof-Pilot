# Experiment: `imo2026-deploy-r4` (vu)

**Owner:** vu (node0) · **Started:** 2026-07-18 (UTC) · **Status:** running · **Hardware:** 8×H200 (NII node0)

OPD-32B generate–verify–refine on the **IMO-2026** problems — a baseline of *our*
harness (bogoconic1 fork + our changes) on the trusted deploy checkpoint, at the
same model + budget Geremie is running live, so the only variables are our harness
changes.

> **Why these harness changes?** Full reasoning (prompting + refinement topology
> vs Geremie, with evidence) in
> [`vu-harness-design-rationale.md`](vu-harness-design-rationale.md).

## TL;DR

| | |
|---|---|
| Model (target) | `fieldsmodelorg/Olmo-3.1-32B-Think-OPD-ProofPilot` → `opd-32b-deploy` (bf16) |
| Draft (DFlash) | same repo → `dflash-32b-draft-v2test-phaseL` |
| Harness | `hav4ik/imo-inference` @ `docker/container-improvements`, config `config-nii-r4.yaml` |
| Problems | IMO-2026, 6 problems, **LaTeX** (`evaluation/data/imo2026-latex-test.csv`) |
| Topology | tp=2 × dp=4 (8 GPUs), bf16, DFlash on, **KV cache = bf16** (`kv_cache_dtype: auto`), fa3 |
| Search | max_rounds **4** (1 gen + 3 refine), 32 proofs/round, 16 verify/proof, temp 1.0, top_p 0.95, ctx 262144, 128k max completion |
| Traces | `imo2026-challenge/chankhavu-imo-reasoning-traces` → subfolder **`imo2026-deploy-r4/`**, every 10 min |
| Reference bar | ycchen's original OPD model scored **12.75 / 42** |

## What is being run

Sequential over the 6 IMO-2026 problems; per problem up to 4 rounds
(round 1 = 32 fresh proofs; rounds 2–4 = self-refinement). Each proof gets up to
16 independent verifier passes; the best proof by mean verifier score is
checkpointed to `submission.csv` after every round. Global search concurrency 96;
server capacity 64 req/DP-replica.

The model runs in **contestant regime** — it sees only the problem statement.
Reference solutions and markschemes are judge-side only and never reach the solver
(enforced: `test.csv` is `id,problem` only; the harness has no channel for
reference material).

## Config (matches Geremie's live IMO-2026 run except our harness changes)

Full config: `hav4ik/imo-inference` → `config-nii-r4.yaml`. Identical to Geremie's
deployment (tp2/dp4, bf16, fa3, page 1, deterministic, ctx 262144, mem_fraction
0.82, max_running 64, 128k completion, 32×16, min_valid 4, concurrency 96, seed 0,
**max_rounds 4**, **bf16 KV**).

**Our harness changes vs upstream** (the only variables in this baseline):

| Change | Ours | Upstream (Geremie) |
|---|---|---|
| refine parents / call | 4 (stratified) | 1 |
| reviews / parent | ≤3 random non-ideal | 4 worst |
| refiner sees parent self-eval | no (gold) | yes |
| parsing | lenient (gold search-based) | strict fullmatch |
| float score `1.0`/`0.0` | accepted (bug fix) | rejected |

All are gold-aligned (Yi-Chia's Kaggle solution) or blatant fixes; each is a
config knob defaulting to gold. See `CHANGES_VS_UPSTREAM.md` in the harness repo.

## Inputs & data provenance

- **Problems:** LaTeX, byte-identical to `chankhavu/IMO2026-GPT-5.6-Sol-Markscheme`
  `train.jsonl` (combined problem-set sha256 `e77c1d25…`). LaTeX chosen over
  Geremie's ASCII set because it's in-distribution for the model and matches the
  MathArena benchmark format.
- **Grading (later, separate):** `chankhavu/IMO2026-GPT-5.6-Sol-Markscheme`
  (private) markschemes, judge-side only.

## Outputs

- **On node0:** `submission.csv` → `/tmp/chankhavu/out/imo2026-deploy-r4/`;
  full artifacts → `/tmp/chankhavu/artifacts/imo2026-deploy-r4/`.
- **HF (traces):** `imo2026-challenge/chankhavu-imo-reasoning-traces` /
  `imo2026-deploy-r4/` — the whole artifacts tree: `problems/<id>/calls.jsonl`
  (every model call incl. `<think>` reasoning + answer), `prompts/`, `proofs/`,
  `rounds/`, `final.json`. Uploaded every 10 min + at shutdown; upload errors are
  logged and never abort the run.

## Experiment plan (checkpoint sweep, same config)

Run order, swapping only `models.bf16_target` + `traces.run_name`:

1. `opd-32b-deploy` → `imo2026-deploy-r4` ← **current**
2. `opd-32b-bf16-step-225` → `imo2026-step225-r4`
3. `opd-32b-bf16-step-125` → `imo2026-step125-r4`
4. (only if spare capacity) `opd-32b-bf16-step-250` → `imo2026-step250-r4`

All step checkpoints are from `fieldsmodelorg/Olmo-3.1-32B-Think-OPD-IMO` and were
SHA-verified to carry all 64 attention-sink tensors (the merged checkpoints had
dropped them — do not use those).

## How to monitor

```bash
opd-status sglang     # server (look for "fired up and ready to roll!")
opd-status submit     # submission; "[submission] id=N round=R selected=..." per round
curl -s -o /dev/null -w 'health %{http_code}\n' 127.0.0.1:30000/health
```
Traces appearing under `imo2026-deploy-r4/` on HF confirm the run is streaming.

## Notes / gotchas

- **Auth:** trace upload uses the node's built-in `hf auth login` (nguyen599, has
  `imo2026-challenge` write). No personal tokens on the shared FS. The submit
  command exports `HF_TOKEN` *before* sourcing `activate-env.sh` (which redirects
  `HF_HOME` and would otherwise hide a file-based login token).
- **Server needs no HF token** — it loads local model dirs (`/tmp/chankhavu/models`).
- Runtime = ycchen's prebuilt patched-SGLang venv at `/tmp/chankhavu/venvs/infervenv`
  (installer: `install/install_infervenv.sh` in the harness repo).
