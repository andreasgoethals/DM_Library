"""End-to-end submodule tests use disposable repositories only."""
import contextlib
import hashlib
import importlib.util
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("dm_propagation", Path(__file__).resolve().parents[1] / "propagate_to_downstream.py")
propagation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(propagation)


def git(cwd, *args):
    proc = subprocess.run(["git", "-c", "protocol.file.allow=always", *args], cwd=cwd,
                          capture_output=True, text=True, encoding="utf-8", errors="replace",
                          env=dict(os.environ, GIT_OPTIONAL_LOCKS="0"))
    if proc.returncode:
        raise AssertionError(f"git {args}: {proc.stderr}")
    return proc.stdout.strip()


def configure(repo):
    git(repo, "config", "user.email", "dm-library-fixture@example.invalid")
    git(repo, "config", "user.name", "DM Library Fixture")
    git(repo, "config", "core.hooksPath", str(repo / ".test-no-hooks"))


def fingerprint(root):
    return {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in root.rglob("*") if path.is_file()}


class PropagationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.library = self.root / "library"
        self.remote = self.root / "Decision_Models_Library.git"
        self.consumer = self.root / "consumer"
        self.library.mkdir()
        self.consumer.mkdir()
        git(self.root, "init", "--bare", str(self.remote))
        git(self.library, "init", "-b", "main")
        configure(self.library)
        self.commit_library("first")
        git(self.library, "remote", "add", "origin", str(self.remote))
        git(self.library, "push", "-u", "origin", "main")
        git(self.remote, "symbolic-ref", "HEAD", "refs/heads/main")
        git(self.consumer, "init", "-b", "main")
        configure(self.consumer)
        (self.consumer / "consumer.txt").write_text("initial", encoding="utf-8")
        git(self.consumer, "add", "consumer.txt")
        git(self.consumer, "commit", "-m", "Initial fixture")
        git(self.consumer, "submodule", "add", str(self.remote), "dm-library")
        git(self.consumer, "commit", "-am", "Add fixture submodule")
        self.patch = patch.object(propagation, "_ROOT", self.library)
        self.patch.start()

    def tearDown(self):
        self.patch.stop()
        # Git objects may be read-only on Windows; TemporaryDirectory handles them.
        self.temp.cleanup()

    def commit_library(self, value):
        (self.library / "knowledge.txt").write_text(value, encoding="utf-8")
        git(self.library, "add", "knowledge.txt")
        git(self.library, "commit", "-m", value)
        return git(self.library, "rev-parse", "HEAD")

    def call(self, *args):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return propagation.main(["--root", str(self.root), *args])

    def test_remote_matching_preserves_host(self):
        self.assertEqual(propagation.normalise_remote("git@github.com:Owner/Decision_Models_Library.git"),
                         propagation.normalise_remote("https://github.com/owner/decision_models_library"))
        self.assertNotEqual(propagation.normalise_remote("https://other.example/owner/library"),
                            propagation.normalise_remote("https://github.com/owner/library"))

    def test_dry_run_is_content_read_only_and_discovers_dirty_library(self):
        self.commit_library("second")
        (self.library / "uncommitted.txt").write_text("pending", encoding="utf-8")
        before = fingerprint(self.root)
        self.assertEqual(self.call("--dry-run"), 0)
        self.assertEqual(before, fingerprint(self.root))
        projects = propagation.discover([self.root], propagation.normalise_remote(str(self.remote)), 2)
        self.assertEqual([(project.repo, project.sub_path) for project in projects], [(self.consumer, "dm-library")])

    def test_dirty_and_unpublished_updates_refused(self):
        self.commit_library("unpublished")
        before = git(self.consumer, "rev-parse", "HEAD")
        self.assertEqual(self.call(), 2)
        self.assertEqual(self.call("--allow-dirty"), 2)
        git(self.library, "push")
        (self.library / "knowledge.txt").write_text("dirty", encoding="utf-8")
        self.assertEqual(self.call(), 2)
        self.assertEqual(before, git(self.consumer, "rev-parse", "HEAD"))

    def test_unborn_library_still_allows_read_only_discovery(self):
        unborn = self.root / "unborn"
        unborn.mkdir()
        git(unborn, "init", "-b", "main")
        configure(unborn)
        git(unborn, "remote", "add", "origin", str(self.remote))
        (unborn / "README.md").write_text("initial uncommitted library", encoding="utf-8")
        before = fingerprint(self.root)
        with patch.object(propagation, "_ROOT", unborn):
            self.assertEqual(self.call("--dry-run"), 0)
            self.assertEqual(self.call(), 2)
        self.assertEqual(before, fingerprint(self.root))

    def test_optional_push_updates_only_disposable_consumer_remote(self):
        consumer_remote = self.root / "consumer-origin.git"
        git(self.root, "init", "--bare", str(consumer_remote))
        git(self.consumer, "remote", "add", "origin", str(consumer_remote))
        git(self.consumer, "push", "-u", "origin", "main")
        target = self.commit_library("second")
        git(self.library, "push")
        self.assertEqual(self.call("--push"), 0)
        self.assertEqual(git(consumer_remote, "rev-parse", "main"), git(self.consumer, "rev-parse", "HEAD"))
        self.assertIn(target, git(consumer_remote, "ls-tree", "main", "dm-library"))

    def test_exact_older_published_commit_and_unrelated_staging_preserved(self):
        target = self.commit_library("second")
        self.commit_library("third")
        git(self.library, "push")
        git(self.library, "checkout", "--detach", target)
        (self.consumer / "unrelated.txt").write_text("keep staged", encoding="utf-8")
        git(self.consumer, "add", "unrelated.txt")
        (self.consumer / "consumer.txt").write_text("keep unstaged", encoding="utf-8")
        self.assertEqual(self.call(), 0)
        self.assertEqual(git(self.consumer / "dm-library", "rev-parse", "HEAD"), target)
        self.assertEqual(git(self.consumer, "show", "--format=", "--name-only", "HEAD"), "dm-library")
        self.assertEqual(git(self.consumer, "diff", "--cached", "--name-only"), "unrelated.txt")
        self.assertEqual(git(self.consumer, "diff", "--name-only"), "consumer.txt")

    def test_dirty_downstream_submodule_preserved(self):
        self.commit_library("second")
        git(self.library, "push")
        sub = self.consumer / "dm-library"
        (sub / "knowledge.txt").write_text("local consumer edit", encoding="utf-8")
        before = git(self.consumer, "rev-parse", "HEAD")
        self.assertEqual(self.call(), 1)
        self.assertEqual(before, git(self.consumer, "rev-parse", "HEAD"))
        self.assertEqual((sub / "knowledge.txt").read_text(encoding="utf-8"), "local consumer edit")

    def test_reconfigured_submodule_origin_refused(self):
        self.commit_library("second")
        git(self.library, "push")
        sub = self.consumer / "dm-library"
        wrong_remote = self.root / "unrelated.git"
        git(self.root, "init", "--bare", str(wrong_remote))
        git(sub, "remote", "set-url", "origin", str(wrong_remote))
        before = git(self.consumer, "rev-parse", "HEAD")
        self.assertEqual(self.call(), 1)
        self.assertEqual(before, git(self.consumer, "rev-parse", "HEAD"))

    def test_pending_registration_preserved(self):
        self.commit_library("second")
        git(self.library, "push")
        path = self.consumer / ".gitmodules"
        path.write_text(path.read_text() + "\n# pending owner registration\n")
        before = git(self.consumer, "rev-parse", "HEAD")
        self.assertEqual(self.call(), 1)
        self.assertEqual(before, git(self.consumer, "rev-parse", "HEAD"))
        self.assertIn("pending owner", path.read_text())

    def test_push_refuses_unrelated_unpublished_consumer_commit(self):
        remote = self.root / "consumer-origin.git"
        git(self.root, "init", "--bare", str(remote))
        git(self.consumer, "remote", "add", "origin", str(remote))
        git(self.consumer, "push", "-u", "origin", "main")
        before = git(remote, "rev-parse", "main")
        (self.consumer / "consumer.txt").write_text("unrelated owner work")
        git(self.consumer, "commit", "-am", "Unrelated owner work")
        self.commit_library("second")
        git(self.library, "push")
        self.assertEqual(self.call("--push"), 1)
        self.assertEqual(before, git(remote, "rev-parse", "main"))
        self.assertIn("unrelated owner", (self.consumer / "consumer.txt").read_text())

    def test_project_filter_does_not_install_any_other_library(self):
        self.commit_library("second")
        git(self.library, "push")
        before = fingerprint(self.consumer)
        self.assertEqual(self.call("--project", "another-consumer"), 0)
        self.assertEqual(before, fingerprint(self.consumer))


if __name__ == "__main__":
    unittest.main()
