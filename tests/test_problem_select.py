from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HARNESS = REPO / "evaluation" / "harness"
sys.path.insert(0, str(HARNESS))

from run_submission import InputRow, select_problems  # noqa: E402


def _rows(n: int = 6) -> list[InputRow]:
    # ids "1".."n" (== P1..Pn), mirroring the IMO-2026 test.csv id column.
    return [InputRow(id=str(i), problem=f"problem {i} statement") for i in range(1, n + 1)]


class SelectProblemsTests(unittest.TestCase):
    def test_all_is_identity_in_csv_order(self):
        rows = _rows()
        self.assertEqual(select_problems(rows, "all"), rows)
        self.assertEqual(select_problems(rows), rows)  # default
        self.assertEqual(select_problems(rows, ""), rows)  # empty == all

    def test_explicit_id_list_preserves_requested_order(self):
        rows = _rows()
        # any subset the input defines is valid -- nothing hardcoded
        self.assertEqual([r.id for r in select_problems(rows, "1,4,5")], ["1", "4", "5"])
        self.assertEqual([r.id for r in select_problems(rows, "5,1,4")], ["5", "1", "4"])
        self.assertEqual([r.id for r in select_problems(rows, "2")], ["2"])
        # whitespace tolerated
        self.assertEqual([r.id for r in select_problems(rows, " 1 , 3 ")], ["1", "3"])

    def test_limit_caps_first_n(self):
        rows = _rows()
        self.assertEqual([r.id for r in select_problems(rows, "all", limit=3)], ["1", "2", "3"])
        # composes with an id list: 1,4,5 then first-2 -> ids 1,4
        self.assertEqual([r.id for r in select_problems(rows, "1,4,5", limit=2)], ["1", "4"])
        # limit larger than selection is a no-op
        self.assertEqual(len(select_problems(rows, "1,4,5", limit=99)), 3)

    def test_duplicate_ids_deduped_preserving_order(self):
        rows = _rows()
        self.assertEqual([r.id for r in select_problems(rows, "1,1,4,4")], ["1", "4"])

    def test_unknown_id_fails_fast(self):
        rows = _rows()
        with self.assertRaises(ValueError) as ctx:
            select_problems(rows, "1,7")
        self.assertIn("7", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
