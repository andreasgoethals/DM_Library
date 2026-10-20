#!/usr/bin/env python
"""Audit live Zotero collection, paper provenance and registered web sources (read-only).

Exit 0: consistent; 1: actionable differences; 2: live audit unavailable.
Collection membership is exact and never inferred from numeric sorting prefixes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.config import COLLECTION_SUBSTRING, LIBRARY_NAME, LOCAL_API, USER_AGENT
from lib.library import ROOT as _ROOT, PAPERS as _PAPERS, MONTHS, _ARXIV_STAMP, ascii_fold

DEFAULT_COLLECTION = COLLECTION_SUBSTRING


def read_zotero_prefs() -> dict[str, str]:
    """Compatibility helper; attachment resolution uses Zotero's API instead."""
    home = Path.home()
    candidates = [home / "Zotero" / "prefs.js",
                  home / "AppData/Roaming/Zotero/Zotero/Profiles",
                  home / ".zotero/zotero", home / "Library/Application Support/Zotero"]
    prefs = {}
    pattern = re.compile(r'user_pref\("([^"]+)",\s*("(?:[^"\\]|\\.)*")\);')
    for candidate in candidates:
        files = [candidate] if candidate.is_file() else candidate.rglob("prefs.js") if candidate.is_dir() else []
        for path in files:
            for m in pattern.finditer(path.read_text(encoding="utf-8", errors="replace")):
                if m.group(1).startswith("extensions.zotero."):
                    prefs.setdefault(m.group(1), json.loads(m.group(2)))
    return prefs


def citation_key(item: dict) -> str:
    data = item.get("data", item)
    key = data.get("citationKey") or item.get("citationKey")
    if key:
        return str(key)
    match = re.search(r"^\s*Citation Key:\s*(\S+)\s*$", data.get("extra", ""), re.I | re.M)
    return match.group(1) if match else ""


def author_names(item: dict) -> tuple[list[str], list[str]]:
    full, last = [], []
    for creator in item.get("data", item).get("creators", []):
        if creator.get("creatorType") != "author":
            continue
        surname = creator.get("lastName") or creator.get("name", "")
        name = " ".join(filter(None, [creator.get("firstName", ""), surname]))
        if name:
            full.append(name)
            last.append(surname)
    return full, last


def publication_date(item: dict) -> str:
    return item.get("meta", {}).get("parsedDate") or item["data"].get("date", "")


