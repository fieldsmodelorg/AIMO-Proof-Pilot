from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
HARNESS = REPO / "evaluation" / "harness"
sys.path.insert(0, str(HARNESS))

from eval_config import load_config  # noqa: E402
from trace_uploader import (  # noqa: E402
    load_hf_token,
    resolve_run_name,
    stage_output_file,
    traces_config,
)


class TracesConfigValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = load_config(REPO / "config.yaml")

    def _load(self, mutate):
        config = copy.deepcopy(self.base)
        mutate(config)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.yaml"
            path.write_text(yaml.safe_dump(config, sort_keys=False))
            return load_config(path)

    def test_base_config_has_valid_traces_section(self):
        self.assertIn("traces", self.base)
        self.assertTrue(self.base["traces"]["enabled"])
        self.assertEqual(
            self.base["traces"]["dataset_repo"],
            "imo2026-challenge/chankhavu-imo-reasoning-traces",
        )

    def test_traces_section_is_optional(self):
        config = self._load(lambda c: c.pop("traces"))
        self.assertNotIn("traces", config)

    def test_unknown_traces_key_rejected(self):
        with self.assertRaisesRegex(ValueError, "traces keys differ"):
            self._load(lambda c: c["traces"].update(bogus=1))

    def test_enabled_flag_must_be_bool(self):
        with self.assertRaisesRegex(ValueError, "traces.enabled"):
            self._load(lambda c: c["traces"].update(enabled="yes"))

    def test_private_flag_must_be_bool(self):
        with self.assertRaisesRegex(ValueError, "traces.private"):
            self._load(lambda c: c["traces"].update(private="no"))

    def test_interval_must_be_positive_int(self):
        with self.assertRaisesRegex(ValueError, "traces.interval_seconds"):
            self._load(lambda c: c["traces"].update(interval_seconds=0))

    def test_enabled_requires_owner_slash_name_repo(self):
        for bad in ("", "no-slash", "a/b/c", "/leading", "trailing/"):
            with self.subTest(repo=bad), self.assertRaisesRegex(
                ValueError, "dataset_repo"
            ):
                self._load(lambda c, bad=bad: c["traces"].update(dataset_repo=bad))

    def test_enabled_allows_empty_secrets_file(self):
        # "" -> use the ambient HF token; valid when enabled.
        config = self._load(lambda c: c["traces"].update(secrets_file=""))
        self.assertEqual(config["traces"]["secrets_file"], "")

    def test_disabled_skips_repo_and_secrets_checks(self):
        # A disabled section with empty fields is still valid (nothing runs).
        config = self._load(
            lambda c: c["traces"].update(
                enabled=False, dataset_repo="", secrets_file=""
            )
        )
        self.assertFalse(config["traces"]["enabled"])


class TracesConfigAccessorTests(unittest.TestCase):
    def test_returns_section_when_enabled(self):
        config = {"traces": {"enabled": True, "dataset_repo": "a/b"}}
        self.assertEqual(traces_config(config), config["traces"])

    def test_returns_none_when_disabled(self):
        self.assertIsNone(traces_config({"traces": {"enabled": False}}))

    def test_returns_none_when_absent(self):
        self.assertIsNone(traces_config({}))


class LoadHfTokenTests(unittest.TestCase):
    def _write(self, name, content):
        tmp = tempfile.mkdtemp()
        path = Path(tmp) / name
        path.write_text(content)
        return path

    def test_reads_json(self):
        path = self._write("SECRETS.json", '{"hf_token": "hf_json"}')
        self.assertEqual(load_hf_token(str(path)), "hf_json")

    def test_reads_yaml(self):
        path = self._write("SECRETS.yaml", "hf_token: hf_yaml\n")
        self.assertEqual(load_hf_token(str(path)), "hf_yaml")

    def test_accepts_alternate_key(self):
        path = self._write("s.json", '{"huggingface_token": "hf_alt"}')
        self.assertEqual(load_hf_token(str(path)), "hf_alt")

    def test_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            load_hf_token("/nonexistent/SECRETS.json")

    def test_missing_token_key_raises(self):
        path = self._write("s.json", '{"something_else": "x"}')
        with self.assertRaisesRegex(ValueError, "no token"):
            load_hf_token(str(path))


class ResolveRunNameTests(unittest.TestCase):
    def test_empty_derives_from_target_basename(self):
        self.assertEqual(
            resolve_run_name("", Path("/tmp/chankhavu/models/opd-32b-bf16-step-225")),
            "opd-32b-bf16-step-225",
        )

    def test_explicit_is_stripped(self):
        self.assertEqual(
            resolve_run_name("  my-run/ ", Path("/x/opd-32b-deploy")), "my-run"
        )


class StageOutputFileTests(unittest.TestCase):
    def test_copies_submission_into_artifacts_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = root / "out" / "submission.csv"
            out.parent.mkdir(parents=True)
            out.write_text("id,proof\n1,done\n", encoding="utf-8")
            artifacts = root / "artifacts"
            artifacts.mkdir()
            stage_output_file(out, artifacts)
            staged = artifacts / "submission.csv"
            self.assertTrue(staged.is_file())
            self.assertEqual(staged.read_text(encoding="utf-8"), out.read_text(encoding="utf-8"))

    def test_noop_when_none_or_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            artifacts = Path(tmp)
            stage_output_file(None, artifacts)  # must not raise
            stage_output_file(artifacts / "nope.csv", artifacts)  # missing -> no-op
            self.assertFalse((artifacts / "nope.csv").exists())


if __name__ == "__main__":
    unittest.main()
