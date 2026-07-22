from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HARNESS = REPO / "evaluation" / "harness"
sys.path.insert(0, str(HARNESS))

import proof_prompts as pp  # noqa: E402
from proof_search import majority_winner, ProblemSearch, Proof, Verification  # noqa: E402


class ParseSelectedIdTests(unittest.TestCase):
    def test_well_formed_tag(self):
        self.assertEqual(pp.parse_selected_id("blah <selected_id>P3</selected_id> ok"), "P3")

    def test_last_match_wins(self):
        # the model may reconsider; take its final answer
        self.assertEqual(
            pp.parse_selected_id("<selected_id>P1</selected_id>...<selected_id>P7</selected_id>"),
            "P7",
        )

    def test_open_tag_missing_close(self):
        self.assertEqual(pp.parse_selected_id("... <selected_id>P2 and that's it"), "P2")

    def test_bare_token_last_resort(self):
        self.assertEqual(pp.parse_selected_id("I think the answer is R4."), "R4")

    def test_case_insensitive_and_upper(self):
        self.assertEqual(pp.parse_selected_id("<SELECTED_ID>p5</SELECTED_ID>"), "P5")

    def test_none_when_no_id(self):
        self.assertIsNone(pp.parse_selected_id("no id here at all"))
        self.assertIsNone(pp.parse_selected_id(""))


class SelectionBundleAndMessagesTests(unittest.TestCase):
    def test_bundle_format(self):
        b = pp.selection_bundle([("P1", "proof one"), ("P2", "proof two")])
        self.assertIn('<candidate id="P1">', b)
        self.assertIn('<candidate id="P2">', b)
        self.assertEqual(b.count("<proof>"), 2)
        self.assertEqual(b.count("</candidate>"), 2)
        self.assertIn("proof one", b)
        # order preserved
        self.assertLess(b.index("proof one"), b.index("proof two"))

    def test_selector_messages_render_and_split(self):
        msgs = pp.selector_messages("PROVE X.", pp.selection_bundle([("P1", "the proof body")]))
        self.assertEqual([m["role"] for m in msgs], ["system", "user"])
        self.assertIn("choosing the final submission", msgs[0]["content"])
        self.assertIn("PROVE X.", msgs[1]["content"])          # {problem} substituted
        self.assertIn("the proof body", msgs[1]["content"])    # {selection_bundle} substituted
        self.assertIn("<selected_id>", msgs[1]["content"])
        # no unreplaced placeholders
        self.assertNotIn("{problem}", msgs[1]["content"])
        self.assertNotIn("{selection_bundle}", msgs[1]["content"])


class MajorityWinnerTests(unittest.TestCase):
    RANK = ["a", "b", "c", "d"]  # rank order (a highest)

    def test_plain_majority(self):
        votes = ["b", "b", "a", "c", "b"]
        self.assertEqual(majority_winner(votes, self.RANK), "b")

    def test_tie_broken_by_rank(self):
        # a and c tie at 2 each; a is higher-ranked -> a wins
        votes = ["c", "a", "c", "a"]
        self.assertEqual(majority_winner(votes, self.RANK), "a")

    def test_nulls_ignored(self):
        self.assertEqual(majority_winner([None, "d", None, "d", "a"], self.RANK), "d")

    def test_all_null_returns_none(self):
        self.assertIsNone(majority_winner([None, None], self.RANK))
        self.assertIsNone(majority_winner([], self.RANK))