class ZoteroReader:
    def get(self, route: str, *, raw: bool = False):
        req = urllib.request.Request(LOCAL_API + route,
              headers={"Zotero-API-Version": "3", "User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=30) as response:
            body = response.read().decode("utf-8")
        return body if raw else json.loads(body)

    def all(self, route: str) -> list[dict]:
        """Paginate collections, items and children, preserving existing query parameters."""
        parts = urllib.parse.urlsplit(route)
        query = dict(urllib.parse.parse_qsl(parts.query))
        out, start = [], 0
        while True:
            query.update(limit="100", start=str(start))
            page = self.get(urllib.parse.urlunsplit(("", "", parts.path, urllib.parse.urlencode(query), "")))
            if not isinstance(page, list):
                raise ValueError(f"expected list from Zotero {parts.path}")
            out.extend(page)
            if len(page) < 100:
                return out
            start += len(page)

    def collection(self, name: str) -> dict:
        if not name.strip() or re.fullmatch(r"[\d.\s]+", name):
            raise ValueError("collection selector must be a stable name substring")
        matches = [c for c in self.all("/collections")
                   if name.casefold() in c["data"]["name"].casefold()]
        if len(matches) != 1:
            names = ", ".join(c["data"]["name"] for c in matches)
            raise ValueError(f"expected one collection containing {name!r}; found {len(matches)} ({names})")
        return matches[0]

    def items(self, collection_key: str) -> list[dict]:
        return [i for i in self.all(f"/collections/{collection_key}/items/top")
                if not i["data"].get("deleted")
                and i["data"].get("itemType") not in ("attachment", "note", "annotation")]

    def pdfs(self, item_key: str) -> list[dict]:
        return [c for c in self.all(f"/items/{item_key}/children")
                if not c["data"].get("deleted")
                and c["data"].get("contentType") == "application/pdf"]

    def file_path(self, attachment_key: str) -> Path:
        url = self.get(f"/items/{attachment_key}/file/view/url", raw=True).strip()
        parts = urllib.parse.urlsplit(url)
        if parts.scheme != "file":
            raise ValueError(f"attachment {attachment_key} has no local file URL")
        path = (f"//{parts.netloc}" if parts.netloc else "") + parts.path
        return Path(urllib.request.url2pathname(path))


def signature(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", ascii_fold(value).lower())


def library_papers() -> dict[str, Path]:
    """Relative paths are identities: equal basenames in different years stay visible."""
    return {p.relative_to(_ROOT).as_posix(): p for p in sorted(_PAPERS.glob("*/*.pdf"))
            if len(p.parent.name) == 4 and p.parent.name.isdigit()}


def match_library_file(title: str, lib: dict[str, Path]) -> str | None:
    """Conservative compatibility matching for papers predating the provenance manifest."""
    title_sig = signature(title)
    matches = [name for name in lib if title_sig and title_sig in signature(Path(name).stem)]
    return matches[0] if len(matches) == 1 else None


def load_registry(path: Path, field: str, default):
    if not path.exists():
        return default
    body = json.loads(path.read_text(encoding="utf-8"))
    if body.get("schema_version") != 1 or not isinstance(body.get(field), type(default)):
        raise ValueError(f"invalid schema in {path}")
    return body[field]


def filed_date(pdf: Path) -> tuple[str, str | None]:
    name_date = f"{pdf.parent.name}-{pdf.name[:2]}"
    text = _PAPERS / "text" / pdf.parent.name / (pdf.stem + ".txt")
    stamp = _ARXIV_STAMP.search(text.read_text(encoding="utf-8")[:16000]) if text.is_file() else None
    return name_date, f"{stamp.group(5)}-{MONTHS[stamp.group(4)]:02d}" if stamp else None


def author_segment(creators: list[str]) -> str:
    if len(creators) > 2:
        return f"{creators[0]} et al."
    return " and ".join(creators)


class Report:
    def __init__(self):
        self.sections: dict[str, list[str]] = {}

    def add(self, section: str, line: str) -> None:
        self.sections.setdefault(section, []).append(line)

    @property
    def total(self) -> int:
        return sum(len(lines) for lines in self.sections.values())

    def render(self, stats: dict) -> str:
        out = [f"Zotero <-> {LIBRARY_NAME} consistency check"]
        out.extend(f"  {key}: {value}" for key, value in stats.items())
        for section, lines in self.sections.items():
            out.append(f"\n{section} ({len(lines)})")
            out.extend(f"  - {line}" for line in lines)
        out.append(f"\n{self.total} issue(s)." if self.total else "\nNo inconsistencies found.")
        return "\n".join(out)


def _safe_path(relative: str) -> Path:
    path = (_ROOT / relative).resolve()
    if not path.is_relative_to(_ROOT.resolve()):
        raise ValueError(f"registry path escapes library: {relative}")
    return path


def _metadata_issues(record: dict, item: dict, label: str, rep: Report) -> None:
    data = item["data"]
    actual = {"title": data.get("title", ""), "publication_date": publication_date(item),
              "authors": author_names(item)[0], "citation_key": citation_key(item)}
    # Optional fields are checked whenever registered, without manufacturing
    # values for sparse bibliographic records or web-only source registries.
    for field, value in {"doi": data.get("DOI", ""), "url": data.get("url", ""),
                         "abstract": data.get("abstractNote", ""),
                         "item_type": data.get("itemType", "")}.items():
        if field in record:
            actual[field] = value
    overrides = record.get("overrides", {})
    for field, expected in actual.items():
        if field in overrides:
            continue
        if record.get(field) != expected:
            rep.add("Registered metadata differs from Zotero", f"{label}: {field}: {record.get(field)!r} != {expected!r}")
    if not actual["citation_key"]:
        rep.add("Zotero citation key unavailable", label)


def compare(z: ZoteroReader, collection: dict) -> tuple[dict, Report, list[str]]:
    rep, notes = Report(), []
    lib = library_papers()
    manifest = load_registry(_PAPERS / "manifest.json", "papers", {})
    web = load_registry(_PAPERS / "web_sources.json", "sources", [])
    records: dict[str, list[tuple[str, dict]]] = {}
    for relative, record in manifest.items():
        _safe_path(relative)
        records.setdefault(record.get("zotero_item_key", ""), []).append((relative, record))
        if relative not in lib:
            rep.add("Manifest PDFs absent on disk", relative)
    for record in web:
        records.setdefault(record.get("zotero_item_key", ""), []).append(("web", record))
    for key, entries in records.items():
        if not key or len(entries) != 1:
            rep.add("Missing or duplicate registry Zotero key", f"{key!r}: {len(entries)} records")
    items = z.items(collection["key"])
    live_keys, matched_lib, matched_web = set(), {}, set()
    for item in items:
        data, key = item["data"], item["key"]
        live_keys.add(key)
        title = data.get("title", "")
        label = f"{key} | {title}"
        authors, _ = author_names(item)
        if not authors:
            rep.add("Zotero items with NO author", label)
        if not data.get("DOI") and not data.get("url"):
            rep.add("Zotero items with neither DOI nor URL", label)
        if not publication_date(item):
            rep.add("Zotero publication date unavailable", label)
        entries = records.get(key, [])
        entry = entries[0] if len(entries) == 1 else None
        web_entry = entry is not None and entry[0] == "web"
        if web_entry:
            record = entry[1]
            eligible = (data.get("itemType") == "blogPost" or
                        (data.get("itemType") == "report" and "model card" in data.get("reportType", "").casefold()))
            if not eligible:
                rep.add("Research source incorrectly registered as web-only", label)
            matched_web.add(key)
            _metadata_issues(record, item, label, rep)
            archive = record.get("archive_path")
            if archive and not _safe_path(archive).is_file():
                rep.add("Registered web snapshot absent", f"{label}: {archive}")
            if not archive:
                notes.append(f"{key}: web source recorded without local snapshot ({record.get('status', 'status unspecified')})")
            if not record.get("url") or record.get("url") != data.get("url"):
                rep.add("Registered web URL differs from Zotero", label)
        pdfs = z.pdfs(key)
        if not pdfs and not web_entry:
            rep.add("Zotero items with no PDF attachment", label)
        for attachment in pdfs:
            try:
                if not z.file_path(attachment["key"]).is_file():
                    rep.add("Zotero attachment paths broken on disk", f"{label}: {attachment['key']}")
            except (urllib.error.URLError, ValueError, OSError) as exc:
                rep.add("Zotero PDF attachment unavailable", f"{label}: {attachment['key']}: {exc}")
        if web_entry:
            continue
        name = entry[0] if entry else match_library_file(title, lib)
        if name not in lib:
            rep.add("In Zotero collection but NOT in papers/", label)
            continue
        if name in matched_lib:
            rep.add("Multiple Zotero items matched one PDF", f"{matched_lib[name]} and {key} -> {name}")
        matched_lib[name] = key
        pdf = lib[name]
        name_date, version_date = filed_date(pdf)
        if entry:
            record = entry[1]
            _metadata_issues(record, item, label, rep)
            if record.get("filed_date") != name_date:
                rep.add("Manifest filed date disagrees with filename", name)
            if record.get("sha256") != hashlib.sha256(pdf.read_bytes()).hexdigest():
                rep.add("PDF content differs from provenance hash", name)
            if not record.get("date_source"):
                rep.add("Filed date provenance missing", name)
        else:
            rep.add("PDF missing provenance manifest record", name)
        if version_date and version_date != name_date:
            rep.add("Filed date disagrees with stored arXiv version", f"{name}: filename {name_date}, banner {version_date}")
        date = publication_date(item)
        if date and not date.startswith(name_date):
            if version_date == name_date or entry and entry[1].get("date_source") in ("explicit override", "PDF arXiv banner"):
                notes.append(f"{key}: publication date {date}; filed-version date {name_date} ({entry[1].get('date_source') if entry else 'PDF arXiv banner'})")
            elif re.match(r"\d{4}-\d{2}", date):
                rep.add("Publication/filed date differs without version evidence", f"{label}: {date} vs {name_date}")
            elif re.match(r"\d{4}", date) and date[:4] != pdf.parent.name:
                rep.add("Publication/filed year differs without version evidence", f"{label}: {date} vs {name_date}")
    for name in sorted(set(lib) - set(matched_lib)):
        rep.add("In papers/ but NOT in Zotero collection", name)
    for key in sorted(set(records) - live_keys):
        rep.add("Registered source outside selected Zotero collection", key)
    for name, pdf in lib.items():
        text = _PAPERS / "text" / pdf.parent.name / (pdf.stem + ".txt")
        if not text.is_file():
            rep.add("PDFs with no text extraction", name)
    for text in sorted((_PAPERS / "text").glob("*/*.txt")):
        pdf = _PAPERS / text.parent.name / (text.stem + ".pdf")
        if not pdf.is_file():
            rep.add("Text extraction without PDF", text.relative_to(_ROOT).as_posix())
    stats = {"Zotero collection": collection["data"]["name"], "source": "live Local API (read-only)",
             "items in collection": len(items), "PDFs in papers/": len(lib),
             "matched PDFs": len(matched_lib), "registered web sources": len(matched_web)}
    return stats, rep, notes


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--collection", default=DEFAULT_COLLECTION, help="unique stable collection name substring")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--list-collections", action="store_true")
    args = ap.parse_args(argv)
    z = ZoteroReader()
    try:
        if args.list_collections:
            for c in sorted(z.all("/collections"), key=lambda x: x["data"]["name"]):
                print(c["data"]["name"])
            return 0
        stats, rep, notes = compare(z, z.collection(args.collection))
    except (urllib.error.URLError, ValueError, OSError, KeyError) as exc:
        message = f"Cannot complete live Zotero audit: {exc}. Zotero must be running with Local API enabled. No SQLite fallback attempted."
        print(json.dumps({"error": message}, indent=2) if args.json else f"ERROR: {message}")
        return 2
    if args.json:
        print(json.dumps({"stats": stats, "issues": rep.sections, "version_notes": notes}, indent=2))
    else:
        print(rep.render(stats))
        for note in notes:
            print(f"  Note: {note}")
    return int(bool(rep.total))


if __name__ == "__main__":
    raise SystemExit(main())
