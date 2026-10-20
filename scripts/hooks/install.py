#!/usr/bin/env python
"""Install, inspect or remove the versioned offline Git hook in this checkout."""
from __future__ import annotations
import argparse
import os
from pathlib import Path
import stat
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
HOOKS = Path(__file__).resolve().parent
REL = "scripts/hooks"


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--uninstall", action="store_true")
    group.add_argument("--status", action="store_true")
    args = ap.parse_args(argv)
    if git("rev-parse", "--git-dir").returncode:
        print("ERROR: this checkout is not a Git repository.", file=sys.stderr)
        return 2
    result = git("config", "--local", "--get", "core.hooksPath")
    current = result.stdout.strip()
    if args.status:
        print(f"core.hooksPath = {current or '(unset)'}")
        return 0
    if current and current != REL:
        print(f"ERROR: preserving existing core.hooksPath={current!r}; change that local setting explicitly first.", file=sys.stderr)
        return 2
    if args.uninstall:
        if current:
            result = git("config", "--local", "--unset", "core.hooksPath")
            if result.returncode:
                print(result.stderr, file=sys.stderr)
                return 2
        print("Library hook uninstalled.")
        return 0
    result = git("config", "--local", "core.hooksPath", REL)
    if result.returncode:
        print(result.stderr, file=sys.stderr)
        return 2
    for hook in HOOKS.iterdir():
        if hook.is_file() and not hook.suffix:
            os.chmod(hook, hook.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP)
    print(f"Installed core.hooksPath={REL}; commits run offline docs/text/symbol checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