class ConfigOptionalSelectorKeysTests(unittest.TestCase):
    def _base_search(self):
        import yaml
        cfg = yaml.safe_load((REPO / "config-nii-r4.yaml").read_text())
        return cfg

    def test_absent_is_valid(self):
        from eval_config import load_config
        import tempfile, yaml
        cfg = self._base_search()
        self.assertNotIn("llm_selector", cfg["search"])  # base config omits it
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
            yaml.safe_dump(cfg, f)
            path = Path(f.name)
        load_config(path)  # must not raise

    def test_present_and_typed(self):
        from eval_config import load_config
        import tempfile, yaml
        cfg = self._base_search()
        cfg["search"]["llm_selector"] = True
        cfg["search"]["selection_votes"] = 16
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
            yaml.safe_dump(cfg, f)
            path = Path(f.name)
        cfg["search"]["selection_candidates"] = 4
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
            yaml.safe_dump(cfg, f)
            path = Path(f.name)
        loaded = load_config(path)
        self.assertTrue(loaded["search"]["llm_selector"])
        self.assertEqual(loaded["search"]["selection_votes"], 16)
        self.assertEqual(loaded["search"]["selection_candidates"], 4)

    def test_bad_types_rejected(self):
        from eval_config import load_config
        import tempfile, yaml
        for key, bad in (
            ("llm_selector", "yes"),
            ("selection_votes", 0),
            ("selection_votes", -3),
            ("selection_candidates", 0),
            ("selection_candidates", -1),
        ):
            cfg = self._base_search()
            cfg["search"][key] = bad
            with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
                yaml.safe_dump(cfg, f)
                path = Path(f.name)
            with self.assertRaises(ValueError, msg=f"{key}={bad!r} should be rejected"):
                load_config(path)

    def test_tournament_keys_accepted(self):
        from eval_config import load_config
        import tempfile, yaml
        cfg = self._base_search()
        cfg["search"].update(
            selection_tournament=True,
            selection_tournament_threshold=0.9,
            selection_tournament_rounds=32,
            selection_tournament_max_candidates=8,
            selection_score_window=0.15,
        )
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
            yaml.safe_dump(cfg, f)
            path = Path(f.name)
        loaded = load_config(path)
        self.assertTrue(loaded["search"]["selection_tournament"])
        self.assertEqual(loaded["search"]["selection_tournament_rounds"], 32)

    def test_tournament_bad_values_rejected(self):
        from eval_config import load_config
        import tempfile, yaml
        for key, bad in (
            ("selection_tournament", "yes"),
            ("selection_tournament_threshold", 0),
            ("selection_tournament_threshold", 1.5),
            ("selection_tournament_rounds", 0),
            ("selection_tournament_max_candidates", 0),
            ("selection_score_window", 1.0),
            ("selection_score_window", -0.1),
        ):
            cfg = self._base_search()
            cfg["search"][key] = bad
            with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
                yaml.safe_dump(cfg, f)
                path = Path(f.name)
            with self.assertRaises(ValueError, msg=f"{key}={bad!r} should be rejected"):
                load_config(path)


