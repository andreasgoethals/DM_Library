"""Stage orchestration is tested without network or writes to the real library."""
import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("dm_maintain", Path(__file__).resolve().parents[1] / "maintain.py")
maintenance = importlib.util.module_from_spec(spec)
spec.loader.exec_module(maintenance)


class MaintenanceTests(unittest.TestCase):
    def test_only_skip_and_check_only_selection(self):
        calls = []
        def stage(name, argv):
            calls.append((name, argv))
            return 0, 0.0, ""
        with patch.object(maintenance, "run_stage", stage), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(maintenance.main(["--check-only", "--only", "text", "--only", "repos", "--only", "docs", "--skip", "docs"]), 0)
        self.assertEqual([name for name, _ in calls], ["text"])
        self.assertIn("--check", calls[0][1])

    def test_failures_are_aggregated_and_do_not_stop_later_checks(self):
        calls = []
        def stage(name, argv):
            calls.append(name)
            return (2 if name == "docs" else 0), 0.0, ""
        with patch.object(maintenance, "run_stage", stage), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(maintenance.main(["--only", "docs", "--only", "symbols"]), 1)
        self.assertEqual(calls, ["docs", "symbols"])

    def test_post_refresh_rechecks_run_once_after_all_mutating_stages(self):
        stages = {
            "first": {"command": ["first.py"], "mutating": True, "description": "first", "post_checks": ["check", "docs"]},
            "second": {"command": ["second.py"], "mutating": True, "description": "second", "post_checks": ["check"]},
            "check": {"command": ["check.py"], "description": "check", "strict_review": True},
            "docs": {"command": ["docs.py"], "description": "docs"},
        }
        calls = []
        def stage(name, argv):
            calls.append((name, argv))
            return 0, 0.0, ""
        probe = subprocess.CompletedProcess([], 0, stdout="", stderr="")
        with patch.dict(maintenance.CONFIG, {"stages": stages}), \
             patch.object(maintenance, "STAGES", {name: ([sys.executable, "-B", *item["command"]], item.get("mutating", False), item["description"]) for name, item in stages.items()}), \
             patch.object(maintenance.subprocess, "run", return_value=probe), \
             patch.object(maintenance, "run_stage", stage), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(maintenance.main(["--only", "first", "--only", "second", "--strict-review"]), 0)
        self.assertEqual([name for name, _ in calls], ["first", "second", "check", "docs"])
        self.assertEqual(calls[2][1][-1], "--strict-review")
        self.assertNotIn("--strict-review", calls[3][1])

    def test_subprocess_imports_leave_no_bytecode(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "local_module.py").write_text("value = 42\n", encoding="utf-8")
            (root / "check.py").write_text("import local_module\nassert local_module.value == 42\n", encoding="utf-8")
            before = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
            with patch.object(maintenance, "_ROOT", root):
                code, _, output = maintenance.run_stage("fixture", [sys.executable, str(root / "check.py")])
            self.assertEqual(code, 0, output)
            self.assertEqual(before, sorted(path.relative_to(root).as_posix() for path in root.rglob("*")))


if __name__ == "__main__":
    unittest.main()
