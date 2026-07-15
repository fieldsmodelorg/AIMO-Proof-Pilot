from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO = Path(__file__).resolve().parents[1]
PATCH_PATH = REPO / "vllm_patches" / "patch_dflash_context_cutoff.py"
SPEC = importlib.util.spec_from_file_location("dflash_context_cutoff_patch", PATCH_PATH)
assert SPEC is not None and SPEC.loader is not None
patch_module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(patch_module)


class DFlashContextCutoffPatchTests(unittest.TestCase):
    def test_resolve_vllm_root_preserves_venv_python_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            venv = Path(temporary) / "venv"
            interpreter = venv / "bin" / "python"
            interpreter.parent.mkdir(parents=True)
            interpreter.symlink_to(sys.executable)

            expected = (Path(temporary) / "site-packages" / "vllm", "0.25.1")
            with mock.patch.object(
                patch_module,
                "_installed_vllm",
                return_value=expected,
            ) as locate:
                result = patch_module.resolve_vllm_root(interpreter)

            self.assertEqual(result, expected)
            locate.assert_called_once_with(interpreter.absolute())

    def test_fresh_runner_patch_preserves_native_k_wide_zero_buffer(self) -> None:
        source = (
            patch_module.RUNNER_GATE_ORIGINAL
            + "\n"
            + patch_module.EMPTY_DRAFTS_ORIGINAL
        )

        patched = patch_module.patch_runner_source(source)

        self.assertIn(patch_module.RUNNER_GATE_MARKER, patched)
        self.assertIn(patch_module.EMPTY_DRAFTS_ORIGINAL, patched)
        self.assertNotIn("DFLASH_CONTEXT_CUTOFF_EMPTY_DRAFTS", patched)

    def test_runner_patch_migrates_legacy_zero_width_buffer(self) -> None:
        source = (
            patch_module.RUNNER_GATE_PATCHED
            + "\n"
            + patch_module.LEGACY_EMPTY_DRAFTS_PATCHED
        )

        patched = patch_module.patch_runner_source(source)

        self.assertIn(patch_module.EMPTY_DRAFTS_ORIGINAL, patched)
        self.assertNotIn("DFLASH_CONTEXT_CUTOFF_EMPTY_DRAFTS", patched)

    def test_runner_patch_is_idempotent_after_migration(self) -> None:
        source = (
            patch_module.RUNNER_GATE_ORIGINAL
            + "\n"
            + patch_module.EMPTY_DRAFTS_ORIGINAL
        )
        patched = patch_module.patch_runner_source(source)

        self.assertEqual(patch_module.patch_runner_source(patched), patched)


if __name__ == "__main__":
    unittest.main()