class TournamentSelectionTests(unittest.TestCase):
    """The tiered tournament path (saturated verifier -> stratified brackets)."""

    MARK = "THE-TARGET-PROOF"

    def _proof(self, i: int, score: float, mark: bool = False) -> Proof:
        body = f"Proof number {i}." + (f" {self.MARK}" if mark else "")
        return Proof(
            proof_id=f"r00-p{i:04d}",
            round_index=0,
            parent_id=None,
            proof=body,
            self_evaluation="ok",
            self_score=1.0,
            generation_sample_id=f"s{i}",
            verifications=[Verification(sample_id=f"v{i}", score=score, analysis="")],
        )

    def _run(self, cfg, ranked, perform):
        import asyncio, tempfile

        with tempfile.TemporaryDirectory() as d:
            ps = ProblemSearch(
                problem_id="1",
                problem="Prove something.",
                output_dir=Path(d),
                client=None,
                semaphore=asyncio.Semaphore(8),
                config=cfg,
            )
            ps._perform = perform
            return asyncio.run(ps._select_final(ranked))

    def _target_ballot(self, seen):
        """A fake selector that votes for the marked proof when present, else abstains
        (null vote). Records per-bracket candidate counts into `seen`."""
        import re

        async def perform(spec, temperature=None):
            user = spec.messages[-1]["content"]
            cands = re.findall(r'<candidate id="(P\d+)">.*?<proof>(.*?)</proof>', user, re.S)
            seen.append(len(cands))
            for cid, body in cands:
                if self.MARK in body:
                    return {"content": f"<selected_id>{cid}</selected_id>"}
            return {"content": "no pick here"}  # parses to None -> null vote

        return perform

    def test_tournament_runs_when_saturated_and_picks_most_wins(self):
        # 8 proofs all >=0.95 -> saturated (> selection_candidates=4) -> tournament.
        cfg = {
            "seed": 0, "top_proofs": 16, "selection_candidates": 4, "selection_votes": 16,
            "temperature": 1.0, "top_p": 0.95,
            "selection_tournament": True, "selection_tournament_threshold": 0.95,
            "selection_tournament_rounds": 16, "selection_tournament_max_candidates": 10,
        }
        scores = [1.0, 0.99, 0.98, 0.97, 0.97, 0.96, 0.96, 0.95]
        ranked = [self._proof(i, s, mark=(i == 3)) for i, s in enumerate(scores)]
        seen = []
        result = self._run(cfg, ranked, self._target_ballot(seen))

        self.assertIsNotNone(result)
        self.assertEqual(result["mode"], "tournament")
        self.assertEqual(result["winner_id"], "r00-p0003")           # the marked proof
        self.assertEqual(result["total_votes"], 16)                  # one tally per bracket
        self.assertEqual(len(seen), 16)                              # 16 selector calls
        self.assertTrue(all(c == 4 for c in seen), seen)             # group size = 4
        # stratified: 8 proofs * appearances, 16 rounds * 4 slots = 64 -> 8 each, balanced
        appear = result["appearances"]
        self.assertEqual(set(appear.values()), {8})

    def test_tournament_is_on_by_default(self):
        # selection_tournament OMITTED -> defaults ON; a saturated pool still tournaments.
        cfg = {
            "seed": 0, "selection_candidates": 4, "selection_votes": 16,
            "temperature": 1.0, "top_p": 0.95,
            "selection_tournament_rounds": 8,
        }
        ranked = [self._proof(i, 1.0, mark=(i == 2)) for i in range(8)]
        seen = []
        result = self._run(cfg, ranked, self._target_ballot(seen))
        self.assertEqual(result["mode"], "tournament")
        self.assertEqual(result["winner_id"], "r00-p0002")

    def test_tournament_caps_pool_at_max_candidates(self):
        cfg = {
            "seed": 1, "selection_candidates": 4, "selection_votes": 16,
            "temperature": 1.0, "top_p": 0.95,
            "selection_tournament": True, "selection_tournament_threshold": 0.95,
            "selection_tournament_rounds": 20, "selection_tournament_max_candidates": 6,
        }
        ranked = [self._proof(i, 1.0, mark=(i == 0)) for i in range(12)]  # all saturated
        seen = []
        result = self._run(cfg, ranked, self._target_ballot(seen))
        # only the top-6 candidates ever entered the bracket pool
        self.assertEqual(len(result["appearances"]), 6)
        self.assertEqual(set(result["appearances"].keys()),
                         {f"r00-p{i:04d}" for i in range(6)})

    def test_below_threshold_uses_windowed_vote_excluding_far_proofs(self):
        # only 2 proofs >=0.95 (not > 4) -> windowed majority vote, window 0.2 of best (1.0)
        # -> floor 0.8, so the 0.5 and 0.3 proofs are never shown to the selector.
        cfg = {
            "seed": 0, "selection_candidates": 4, "selection_votes": 5,
            "temperature": 1.0, "top_p": 0.95,
            "selection_tournament": True, "selection_tournament_threshold": 0.95,
            "selection_score_window": 0.2,
        }
        ranked = [self._proof(0, 1.0), self._proof(1, 0.96),
                  self._proof(2, 0.5), self._proof(3, 0.3)]
        bodies = []

        async def perform(spec, temperature=None):
            bodies.append(spec.messages[-1]["content"])
            return {"content": "<selected_id>P1</selected_id>"}

        result = self._run(cfg, ranked, perform)
        self.assertIsNotNone(result)
        self.assertEqual(result["mode"], "vote")               # NOT tournament
        joined = "\n".join(bodies)
        self.assertIn("Proof number 0.", joined)
        self.assertIn("Proof number 1.", joined)
        self.assertNotIn("Proof number 2.", joined)            # 0.5 excluded by window
        self.assertNotIn("Proof number 3.", joined)            # 0.3 excluded by window

    def test_disabled_ignores_scores_and_uses_top_n(self):
        # selection_tournament=False -> legacy top-n vote, mean_score never consulted.
        cfg = {
            "seed": 0, "selection_candidates": 4, "selection_votes": 3,
            "temperature": 1.0, "top_p": 0.95, "selection_tournament": False,
        }
        ranked = [self._proof(i, 1.0) for i in range(8)]
        seen = []

        async def perform(spec, temperature=None):
            seen.append(spec.messages[-1]["content"].count("<candidate"))
            return {"content": "<selected_id>P1</selected_id>"}

        result = self._run(cfg, ranked, perform)
        self.assertEqual(result["mode"], "vote")
        self.assertTrue(all(c == 4 for c in seen), seen)


