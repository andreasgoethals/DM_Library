#!/usr/bin/env python
"""Extract PDF text into papers/text/<year>/<same-name>.txt (never edit by hand)."""
from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.library import ROOT as _ROOT, PAPERS as _PAPERS, TEXT as _TEXT


def text_path_for(pdf: Path) -> Path:
    pdf = pdf.resolve()
    if (pdf.parent.parent != _PAPERS.resolve() or len(pdf.parent.name) != 4
            or not pdf.parent.name.isdigit() or pdf.suffix.lower() != ".pdf"):
        raise ValueError(f"expected papers/<four-digit-year>/<file>.pdf, got {pdf}")
    return _TEXT / pdf.parent.name / (pdf.stem + ".txt")


def iter_pdfs() -> list[Path]:
    return sorted(p for p in _PAPERS.glob("*/*.pdf")
                  if len(p.parent.name) == 4 and p.parent.name.isdigit())


def _strip_line_number_gutters(text: str, min_run: int = 8) -> str:
    lines = text.split("\n")
    keep = [True] * len(lines)
    run: list[int] = []
    for i, line in enumerate(lines + [""]):
        if line.strip().isdigit():
            run.append(i)
            continue
        if len(run) >= min_run:
            for j in run:
                keep[j] = False
        run = []
    return "\n".join(line for line, yes in zip(lines, keep) if yes)


def pdf_text(pdf: Path) -> tuple[str, int]:
    from pypdf import PdfReader
    reader = PdfReader(str(pdf))
    text = "\n\n".join(page.extract_text() or "" for page in reader.pages)
    text = "".join(ch for ch in text if ch in "\n\t" or ord(ch) >= 32)
    return _strip_line_number_gutters(text), len(reader.pages)


def atomic_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix="." + path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(body)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        Path(name).unlink(missing_ok=True)


def extract(pdf: Path) -> Path:
    out = text_path_for(pdf)
    text, pages = pdf_text(pdf)
    if not text.strip():
        raise ValueError(f"no extractable text in {pdf}; OCR is required before filing")
    atomic_text(out, text)
    print(f"{pdf.parent.name}/{pdf.name}: {pages} pages, {len(text):,} chars -> {out.relative_to(_ROOT)}")
    return out


def missing() -> list[Path]:
    return [p for p in iter_pdfs() if not text_path_for(p).is_file()]


def orphans() -> list[Path]:
    wanted = {text_path_for(p).resolve() for p in iter_pdfs()}
    return sorted(p for p in _TEXT.glob("*/*.txt") if p.resolve() not in wanted)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--all", action="store_true", help="extract missing mirrors")
    group.add_argument("--check", action="store_true", help="report gaps/quality, write nothing")
    ap.add_argument("pdf", nargs="?")
    args = ap.parse_args(argv)
    if args.check:
        miss, orphan, bad = missing(), orphans(), 0
        for p in miss:
            print(f"MISSING TEXT: {p.relative_to(_ROOT)}")
        for p in orphan:
            print(f"ORPHAN TEXT: {p.relative_to(_ROOT)}")
        for p in sorted(_TEXT.glob("*/*.txt")):
            raw = p.read_bytes()
            try:
                body = raw.decode("utf-8")
            except UnicodeDecodeError:
                print(f"NOT UTF-8: {p.relative_to(_ROOT)}")
                bad += 1
                continue
            issues = []
            if not body.strip():
                issues.append("empty extraction")
            if b"\r" in raw:
                issues.append("CR endings")
            if any(b < 32 and b not in (9, 10) for b in raw):
                issues.append("control bytes")
            if _strip_line_number_gutters(body) != body:
                issues.append("line-number gutter")
            if issues:
                print(f"TEXT QUALITY: {p.relative_to(_ROOT)}: {', '.join(issues)}")
                bad += 1
        print(f"{len(iter_pdfs())} PDFs, {len(miss)} missing, {len(orphan)} orphaned, {bad} quality issue(s)")
        return int(bool(miss or orphan or bad))
    try:
        if args.all:
            for p in missing():
                extract(p)
            return 0
        if not args.pdf:
            ap.error("give a PDF path, --all, or --check")
        extract(Path(args.pdf))
        return 0
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
