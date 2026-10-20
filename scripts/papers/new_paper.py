#!/usr/bin/env python
"""File a selected Zotero paper, extract text, and scaffold the intellectual work.

Use --zotero KEY, or a PDF path plus explicit metadata when Zotero has no
resolvable PDF. Combining both preserves curated metadata and membership
enforcement. Missing dates remain missing: --year/--month resolve them.
Scaffolds contain TODO(new-paper), which check_docs.py rejects.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import tempfile
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "checks"))
from lib.config import COLLECTION_SUBSTRING, USER_AGENT
from lib.library import ROOT, PAPERS, SUMMARIES, SYNTHESIS, CHANGELOG, MONTHS, _ARXIV_STAMP, ascii_fold, house_filename
from check_zotero_sync import ZoteroReader, author_names, citation_key, publication_date, load_registry

TODO = "TODO(new-paper)"
MIRRORED = COLLECTION_SUBSTRING
_ARXIV_ID = r"(?:\d{4}\.\d{4,5}|[a-zA-Z][a-zA-Z.\-]+/\d{7})(?:v\d+)?"
_ARXIV_ANY = re.compile(r"arXiv\s*[:/]\s*(" + _ARXIV_ID + r")", re.I)
_ATOM = "{http://www.w3.org/2005/Atom}"


@dataclass
class Meta:
    title: str
    authors: list[str]
    year: str = ""
    month: str = ""
    arxiv: str | None = None
    source: str = "unknown"
    surnames: list[str] = field(default_factory=list)
    zotero_item_key: str = ""
    citation_key: str = ""
    publication_date: str = ""
    venue: str = ""
    doi: str = ""
    abstract: str = ""
    url: str = ""
    item_type: str = ""
    date_source: str = ""
    arxiv_version: int | None = None
    overrides: dict = field(default_factory=dict)

    @property
    def date(self) -> str:
        return f"{self.year}-{self.month}"

    @property
    def last_names(self) -> list[str]:
        return self.surnames or [name.split()[-1] for name in self.authors if name.split()]

    @property
    def cite(self) -> str:
        names = self.last_names
        return f"{names[0]} et al." if len(names) > 2 else " and ".join(names) or TODO

    @property
    def filename(self) -> str:
        return house_filename(self.last_names, self.month, self.title)

    def validate(self) -> None:
        if not self.title.strip() or TODO in self.title or not self.authors:
            raise ValueError("title/authors unresolved; supply --title and --authors")
        if not re.fullmatch(r"\d{4}", self.year) or int(self.year) < 1:
            raise ValueError("filed-version year unresolved; supply --year YYYY (historical years supported)")
        if not re.fullmatch(r"0[1-9]|1[0-2]", self.month):
            raise ValueError("filed-version month unresolved; supply --month MM only with evidence; no month is invented")
        if self.zotero_item_key and not self.citation_key:
            raise ValueError("Zotero citation key unavailable; supply --citation-key from Zotero's exported record")


def pdf_text(pdf: Path, pages: int = 2) -> str:
    from pypdf import PdfReader
    reader = PdfReader(str(pdf))
    return "\n".join(page.extract_text() or "" for page in reader.pages[:pages])


def _banner(meta: Meta, body: str) -> bool:
    stamp = _ARXIV_STAMP.search(body)
    if not stamp:
        return False
    aid, version, _, month, year = stamp.groups()
    meta.year, meta.month = year, f"{MONTHS[month]:02d}"
    meta.arxiv, meta.arxiv_version = aid, int(version) if version else None
    meta.date_source = "PDF arXiv banner"
    return True


def from_arxiv(arxiv_id: str) -> Meta | None:
    import urllib.parse
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode({"id_list": arxiv_id})
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=30) as response:
            entry = ET.fromstring(response.read()).find(f"{_ATOM}entry")
        if entry is None or not entry.findtext(f"{_ATOM}id", "").startswith(("http://arxiv.org/abs/", "https://arxiv.org/abs/")):
            return None
    except (urllib.error.URLError, ET.ParseError, TimeoutError):
        return None
    meta = Meta(" ".join(entry.findtext(f"{_ATOM}title", "").split()),
                [" ".join(a.findtext(f"{_ATOM}name", "").split()) for a in entry.findall(f"{_ATOM}author")],
                arxiv=arxiv_id, source="arXiv API")
    # An unversioned lookup describes the latest remote version, not the held PDF.
    # Only an explicit version id provides evidence of the filed version's date.
    version = re.search(r"v(\d+)$", arxiv_id)
    if version:
        stamp = entry.findtext(f"{_ATOM}updated", "")[:7]
        if re.fullmatch(r"\d{4}-(?:0[1-9]|1[0-2])", stamp):
            meta.year, meta.month = stamp[:4], stamp[5:]
            meta.date_source = "version-specific arXiv API"
            meta.arxiv_version = int(version.group(1))
            meta.arxiv = arxiv_id[:version.start()]
    return meta


def from_pdf(pdf: Path) -> Meta:
    from pypdf import PdfReader
    reader = PdfReader(str(pdf))
    info = reader.metadata or {}
    body = "\n".join(page.extract_text() or "" for page in reader.pages[:2])
    title = " ".join(str(info.get("/Title") or "").split())
    if not title or title.lower().endswith(".dvi"):
        title = next((line.strip() for line in body.splitlines()
                      if len(line.strip()) > 12 and not line.startswith("arXiv")), "")
    authors = [a.strip() for a in re.split(r",| and |;", str(info.get("/Author") or "")) if a.strip()]
    meta = Meta(title, authors, source="PDF metadata (verify explicitly)")
    _banner(meta, body)
    # CreationDate is a technical file timestamp, not publication/version evidence.
    return meta


def from_zotero(key: str, pdf: Path | None = None,
                collection: str = MIRRORED, reader: ZoteroReader | None = None) -> tuple[Meta, Path]:
    z = reader or ZoteroReader()
    selected = z.collection(collection)
    item = z.get(f"/items/{key}")
    data = item["data"]
    if (data.get("deleted") or data.get("itemType") in ("note", "attachment", "annotation")
            or selected["key"] not in data.get("collections", [])):
        raise ValueError(f"{key} is not a live top-level reference in {selected['data']['name']!r}")
    full, surnames = author_names(item)
    date = publication_date(item)
    match = re.match(r"(\d{4})(?:-(\d{2}))?", date)
    meta = Meta(data.get("title", ""), full, match.group(1) if match else "",
                match.group(2) or "" if match else "", source="Zotero", surnames=surnames,
                zotero_item_key=key, citation_key=citation_key(item), publication_date=date,
                venue=data.get("publicationTitle") or data.get("conferenceName") or data.get("proceedingsTitle") or data.get("reportType") or "",
                doi=data.get("DOI", ""), abstract=data.get("abstractNote", ""), url=data.get("url", ""),
                item_type=data.get("itemType", ""), date_source="Zotero publication date" if match else "")
    arxiv = re.search(r"(?:arxiv\.org/(?:abs|pdf)/|arXiv[:\s]+)(" + _ARXIV_ID + ")", data.get("url", "") + " " + data.get("DOI", ""), re.I)
    if arxiv:
        meta.arxiv = arxiv.group(1)
    if pdf is None:
        errors = []
        for attachment in z.pdfs(key):
            try:
                candidate = z.file_path(attachment["key"])
                if candidate.is_file():
                    pdf = candidate
                    break
            except (urllib.error.URLError, OSError, ValueError) as exc:
                errors.append(str(exc))
        if pdf is None:
            raise ValueError(f"{key} has no resolvable PDF; pass a local PDF path alongside --zotero. {'; '.join(errors)}")
    if not pdf.is_file():
        raise ValueError(f"PDF not found: {pdf}")
    _banner(meta, pdf_text(pdf))
    return meta, pdf


def apply_overrides(meta: Meta, args: argparse.Namespace) -> Meta:
    for name in ("title", "year", "month", "citation_key", "venue", "doi", "arxiv"):
        value = getattr(args, name, None)
        if value is not None:
            if name == "month":
                if not str(value).isdigit() or not 1 <= int(value) <= 12:
                    raise ValueError("--month must be 1 through 12")
                value = f"{int(value):02d}"
            setattr(meta, name, value)
            meta.overrides[name] = value
    if getattr(args, "authors", None):
        meta.authors = [a.strip() for a in args.authors.split(",") if a.strip()]
        meta.surnames = []
        meta.overrides["authors"] = meta.authors
    if getattr(args, "year", None) or getattr(args, "month", None):
        meta.date_source = "explicit override"
    return meta


def resolve(pdf: Path, args: argparse.Namespace) -> Meta:
    base = from_pdf(pdf)
    arxiv = getattr(args, "arxiv", None)
    if not arxiv:
        match = _ARXIV_ANY.search(pdf_text(pdf))
        arxiv = match.group(1) if match else None
    meta = from_arxiv(arxiv) if arxiv else None
    if meta is None:
        meta = base
    _banner(meta, pdf_text(pdf))
    return apply_overrides(meta, args)


def _anchor(meta: Meta) -> str:
    title = re.sub(r"[^a-z0-9]+", "-", ascii_fold(meta.title).lower()).strip("-")
    return title or "paper-" + meta.zotero_item_key.lower()


def _insert_sorted_line(lines: list[str], new: str, date: str, pattern: str) -> list[str]:
    # Both durable documents also contain a separate web-source date table.
    # Locate the first Date table and keep insertion inside that table even
    # when later sections contain matching dates or year-only records.
    headers = [i for i, line in enumerate(lines)
               if re.match(r"^\|\s*(?:Filed date|Date)\s*\|", line, re.I)]
    if not headers:
        raise ValueError("document needs a table with a Date or Filed date first column")
    start = headers[0] + 2
    end = start
    while end < len(lines) and lines[end].lstrip().startswith("|"):
        end += 1
    indices = [i for i in range(start, end) if re.match(pattern, lines[i])]
    for i in indices:
        if re.match(pattern, lines[i]).group(1) > date:
            return lines[:i] + [new] + lines[i:]
    if indices:
        at = indices[-1] + 1
    else:
        at = start
    return lines[:at] + [new] + lines[at:]


def summaries_text(meta: Meta, relative: str, text: str) -> str:
    row = f"| {meta.date} | {meta.cite} | {meta.title} | {TODO}: contribution. | [pdf]({relative}) |"
    text = "\n".join(_insert_sorted_line(text.split("\n"), row, meta.date, r"^\| (\d{4}(?:-\d{2})?) \|"))
    anchor = _anchor(meta)
    if f'id="{anchor}"' in text:
        raise ValueError(f"summary anchor already exists: {anchor}")
    provenance = meta.venue or "Venue unresolved"
    if meta.doi:
        provenance += f"; DOI: {meta.doi}"
    if meta.arxiv:
        provenance += f"; [arXiv:{meta.arxiv}](https://arxiv.org/abs/{meta.arxiv})"
    entry = (f'<a id="{anchor}"></a>\n\n## {meta.date} — {meta.cite} — {meta.title}\n\n'
             f"**Venue/provenance.** {provenance}. Filed version: {meta.date} ({meta.date_source}).\n"
             f"**Zotero citation key:** `{meta.citation_key or TODO}`. **PDF:** [open]({relative}).\n\n"
             f"**Where it fits.** {TODO}: relationship to the other papers.\n\n"
             f"**What it contains.** {TODO}: method, assumptions, setup and evidence.\n\n"
             f"**Strengths.** {TODO}\n\n**Limitations.** {TODO}\n\n---\n")
    web_section = re.search(r"^## Web-source overview\b.*$", text, re.M | re.I)
    paper_end = web_section.start() if web_section else len(text)
    later = next((m for m in re.finditer(r"^## (\d{4}(?:-\d{2})?) — ", text[:paper_end], re.M)
                  if m.group(1) > meta.date), None)
    if later:
        at = later.start()
        prefix = re.search(r'<a id="[^"]+"></a>\s*$', text[:at])
        if prefix:
            at = prefix.start()
        return text[:at] + entry + "\n" + text[at:]
    if web_section:
        return text[:paper_end].rstrip() + "\n\n" + entry + "\n" + text[paper_end:]
    return text.rstrip() + "\n\n" + entry


def synthesis_text(meta: Meta, text: str) -> str:
    row = f"| {meta.date} | {meta.cite} ({meta.year}), [{meta.title}](SUMMARIES.md#{_anchor(meta)}) | {TODO}: what it establishes | {TODO} |"
    return "\n".join(_insert_sorted_line(text.split("\n"), row, meta.date, r"^\| (\d{4}(?:-\d{2})?) \|"))


def changelog_text(meta: Meta, text: str) -> str:
    today = dt.date.today().isoformat()
    line = f"- Added **{meta.cite} {meta.date} — {meta.title}**. {TODO}: contribution and synthesis changes.\n"
    heading = re.search(r"^## " + re.escape(today) + r"\s*$", text, re.M)
    if heading:
        at = heading.end()
        return text[:at] + "\n\n" + line + text[at:].lstrip("\n")
    first = re.search(r"^## \d{4}-\d{2}-\d{2}", text, re.M)
    at = first.start() if first else len(text)
    return text[:at].rstrip() + "\n\n" + f"## {today}\n\n{line}\n" + text[at:]


def atomic_batch(updates: dict[Path, bytes]) -> None:
    """Stage before replacement; roll back earlier outputs if any replacement fails."""
    staged, originals, installed = {}, {}, []
    try:
        for path, content in updates.items():
            originals[path] = path.read_bytes() if path.exists() else None
            path.parent.mkdir(parents=True, exist_ok=True)
            fd, name = tempfile.mkstemp(prefix="." + path.name + ".", suffix=".tmp", dir=path.parent)
            staged[path] = Path(name)
            with os.fdopen(fd, "wb") as stream:
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
        for path, temp in staged.items():
            os.replace(temp, path)
            installed.append(path)
    except BaseException:
        for path in reversed(installed):
            original = originals[path]
            if original is None:
                path.unlink(missing_ok=True)
            else:
                fd, name = tempfile.mkstemp(prefix=".rollback-", dir=path.parent)
                with os.fdopen(fd, "wb") as stream:
                    stream.write(original)
                os.replace(name, path)
        raise
    finally:
        for temp in staged.values():
            temp.unlink(missing_ok=True)


def scaffold_summaries(meta: Meta, rel_pdf: str) -> str:
    atomic_batch({SUMMARIES: summaries_text(meta, rel_pdf, SUMMARIES.read_text(encoding="utf-8")).encode()})
    return _anchor(meta)


def scaffold_synthesis(meta: Meta) -> None:
    atomic_batch({SYNTHESIS: synthesis_text(meta, SYNTHESIS.read_text(encoding="utf-8")).encode()})


def scaffold_changelog(meta: Meta) -> None:
    atomic_batch({CHANGELOG: changelog_text(meta, CHANGELOG.read_text(encoding="utf-8")).encode()})


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("pdf", nargs="?", help="local PDF; also usable as Zotero attachment fallback")
    ap.add_argument("--zotero", metavar="KEY", help=f"item in the unique {MIRRORED!r} collection")
    ap.add_argument("--collection", default=MIRRORED, help="unique stable collection name substring")
    for name in ("title", "arxiv", "authors", "year", "month", "citation-key", "venue", "doi"):
        ap.add_argument("--" + name)
    ap.add_argument("--move", action="store_true", help="move non-Zotero input after successful filing")
    ap.add_argument("--no-scaffold", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--yes", action="store_true")
    args = ap.parse_args(argv)
    try:
        if args.zotero and args.move:
            raise ValueError("--move cannot be combined with --zotero: Zotero attachments must be preserved")
        if not args.pdf and not args.zotero:
            ap.error("give a PDF path or --zotero KEY")
        src = Path(args.pdf).expanduser().resolve() if args.pdf else None
        if args.zotero:
            meta, src = from_zotero(args.zotero, src, args.collection)
            apply_overrides(meta, args)
        else:
            if not src.is_file():
                raise ValueError(f"PDF not found: {src}")
            meta = resolve(src, args)
        meta.validate()
        dest = PAPERS / meta.year / meta.filename
        relative = dest.relative_to(ROOT).as_posix()
        manifest_path = PAPERS / "manifest.json"
        manifest = load_registry(manifest_path, "papers", {})
        if dest.exists():
            raise ValueError(f"already filed: {relative}; nothing overwritten")
        if meta.zotero_item_key and any(r.get("zotero_item_key") == meta.zotero_item_key for r in manifest.values()):
            raise ValueError(f"Zotero item {meta.zotero_item_key} is already in the manifest")
        print(f"Metadata: {meta.source}\nTitle: {meta.title}\nAuthors: {', '.join(meta.authors)}")
        print(f"Publication date: {meta.publication_date or '(unavailable)'}\nFiled date: {meta.date} ({meta.date_source})")
        print(f"Citation key: {meta.citation_key or '(unavailable)'}\nDestination: {relative}")
        if args.dry_run:
            print("Dry run: no files changed.")
            return 0
        if not args.yes:
            if not sys.stdin.isatty() or input("File under this name? [y/N] ").strip().lower() != "y":
                print("Not filed. Re-run with --yes to accept the plan non-interactively.")
                return 2
        from extract_paper_text import pdf_text as extract_text
        body, pages = extract_text(src)
        if not body.strip():
            raise ValueError("PDF has no extractable text; no files written. OCR is required.")
        pdf_bytes = src.read_bytes()
        record = asdict(meta)
        for name in ("year", "month", "source"):
            record.pop(name)
        record.update(filed_date=meta.date, sha256=hashlib.sha256(pdf_bytes).hexdigest())
        manifest[relative] = record
        text_path = PAPERS / "text" / meta.year / (dest.stem + ".txt")
        updates = {dest: pdf_bytes, text_path: body.encode("utf-8"),
                   manifest_path: (json.dumps({"schema_version": 1, "papers": manifest}, ensure_ascii=False, indent=2) + "\n").encode("utf-8")}
        if not args.no_scaffold:
            updates.update({SUMMARIES: summaries_text(meta, relative, SUMMARIES.read_text(encoding="utf-8")).encode("utf-8"),
                            SYNTHESIS: synthesis_text(meta, SYNTHESIS.read_text(encoding="utf-8")).encode("utf-8"),
                            CHANGELOG: changelog_text(meta, CHANGELOG.read_text(encoding="utf-8")).encode("utf-8")})
        atomic_batch(updates)
        if args.move:
            src.unlink()
        print(f"Filed PDF, {pages}-page extraction and provenance manifest.")
        if not args.no_scaffold:
            print(f"Complete all {TODO} entries, integrate the synthesis argument, then run python scripts/checks/check_docs.py.")
        return 0
    except (OSError, ValueError, urllib.error.URLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
