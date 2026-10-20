"""Hook configuration is modified only in disposable fixture repositories."""
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
spec = importlib.util.spec_from_file_location("dm_hook_install", Path(__file__).resolve().parents[1] / "hooks/install.py")
hooks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hooks)


class HookTests(unittest.TestCase):
    def test_install_status_remove_and_preserve_existing_hook_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            hook_dir = root / "scripts/hooks"
            hook_dir.mkdir(parents=True)
            (hook_dir / "pre-commit").write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            subprocess.run(["git", "init", str(root)], check=True, capture_output=True)
            with patch.object(hooks, "ROOT", root), patch.object(hooks, "HOOKS", hook_dir), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(hooks.main(["--status"]), 0)
                self.assertEqual(hooks.main([]), 0)
                self.assertEqual(hooks.git("config", "--local", "--get", "core.hooksPath").stdout.strip(), "scripts/hooks")
                self.assertEqual(hooks.main(["--uninstall"]), 0)
                hooks.git("config", "--local", "core.hooksPath", "existing-hooks")
                self.assertEqual(hooks.main([]), 2)
                self.assertEqual(hooks.main(["--uninstall"]), 2)
                self.assertEqual(hooks.git("config", "--local", "--get", "core.hooksPath").stdout.strip(), "existing-hooks")


if __name__ == "__main__":
    unittest.main()
