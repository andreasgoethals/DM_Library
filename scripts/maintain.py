#!/usr/bin/env python
"""Run DM Library maintenance; --check-only never writes library content."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

# Set this before importing local modules, including on direct invocation.
sys.dont_write_bytecode = True
_ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = _ROOT / "scripts"
sys.path.insert(0, str(_SCRIPTS))
from lib.config import LIBRARY_NAME

STAGES = {
    "text": ([sys.executable, "-B", str(_SCRIPTS / "papers/extract_paper_text.py"), "--all"], True, "extract missing paper text"),
    "docs": ([sys.executable, "-B", str(_SCRIPTS / "checks/check_docs.py"), "--quiet"], False, "coverage, chronology, links and neutrality"),
    "symbols": ([sys.executable, "-B", str(_SCRIPTS / "checks/check_symbols.py")], False, "verify cited upstream symbols and paths"),
    "zotero": ([sys.executable, "-B", str(_SCRIPTS / "checks/check_zotero_sync.py")], False, "compare the selected Zotero corpus"),
    "versions": ([sys.executable, "-B", str(_SCRIPTS / "checks/check_paper_versions.py")], False, "report newer arXiv versions"),
    "repos": ([sys.executable, "-B", str(_SCRIPTS / "dumps/refresh_repositories.py")], True, "refresh registered upstream snapshots"),
}
CHECK_ONLY_OVERRIDE = {
    "text": [sys.executable, "-B", str(_SCRIPTS / "papers/extract_paper_text.py"), "--check"],
}


def run_stage(name: str, argv: list[str]) -> tuple[int, float, str]:
    started = time.monotonic()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    try:
        proc = subprocess.run(argv, cwd=_ROOT, env=env, capture_output=True,
                              text=True, encoding="utf-8", errors="replace")
        return proc.returncode, time.monotonic() - started, (proc.stdout or "") + (proc.stderr or "")
    except OSError as exc:
        return 2, time.monotonic() - started, str(exc)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check-only", action="store_true", help="report only; skip snapshot refresh and check extraction parity")
    ap.add_argument("--skip", action="append", default=[], choices=list(STAGES), metavar="STAGE")
    ap.add_argument("--only", action="append", default=[], choices=list(STAGES), metavar="STAGE")
    ap.add_argument("--quiet", action="store_true", help="suppress stage output and print the result summary")
    args = ap.parse_args(argv)
    selected = [s for s in STAGES if (not args.only or s in args.only) and s not in args.skip]
    excluded = [s for s in selected if args.check_only and STAGES[s][1] and s not in CHECK_ONLY_OVERRIDE]
    selected = [s for s in selected if s not in excluded]
    print(f"{LIBRARY_NAME} maintenance" + (" (read-only)" if args.check_only else ""))
    print("Stages: " + (", ".join(selected) or "(none)"))
    if excluded:
        print("Skipped mutating stages: " + ", ".join(excluded))
    results = []
    for name in selected:
        cmd = CHECK_ONLY_OVERRIDE.get(name, STAGES[name][0]) if args.check_only else STAGES[name][0]
        print(f"\n>>> [{name}] {STAGES[name][2]}", flush=True)
        code, elapsed, output = run_stage(name, cmd)
        if not args.quiet and output.strip():
            print(output.rstrip())
        print(f"[{name}] {'OK' if code == 0 else 'ATTENTION'} (exit {code}, {elapsed:.1f}s)", flush=True)
        results.append((name, code))
        # A refresh can invalidate citations. Validate after successful writes too.
        if name == "repos" and code == 0 and "symbols" not in args.skip:
            post_code, elapsed, output = run_stage("symbols", STAGES["symbols"][0])
            if not args.quiet and output.strip():
                print(output.rstrip())
            print(f"[symbols after refresh] {'OK' if post_code == 0 else 'ATTENTION'} (exit {post_code}, {elapsed:.1f}s)")
            results.append(("symbols after refresh", post_code))
    failed = [name for name, code in results if code != 0]
    print("\n" + ("Needs attention: " + ", ".join(failed) if failed else "All selected stages passed."))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