class SelectionCandidateCapTests(unittest.TestCase):
    """The selector must re-rank only selection_candidates proofs, NOT top_proofs.

    top_proofs sizes the refinement parent pool (16 in the 2x config); the selector
    model was only trained to choose among a small set (~4). Feeding it 16 is out of
    distribution. This locks the two knobs apart.
    """

    def _proof(self, i: int) -> Proof:
        return Proof(
            proof_id=f"r00-p{i:04d}",
            round_index=0,
            parent_id=None,
            proof=f"Proof number {i}.",
            self_evaluation="ok",
            self_score=1.0,
            generation_sample_id=f"s{i}",
        )

    def test_selector_only_sees_selection_candidates(self):
        import asyncio, tempfile

        cfg = {
            "seed": 0,
            "top_proofs": 16,
            "selection_candidates": 4,
            "selection_votes": 3,
            "temperature": 1.0,
            "top_p": 0.95,
            "selection_tournament": False,  # exercising the legacy top-n vote path
        }
        ranked = [self._proof(i) for i in range(16)]

        with tempfile.TemporaryDirectory() as d:
            ps = ProblemSearch(
                problem_id="1",
                problem="Prove something.",
                output_dir=Path(d),
                client=None,
                semaphore=asyncio.Semaphore(8),
                config=cfg,
            )
            seen_counts = []

            async def fake_perform(spec, temperature=None):
                user = spec.messages[-1]["content"]
                seen_counts.append(user.count("<candidate"))
                return {"content": "<selected_id>P1</selected_id>"}

            ps._perform = fake_perform
            result = asyncio.run(ps._select_final(ranked))

        # every ballot's bundle carried exactly selection_candidates candidates
        self.assertTrue(seen_counts)
        self.assertTrue(all(c == 4 for c in seen_counts), seen_counts)
        self.assertIsNotNone(result)
        # winner must be one of the top-4 canonical ids, never a lower-ranked proof
        top4 = {p.proof_id for p in ranked[:4]}
        self.assertIn(result["winner_id"], top4)

    def test_default_candidates_is_four(self):
        import asyncio, tempfile

        cfg = {
            "seed": 0,
            "top_proofs": 16,  # no selection_candidates -> must default to 4
            "selection_votes": 2,
            "temperature": 1.0,
            "top_p": 0.95,
            "selection_tournament": False,  # exercising the legacy top-n vote path
        }
        ranked = [self._proof(i) for i in range(16)]
        with tempfile.TemporaryDirectory() as d:
            ps = ProblemSearch(
                problem_id="1",
                problem="Prove something.",
                output_dir=Path(d),
                client=None,
                semaphore=asyncio.Semaphore(8),
                config=cfg,
            )
            seen_counts = []

            async def fake_perform(spec, temperature=None):
                seen_counts.append(spec.messages[-1]["content"].count("<candidate"))
                return {"content": "<selected_id>P1</selected_id>"}

            ps._perform = fake_perform
            asyncio.run(ps._select_final(ranked))
        self.assertTrue(all(c == 4 for c in seen_counts), seen_counts)


if __name__ == "__main__":
    unittest.main()
