#!/usr/bin/env python
"""Check cited upstream symbols/source paths and reject unstable dump line citations."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.library import REPOSITORIES, ROOT

DOCS = ["REPOSITORIES.md", "SUMMARIES.md", "SYNTHESIS.md"]
SECTIONED = {"REPOSITORIES.md"}
_DUMP = re.compile(r"`(?:repositories/)?([^`\n/]+\.txt)`")
_TICK = re.compile(r"`([^`\n]+)`")
_LINE_CITE = re.compile(r"`([^`\n]+\.txt):(?:L)?\d+(?:[-:]\d+)?`")
_CODE_SHAPES = (
    re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\(\)$"),
    re.compile(r"^[A-Za-z_][A-Za-z0-9_]*_[A-Za-z0-9_]+$"),
    re.compile(r"^[a-z][A-Za-z0-9]*[A-Z][A-Za-z0-9]*$"),
    re.compile(r"^[A-Z][a-z0-9]+[A-Z][A-Za-z0-9]*$"),
    re.compile(r"^[\w./-]+\.(?:py|jl|R|cpp|cc|c|h|hpp|sh|yaml|yml|toml|json|patch|ini|cfg)$"),
    re.compile(r"^[\w.-]+(?:/[\w.-]+)+/?$"),
)
_IGNORE = {"PROJECT_SPECIFIC.md", "requirements.txt", "gitingest", "FILE:"}
_IGNORE_PREFIX = ("papers/", "scripts/", "repositories/", "https://", "http://", "arXiv:")


def own_code_symbols() -> set[str]:
    out = set()
    for path in (ROOT / "scripts").rglob("*.py"):
        source = path.read_text(encoding="utf-8", errors="replace")
        out.update(re.findall(r"^\s*(?:def|class)\s+(\w+)", source, re.M))
        out.update(re.findall(r"^([A-Z][A-Z0-9_]{3,})\s*[:=]", source, re.M))
    return out


def is_symbol(token: str, own: set[str] | None = None) -> bool:
    token = token.strip()
    if token in _IGNORE or token in (own or set()) or token.startswith(_IGNORE_PREFIX):
        return False
    if token.endswith((".txt", ".md", ".pdf", ".ipynb")) or " " in token or "XXX" in token:
        return False
    if re.match(r"^[\w.-]+/[\w.-]+$", token) and "." not in token.split("/")[-1]:
        return False  # owner/repository remote identity
    return any(pattern.match(token) for pattern in _CODE_SHAPES)


def dump_names(text: str) -> list[str]:
    return _DUMP.findall(text)


def dump_sections(text: str) -> list[tuple[list[str], str]]:
    heads = list(re.finditer(r"^(#{2,6})\s+(.*)$", text, re.M))
    out = []
    stack = []
    for i, match in enumerate(heads):
        level, names = len(match.group(1)), dump_names(match.group(2))
        while stack and stack[-1][0] >= level:
            stack.pop()
        if names:
            stack.append((level, names))
        current = names or (stack[-1][1] if stack else [])
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        if current:
            out.append((current, text[match.end():end]))
    return out


def paragraph_sections(text: str) -> list[tuple[list[str], str]]:
    return [(dump_names(para), para) for para in re.split(r"\n\s*\n", text) if dump_names(para)]


def collect(doc: str) -> dict[str, set[str]]:
    text = (ROOT / doc).read_text(encoding="utf-8")
    own = own_code_symbols()
    sections = dump_sections(text) if doc in SECTIONED else paragraph_sections(text)
    # Overview-table rows also carry concrete source maps.
    if doc in SECTIONED:
        sections += [(dump_names(line), line) for line in text.splitlines()
                     if line.startswith("|") and dump_names(line)]
    cited: dict[str, set[str]] = {}
    for names, body in sections:
        for line in body.splitlines():
            # An explicit same-line attribution is more precise than the enclosing heading.
            here = set(dump_names(line) or names)
            for token in _TICK.findall(line):
                if is_symbol(token, own):
                    cited.setdefault(token.strip().removesuffix("()"), set()).update(here)
    return cited


def line_citations(docs: list[str] | None = None) -> list[tuple[str, int, str]]:
    out = []
    for doc in docs or DOCS:
        path = ROOT / doc
        if path.is_file():
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                out.extend((doc, number, match.group()) for match in _LINE_CITE.finditer(line))
    return out


def symbol_present(symbol: str, text: str) -> bool:
    if re.fullmatch(r"\w+", symbol):
        return re.search(r"(?<![A-Za-z0-9_])" + re.escape(symbol) + r"(?![A-Za-z0-9_])", text) is not None
    return symbol in text


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--doc", action="append", default=[], choices=DOCS)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args(argv)
    docs = args.doc or DOCS
    cited: dict[str, set[str]] = {}
    named = set()
    problems = []
    for doc in docs:
        path = ROOT / doc
        if not path.is_file():
            problems.append(f"missing document: {doc}")
            continue
        named.update(dump_names(path.read_text(encoding="utf-8")))
        for symbol, candidates in collect(doc).items():
            cited.setdefault(symbol, set()).update(candidates)
    bodies = {}
    for name in sorted(named):
        path = REPOSITORIES / name
        if path.is_file():
            bodies[name] = path.read_text(encoding="utf-8", errors="replace")
        else:
            problems.append(f"cited snapshot is unavailable: repositories/{name}; regenerate it before validating citations")
    for symbol, names in sorted(cited.items()):
        found = next((name for name in sorted(names) if name in bodies and symbol_present(symbol, bodies[name])), None)
        if found and args.verbose:
            print(f"[OK] {symbol} in {found}")
        elif not found:
            problems.append(f"{symbol} absent from attributed snapshot(s): {', '.join(sorted(names))}")
    problems.extend(f"{doc}:{number}: unstable line-number citation {cite}" for doc, number, cite in line_citations(docs))
    for problem in problems:
        print("[PROBLEM] " + problem)
    print(f"Symbol check: {len(cited)} distinct symbols, {len(named)} snapshots, {len(problems)} problem(s).")
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())
