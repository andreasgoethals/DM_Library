"""Refresh registered source snapshots, preserving filenames and previous good files.

Adapted from the reference library's atomic replacement, shrink guard, repeatable
--only and --timeout workflow. Remote trees are resolved to immutable revisions
before selected source files are downloaded: weights and datasets are never cloned.
Gitingest flattens that selected local tree. No downloaded code is executed.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timezone
import fnmatch
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile
import time
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.config import USER_AGENT

_SHRINK_GUARD_RATIO = 0.5
_DEFAULT_TIMEOUT_SECONDS = 180
_MAX_FILE_BYTES = 2_000_000
_GIT_LIMIT = 95_000_000
_TEXT = {"*.py", "*.md", "*.rst", "*.toml", "*.txt", "*.yaml", "*.yml",
         "*.cfg", "*.ini", "*.json", "*.sh", "*.bash", "*.ps1", "*.patch",
         "*.diff", "*.jinja", "*.cff", "*.slurm", "*.sbatch", "*.js", "*.ts",
         "*.tsx", "*.html", "*.css", "*.lock", "LICENSE*", "NOTICE*",
         "COPYING*", "THIRD_PARTY*", "Makefile", "Dockerfile", "MANIFEST.in"}
_EXCLUDE = {"tokenizer.json", "*.safetensors.index.json", "results/*", "outputs/*",
            "responses/*", "checkpoints/*", "weights/*", "logs/*", "cache/*",
            "*/results/*", "*/outputs/*", "*/responses/*", "*/checkpoints/*",
            "*/weights/*", "*/logs/*", "*/cache/*",
            "paper/*", "assets/*", "tests/cassettes/*", "tests/expected_responses/*",
            "training/aws/*", "*/stats.json"}

REPOSITORIES: dict[str, dict] = {
    "JevOut.txt": {"url": "https://github.com/xzx34/JevOut", "identity": "https://arxiv.org/html/2609.30243v1"},
    "SearchJev.txt": {"url": "https://github.com/EvoScientist/SearchJev", "identity": "https://arxiv.org/html/2610.05107v1"},
    "SIIDecision.txt": {"url": "https://github.com/amazingljy1206/SII-Decision", "identity": "https://arxiv.org/html/2610.03935v2"},
    "JevBenchmarking.txt": {"url": "https://github.com/AppliedMachineLearning-Lab/jev-benchmarking", "identity": "https://arxiv.org/html/2609.37647v1"},
    "StrandsDecider.txt": {"url": "https://github.com/strands-labs/strands-decider", "identity": "https://strandsagents.com/blog/introducing-strands-decider/"},
    "InternDecision.txt": {"url": "https://github.com/InternLM/Intern-Decision", "identity": "https://huggingface.co/internlm/Intern-Decision-4B"},
    "TypeSafeSystemOneAdapter.txt": {"url": "https://github.com/typesafe-ai/system-one-adapter-python", "identity": "https://typesafe.ai/blog/introducing-system-one-models-and-jev"},
    "Clef.txt": {"url": "https://huggingface.co/Cloudflare/clef", "identity": "https://blog.cloudflare.com/clef-decision-models/"},
    "LiquidD1_3B.txt": {"url": "https://huggingface.co/LiquidAI/d1-3B", "identity": "https://www.liquid.ai/blog/d1-open"},
    "LiquidD1_Omni600M.txt": {"url": "https://huggingface.co/LiquidAI/d1-omni-600M", "identity": "https://www.liquid.ai/blog/d1-open"},
    "PerplexityDecider.txt": {"url": "https://huggingface.co/perplexity-ai/pplx-decider-v1.1-27b", "identity": "https://huggingface.co/perplexity-ai/pplx-decider-v1.1-27b"},
    "AnyJev.txt": {"url": "https://github.com/nokia-applied-research/AnyJev", "identity": "https://arxiv.org/html/2610.00831v1",
                   "exclude": ["bench/results*/*", "bench/outputs/*", "bench/runs/*", "bench/*parity*.json", "space/*"]},
    "StartLuxDecision.txt": {"url": "https://github.com/StartLuxLabs/StartLux-Decision", "identity": "https://arxiv.org/html/2610.17309v1"},
}
# No inherited infrastructure or manual-refresh exceptions.
SKIP_MANUAL: dict[str, str] = {}
SKIP_NON_GIT: dict[str, str] = {}


@dataclass
class _Result:
    filename: str
    url: str | None
    status: str
    size_kb: float | None = None
    elapsed: float | None = None
    reason: str | None = None


def _default_repositories_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "repositories"


def entry_url(entry: str | dict) -> str:
    return entry if isinstance(entry, str) else entry["url"]


def entry_patterns(entry: str | dict) -> dict[str, set[str]]:
    entry = {} if isinstance(entry, str) else entry
    return {"include_patterns": set(entry.get("include", _TEXT)),
            "exclude_patterns": _EXCLUDE | set(entry.get("exclude", []))}


def _license(path: str) -> bool:
    return any(word in PurePosixPath(path).name.upper() for word in ("LICENSE", "LICENCE", "NOTICE", "COPYING"))


def _selected(path: str, size: int, patterns: dict) -> bool:
    """Keep source/configuration and notices, including generators under data/."""
    if size > _MAX_FILE_BYTES:
        return False
    if _license(path):
        return True
    name = PurePosixPath(path).name
    if any(fnmatch.fnmatchcase(path, p) or fnmatch.fnmatchcase(name, p)
           for p in patterns.get("exclude_patterns", ())):
        return False
    return any(fnmatch.fnmatchcase(path, p) or fnmatch.fnmatchcase(name, p)
               for p in patterns.get("include_patterns", _TEXT))


def _get(url: str, timeout: int, max_bytes: int | None = None) -> tuple[bytes, object]:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urlopen(request, timeout=timeout) as response:
        body = response.read(None if max_bytes is None else max_bytes + 1)
        if max_bytes is not None and len(body) > max_bytes:
            raise ValueError(f"Remote file exceeds {max_bytes} bytes: {url}")
        return body, response.headers


def _json(url: str, timeout: int):
    body, headers = _get(url, timeout)
    return json.loads(body), headers


def _remote_tree(url: str, timeout: int, revision: str | None = None) -> tuple[dict, list[dict]]:
    parsed = urlparse(url)
    parts = parsed.path.strip("/").split("/")
    if parsed.scheme != "https" or len(parts) != 2 or parsed.hostname not in {"github.com", "huggingface.co"}:
        raise ValueError(f"Expected a public GitHub or Hugging Face model repository URL: {url}")
    slug = "/".join(parts)
    if parsed.hostname == "github.com":
        # A tree-only shallow clone avoids the unauthenticated GitHub API quota.
        # No checkout and blob:none mean dataset/weight content is not fetched.
        with tempfile.TemporaryDirectory(prefix="dm-tree-") as temp:
            checkout = Path(temp) / "tree"
            env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_LFS_SKIP_SMUDGE="1")

            def git(*args):
                result = subprocess.run(["git", *args], capture_output=True, text=True,
                                        encoding="utf-8", timeout=timeout, env=env)
                if result.returncode:
                    raise RuntimeError(result.stderr.strip())
                return result.stdout.strip()

            git("clone", "--quiet", "--depth=1", "--filter=blob:none", "--no-checkout", url, str(checkout))
            if revision:
                git("-C", str(checkout), "fetch", "--quiet", "--depth=1", "--filter=blob:none", "origin", revision)
            ref = "FETCH_HEAD" if revision else "HEAD"
            sha = git("-C", str(checkout), "rev-parse", ref)
            date = git("-C", str(checkout), "show", "-s", "--format=%cI", sha)
            # Do not request object sizes here: doing so would hydrate blobs.
            listing = git("-C", str(checkout), "ls-tree", "-r", "-z", sha)
            files = []
            for line in listing.split("\0"):
                if not line:
                    continue
                meta, path = line.split("\t", 1)
                if meta.split()[1] == "blob":
                    files.append({"path": path, "size": 0,
                                  "url": f"https://raw.githubusercontent.com/{slug}/{sha}/{quote(path, safe='/')}"})
    else:
        base = f"https://huggingface.co/api/models/{slug}"
        info, _ = _json(f"{base}/revision/{quote(revision or 'main', safe='')}", timeout)
        sha, date = info["sha"], info.get("lastModified")
        next_url = f"{base}/tree/{sha}?recursive=true&limit=1000"
        files = []
        while next_url:
            tree, headers = _json(next_url, timeout)
            files += [{"path": f["path"], "size": f.get("size", 0),
                       "url": f"https://huggingface.co/{slug}/resolve/{sha}/{quote(f['path'], safe='/')}"}
                      for f in tree if f["type"] == "file"]
            match = re.search(r'<([^>]+)>;\s*rel="next"', headers.get("Link", ""))
            next_url = match.group(1) if match else None
            if next_url and urlparse(next_url).hostname != "huggingface.co":
                raise ValueError("Unexpected pagination host")
    return {"upstream": url, "revision": sha, "revision_date": date, "slug": slug}, files


def _write_snapshot(url: str, output: Path, *, timeout: int, patterns: dict,
                    revision: str | None = None) -> None:
    from gitingest import ingest
    from gitingest.utils.ignore_patterns import DEFAULT_IGNORE_PATTERNS
    provenance, remote_files = _remote_tree(url, timeout, revision)
    selected = [f for f in remote_files if _selected(f["path"], f["size"], patterns)]
    if not selected:
        raise ValueError("No source files selected; refusing an empty snapshot")
    with tempfile.TemporaryDirectory(prefix="dm-source-") as temp:
        checkout = Path(temp) / provenance["slug"].replace("/", "-")
        checkout.mkdir()
        checkout = checkout.resolve()

        def download(item):
            path = PurePosixPath(item["path"])
            if path.is_absolute() or ".." in path.parts or "\\" in item["path"] or any(":" in p for p in path.parts):
                raise ValueError("Unsafe upstream path")
            dest = checkout.joinpath(*path.parts)
            # This new private tree never contains symlinks: all fetched blobs
            # are written as ordinary bytes. Validate lexically before mkdir;
            # resolving nonexistent paths races concurrent directory creation
            # on Windows (GetFinalPathNameByHandle partial-path fallbacks).
            if not dest.is_relative_to(checkout):
                raise ValueError(f"Upstream path escapes source directory: {item['path']!r}")
            body, _ = _get(item["url"], timeout, _MAX_FILE_BYTES)
            body.decode("utf-8")  # fail rather than silently drop undecodable source
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(body)
            return {"path": item["path"], "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()}

        with ThreadPoolExecutor(max_workers=8) as pool:
            manifest = list(pool.map(download, selected))
        # The temporary tree already contains only selected source. Gitingest
        # subtracts exact include patterns from its default ignore set; "*" alone
        # does not override exclusions such as bin/ and package-lock.json.
        # Override those defaults without changing global dependency state.
        _, _, content = ingest(source=str(checkout), output=None, include_gitignored=True,
                               include_patterns={"*"} | DEFAULT_IGNORE_PATTERNS,
                               max_file_size=_MAX_FILE_BYTES)
        missing = [f["path"] for f in manifest if f["bytes"] and f"FILE: {f['path']}\n" not in content.replace("\r\n", "\n")]
        if missing:
            raise ValueError(f"Gitingest omitted selected source files: {missing[:8]}")
        provenance["retrieved_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        provenance["identity_source"] = next((e["identity"] for e in REPOSITORIES.values() if e["url"] == url), None)
        provenance["included_files"] = len(manifest)
        provenance["excluded_files"] = len(remote_files) - len(manifest)
        provenance["file_sha256"] = manifest
        header = "DM Library source snapshot\nDo not edit: regenerate with scripts/dumps/refresh_repositories.py\n"
        output.write_text(header + json.dumps(provenance, indent=2, ensure_ascii=False) + "\n\n" + content,
                          encoding="utf-8", newline="\n")


def refresh_one(filename: str, url: str, *, repositories_dir: Path,
                force_shrink: bool = False, timeout: int | None = None,
                patterns: dict[str, set[str]] | None = None, revision: str | None = None) -> _Result:
    if Path(filename).name != filename or not filename.endswith(".txt"):
        return _Result(filename, url, "FAIL", reason="Snapshot name must be a plain .txt filename")
    repositories_dir.mkdir(parents=True, exist_ok=True)
    target = repositories_dir / filename
    fd, temporary = tempfile.mkstemp(prefix=f".{filename}.", suffix=".refresh.tmp", dir=repositories_dir)
    os.close(fd)
    tmp = Path(temporary)
    start = time.monotonic()
    try:
        _write_snapshot(url, tmp, timeout=timeout or _DEFAULT_TIMEOUT_SECONDS,
                        patterns=patterns or entry_patterns({}), revision=revision)
        size = tmp.stat().st_size
        if not size:
            raise ValueError("Snapshot is empty")
        if target.exists() and not force_shrink and size < target.stat().st_size * _SHRINK_GUARD_RATIO:
            raise ValueError("Shrink guard: snapshot is below 50% of the previous size. Existing file kept; review upstream before --force-shrink.")
        if size > _GIT_LIMIT:
            # Refuse an accidental oversized unignored artifact; callers can register
            # an exact ignore entry first, then rerun using the documented command.
            ignore = repositories_dir.parent / ".gitignore"
            expected = f"/repositories/{filename}"
            if not ignore.exists() or expected not in ignore.read_text(encoding="utf-8").splitlines():
                raise ValueError(f"Snapshot exceeds 95 MB. Add {expected} to .gitignore, document its regeneration, then rerun.")
        os.replace(tmp, target)
        return _Result(filename, url, "OK", size / 1024, time.monotonic() - start)
    except Exception as exc:
        return _Result(filename, url, "FAIL", reason=f"{type(exc).__name__}: {exc}")
    finally:
        tmp.unlink(missing_ok=True)


def _resolve_targets(only: list[str] | None) -> list[str]:
    if not only:
        return list(REPOSITORIES)
    targets = []
    for name in only:
        candidate = name.strip()
        if candidate not in REPOSITORIES:
            candidate += ".txt"
        if candidate not in REPOSITORIES:
            raise ValueError(f"Unknown repository {name!r}; choose from {', '.join(REPOSITORIES)}")
        if candidate not in targets:
            targets.append(candidate)
    return targets


def refresh_all(*, only: list[str] | None = None, repositories_dir: Path | None = None,
                force_shrink: bool = False, timeout: int | None = _DEFAULT_TIMEOUT_SECONDS,
                revision: str | None = None) -> list[_Result]:
    targets = _resolve_targets(only)
    if revision and len(targets) != 1:
        raise ValueError("--revision requires exactly one --only target")
    results = []
    for filename in targets:
        print(f"Refreshing {filename}", file=sys.stderr, flush=True)
        entry = REPOSITORIES[filename]
        results.append(refresh_one(filename, entry_url(entry), repositories_dir=repositories_dir or _default_repositories_dir(),
                                   force_shrink=force_shrink, timeout=timeout, patterns=entry_patterns(entry), revision=revision))
    return results


def _print_summary(results: list[_Result]) -> None:
    for result in results:
        detail = f"{result.size_kb:.1f} KB" if result.status == "OK" else result.reason
        print(f"[{result.status}] {result.filename}: {detail}")
    print(f"OK: {sum(r.status == 'OK' for r in results)}; FAIL: {sum(r.status == 'FAIL' for r in results)}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", action="append", metavar="FILENAME", help="Repeatable; .txt may be omitted")
    parser.add_argument("--force-shrink", action="store_true", help="Allow shrink below 50%% after reviewing upstream")
    parser.add_argument("--timeout", type=int, default=_DEFAULT_TIMEOUT_SECONDS, help="Timeout in seconds for each HTTP request")
    parser.add_argument("--revision", help="Resolve a particular upstream commit; requires one --only")
    args = parser.parse_args(argv)
    if args.timeout < 1:
        parser.error("--timeout must be positive")
    try:
        from loguru import logger
        logger.disable("gitingest")
    except ImportError:
        pass
    try:
        results = refresh_all(only=args.only, force_shrink=args.force_shrink, timeout=args.timeout, revision=args.revision)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    _print_summary(results)
    return int(any(result.status == "FAIL" for result in results))


if __name__ == "__main__":
    raise SystemExit(main())
