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
