"""Offline regression coverage for snapshot integrity and filtering."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "dumps"))
import refresh_repositories as refresh


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.target = self.directory / "Fixture.txt"

    def run_refresh(self, writer, **kwargs):
        with patch.object(refresh, "_write_snapshot", side_effect=writer):
            return refresh.refresh_one("Fixture.txt", "https://github.com/example/source",
                                       repositories_dir=self.directory, **kwargs)

    def test_failed_download_keeps_old_snapshot_and_cleans_temporary(self):
        self.target.write_bytes(b"old" * 100)
        def fail(url, output, **kwargs):
            output.write_bytes(b"partial")
            raise RuntimeError("network failed")
        result = self.run_refresh(fail)
        self.assertEqual(result.status, "FAIL")
        self.assertEqual(self.target.read_bytes(), b"old" * 100)
        self.assertEqual(list(self.directory.iterdir()), [self.target])

    def test_empty_result_cannot_replace_snapshot(self):
        self.target.write_bytes(b"old")
        result = self.run_refresh(lambda url, output, **kw: output.write_bytes(b""))
        self.assertEqual(result.status, "FAIL")
        self.assertEqual(self.target.read_bytes(), b"old")

    def test_shrink_guard_and_explicit_override(self):
        self.target.write_bytes(b"a" * 1000)
        writer = lambda url, output, **kw: output.write_bytes(b"b" * 100)
        self.assertEqual(self.run_refresh(writer).status, "FAIL")
        self.assertEqual(len(self.target.read_bytes()), 1000)
        self.assertEqual(self.run_refresh(writer, force_shrink=True).status, "OK")
        self.assertEqual(self.target.read_bytes(), b"b" * 100)

    def test_success_replaces_same_filename(self):
        self.target.write_bytes(b"old")
        result = self.run_refresh(lambda url, output, **kw: output.write_bytes(b"new contents"))
        self.assertEqual(result.status, "OK")
        self.assertEqual(self.target.read_bytes(), b"new contents")

    def test_failed_atomic_swap_keeps_old_file(self):
        self.target.write_bytes(b"old")
        with patch.object(refresh.os, "replace", side_effect=PermissionError("locked")):
            result = self.run_refresh(lambda url, output, **kw: output.write_bytes(b"new contents"))
        self.assertEqual(result.status, "FAIL")
        self.assertEqual(self.target.read_bytes(), b"old")

    def test_weights_data_outputs_and_tokenizers_excluded(self):
        patterns = refresh.entry_patterns({})
        for path in ["model.safetensors", "data/train.jsonl", "tokenizer.json", "outputs/run.json",
                     "results/eval.json", "v1/results/games/run.json", "bench/outputs/run.json",
                     "v1/responses/calls.json", "v1/checkpoints/config.json",
                     "model.safetensors.index.json", "archive.zip"]:
            with self.subTest(path=path):
                self.assertFalse(refresh._selected(path, 100, patterns))

    def test_source_configs_scripts_patches_notices_retained(self):
        patterns = refresh.entry_patterns({})
        for path in ["data/generators/train.py", "configs/train.json", "training/train.sbatch",
                     "scripts/start.sh", "fix.patch", "responses/LICENSE_RESPONSES.md",
                     "v1/results/LICENSE_DATA.md", "LICENSE", "NOTICE"]:
            with self.subTest(path=path):
                self.assertTrue(refresh._selected(path, 100, patterns))

    def test_anyjev_keeps_evaluation_code_but_not_recorded_runs(self):
        patterns = refresh.entry_patterns(refresh.REPOSITORIES["AnyJev.txt"])
        for path in ["bench/results_v01/2026-09-22/model.json",
                     "bench/results_layout/run.json", "bench/llamacpp_parity_f16.json"]:
            with self.subTest(path=path):
                self.assertFalse(refresh._selected(path, 100, patterns))
        self.assertTrue(refresh._selected("scripts/eval_tacit.py", 100, patterns))

    def test_flattening_retains_selected_files_ignored_by_gitingest_defaults(self):
        bodies = {
            "deploy/sagemaker/bin/cdk-app.ts": b"export const deployment = true;\n",
            "deploy/sagemaker/package-lock.json": b'{"lockfileVersion": 3}\n',
            "scripts/run.sh": b"#!/bin/sh\nprintf ready\n",
            "results/LICENSE_DATA.md": b"Fixture data license notice\n",
            "results/run.json": b'{"generated": true}\n',
        }
        files = [{"path": path, "size": len(body), "url": path}
                 for path, body in bodies.items()]
        provenance = {"upstream": "https://github.com/example/source",
                      "revision": "abc123", "revision_date": "2026-10-20",
                      "slug": "example/source"}
        with patch.object(refresh, "_remote_tree", return_value=(provenance, files)), \
             patch.object(refresh, "_get", side_effect=lambda url, *args: (bodies[url], {})):
            refresh._write_snapshot("https://github.com/example/source", self.target,
                                    timeout=5, patterns=refresh.entry_patterns({}))
        text = self.target.read_text(encoding="utf-8")
        for path, body in bodies.items():
            with self.subTest(path=path):
                if path == "results/run.json":
                    self.assertNotIn("FILE: " + path + "\n", text)
                else:
                    self.assertIn("FILE: " + path + "\n", text)
                    self.assertIn(body.decode(), text)

    def test_large_selected_file_is_excluded(self):
        self.assertFalse(refresh._selected("config.json", refresh._MAX_FILE_BYTES + 1, refresh.entry_patterns({})))

    def test_targets_preserve_names_deduplicate_and_reject_unknown(self):
        self.assertEqual(refresh._resolve_targets(["JevOut", "JevOut.txt", "SearchJev"]), ["JevOut.txt", "SearchJev.txt"])
        with self.assertRaises(ValueError):
            refresh._resolve_targets(["unknown"])

    def test_path_escape_refused(self):
        result = refresh.refresh_one("../outside.txt", "https://github.com/example/source", repositories_dir=self.directory)
        self.assertEqual(result.status, "FAIL")
        self.assertEqual(list(self.directory.iterdir()), [])

    def test_oversize_snapshot_needs_explicit_gitignore(self):
        writer = lambda url, output, **kw: output.write_bytes(b"x" * 20)
        with patch.object(refresh, "_GIT_LIMIT", 10):
            self.assertEqual(self.run_refresh(writer).status, "FAIL")
            ignore = self.directory.parent / ".gitignore"
            # Keep the fixture ignore file inside the test's own temporary folder.
            nested = self.directory / "repositories"
            nested.mkdir()
            (self.directory / ".gitignore").write_text("/repositories/Fixture.txt\n")
            with patch.object(refresh, "_write_snapshot", side_effect=writer):
                result = refresh.refresh_one("Fixture.txt", "https://github.com/example/source", repositories_dir=nested)
            self.assertEqual(result.status, "OK")

    def test_revision_requires_exactly_one_target(self):
        with self.assertRaises(ValueError):
            refresh.refresh_all(revision="abc123")


if __name__ == "__main__":
    unittest.main()
