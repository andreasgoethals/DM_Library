#!/usr/bin/env python
"""Validate corpus identity, complete summaries, links, chronology and neutrality."""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.library import ROOT as _ROOT, github_slug
from lib.config import PROJECT_MARKERS

DOCS = ["README.md", "AGENTS.md", "SUMMARIES.md", "SYNTHESIS.md", "REPOSITORIES.md", "CHANGELOG.md", "PROJECT_SPECIFIC.template.md"]
NEUTRAL_DOCS = ["SUMMARIES.md", "SYNTHESIS.md", "REPOSITORIES.md"]
# Add a consumer name only if an owner identifies it; never inherit another library's list.
_DATE = r"\d{4}-(?:0[1-9]|1[0-2])"
_ENTRY = re.compile(rf"^## ({_DATE}) — (.+)$", re.M)
_ROW = re.compile(rf"^\| ({_DATE}) \|.*$", re.M)
_LINK = re.compile(r"\]\((<[^>]+>|[^\s)]+)(?:\s+\"[^\"]*\")?\)")


class Report:
    def __init__(self) -> None:
        self.problems: list[str] = []
        self.notes: list[str] = []
    def fail(self, msg: str) -> None:
        self.problems.append(msg)
    def note(self, msg: str) -> None:
        self.notes.append(msg)


def read(doc: str) -> str:
    path = _ROOT / doc
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def links(text: str) -> list[str]:
    return [unquote(m.group(1).strip("<>")) for m in _LINK.finditer(text)]


def anchors(text: str) -> set[str]:
    out = set(re.findall(r'<a\s+(?:id|name)=[\"\']([^\"\']+)', text))
    counts: Counter[str] = Counter()
    # Fenced examples do not define document headings or links.
    text = re.sub(r"^```[^\n]*\n.*?^```[^\n]*$", "", text, flags=re.M | re.S)
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.M):
        heading = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", heading)
        slug = github_slug(heading)
        out.add(slug + (f"-{counts[slug]}" if counts[slug] else ""))
        counts[slug] += 1
    return out


def paper_links(text: str) -> list[str]:
    return [urlsplit(target).path for target in links(text)
            if re.match(r"^papers/\d{4}/[^/]+\.pdf$", urlsplit(target).path)]


def check_coverage(rep: Report) -> dict[str, int]:
    pdfs = sorted(p for p in (_ROOT / "papers").glob("*/*.pdf") if re.fullmatch(r"\d{4}", p.parent.name))
    wanted = {p.relative_to(_ROOT).as_posix(): p for p in pdfs}
    txts = sorted((_ROOT / "papers/text").glob("*/*.txt"))
    mirror_set = {_ROOT / "papers/text" / p.parent.name / (p.stem + ".txt") for p in pdfs}
    for p in pdfs:
        if not re.match(r"^(0[1-9]|1[0-2])_[\x00-\x7f]+\.pdf$", p.name) or " " in p.name:
            rep.fail(f"invalid house filename: {p.relative_to(_ROOT).as_posix()}")
        t = _ROOT / "papers/text" / p.parent.name / (p.stem + ".txt")
        if not t.is_file():
            rep.fail(f"no text extraction for {p.parent.name}/{p.name}")
    for t in txts:
        if t not in mirror_set:
            rep.fail(f"orphan extraction (no PDF): {t.parent.name}/{t.name}")
    summary, synthesis = read("SUMMARIES.md"), read("SYNTHESIS.md")
    heads = list(_ENTRY.finditer(summary))
    # Web-only records have their own coverage tables, never synthetic PDFs.
    overview_text = re.split(r"^## Web-source overview\b", summary, flags=re.M)[0]
    timeline_text = re.split(r"^## Web-source timeline\b", synthesis, flags=re.M)[0]
    overview = list(_ROW.finditer(overview_text))
    timeline = list(_ROW.finditer(timeline_text))
    entries = [m.group(1) for m in heads]
    rows = [m.group(1) for m in overview]
    timeline_dates = [m.group(1) for m in timeline]
    counts = {"papers": len(pdfs), "texts": len(txts), "SUMMARIES entries": len(heads), "SUMMARIES rows": len(rows), "SYNTHESIS timeline": len(timeline)}
    if len(set(counts.values())) != 1:
        rep.fail("counts disagree: " + ", ".join(f"{key}={value}" for key, value in counts.items()))
    for label, sequence in (("SUMMARIES entries", entries), ("SUMMARIES rows", rows), ("SYNTHESIS timeline", timeline_dates)):
        if sequence != sorted(sequence):
            rep.fail(f"{label} are not in chronological order")
    if rows != entries:
        rep.fail("SUMMARIES overview-table order does not match entry order")
    if timeline_dates != entries:
        rep.fail("SYNTHESIS timeline dates/order do not match SUMMARIES entries")
    entry_paths: list[str] = []
    anchor_papers: dict[str, str] = {}
    citation_keys: list[str] = []
    manifest_path = _ROOT / "papers/manifest.json"
    manifest = {}
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))["papers"]
            if not isinstance(manifest, dict):
                raise ValueError("papers must map PDF paths to metadata")
        except (ValueError, KeyError, TypeError) as exc:
            rep.fail(f"invalid papers/manifest.json: {exc}")
            manifest = {}
    for i, match in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(summary)
        next_section = re.search(r"^## ", summary[match.end():end], re.M)
        if next_section:
            end = match.end() + next_section.start()
        body = summary[match.end():end]
        label = match.group(2)[:70]
        for section in ("Where it fits", "What it contains", "Strengths", "Limitations"):
            if not re.search(r"\*\*" + re.escape(section) + r"\b", body):
                rep.fail(f"SUMMARIES.md: {label!r} lacks {section}")
        if not re.search(r"\*\*(?:Venue|Provenance)", body, re.I):
            rep.fail(f"SUMMARIES.md: {label!r} lacks venue/provenance")
        keys = re.findall(r"\*\*(?:Zotero )?[Cc]itation key:?\*\*\s*:?\s*`([^`]+)`", body)
        if len(keys) != 1 or not keys[0].strip() or keys[0].lower().startswith(("unknown", "unconfirmed", "todo")):
            rep.fail(f"SUMMARIES.md: {label!r} needs one verified Zotero citation key")
        else:
            citation_keys.extend(keys)
        candidates = list(dict.fromkeys(paper_links(body)))
        if len(candidates) != 1:
            rep.fail(f"SUMMARIES.md: {label!r} must link its single local PDF")
            continue
        paper = candidates[0]
        entry_paths.append(paper)
        path = Path(paper)
        if f"{path.parent.name}-{path.name[:2]}" != match.group(1):
            rep.fail(f"SUMMARIES.md: date does not match filed PDF: {paper}")
        if manifest:
            metadata = manifest.get(paper)
            if not metadata:
                rep.fail(f"SUMMARIES.md: no provenance manifest record for {paper}")
            elif len(keys) == 1 and keys[0] != metadata.get("citation_key"):
                rep.fail(f"SUMMARIES.md: citation key differs from Zotero provenance for {paper}")
        anchor_papers[github_slug(match.group(1) + " — " + match.group(2))] = paper
        # An explicit anchor immediately before the heading belongs to this entry.
        prefix = summary[heads[i - 1].end() if i else 0:match.start()]
        nearby = re.search(r'<a\s+id="([^"]+)"\s*></a>\s*$', prefix)
        if nearby:
            anchor_papers[nearby.group(1)] = paper
    for label, paths in (("summary entries", entry_paths), ("overview rows", [p for row in overview for p in paper_links(row.group())])):
        counter = Counter(paths)
        for paper in wanted:
            if counter[paper] != 1:
                rep.fail(f"{label}: {paper} occurs {counter[paper]} times (expected 1)")
        for paper in counter.keys() - wanted.keys():
            rep.fail(f"{label}: no PDF for {paper}")
    overview_paths = [p for row in overview for p in paper_links(row.group())]
    if overview_paths != entry_paths:
        rep.fail("overview and summary paper identity/order differ")
    timeline_paths = []
    for row in timeline:
        candidates = paper_links(row.group())
        for target in links(row.group()):
            split = urlsplit(target)
            if split.path == "SUMMARIES.md" and split.fragment in anchor_papers:
                candidates.append(anchor_papers[split.fragment])
        candidates = list(dict.fromkeys(candidates))
        if len(candidates) != 1:
            rep.fail(f"SYNTHESIS timeline needs one identifiable paper link: {row.group()[:100]}")
        else:
            timeline_paths.extend(candidates)
    if timeline_paths != entry_paths:
        rep.fail("timeline and summary paper identity/order differ")
    for key, count in Counter(citation_keys).items():
        if count > 1:
            rep.fail(f"duplicate Zotero citation key in summaries: {key}")
    if manifest and set(manifest) != set(wanted):
        rep.fail("PDF files and papers/manifest.json cover different paths")
    return counts


def named_section(text: str, title: str) -> str:
    match = re.search(r"^## " + re.escape(title) + r"[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return match.group(1) if match else ""


def check_web_sources(rep: Report) -> dict[str, int]:
    path = _ROOT / "papers/web_sources.json"
    if not path.exists():
        return {"web sources": 0}
    try:
        registry = json.loads(path.read_text(encoding="utf-8"))
        sources = registry["sources"]
        if registry.get("schema_version") != 1 or not isinstance(sources, list):
            raise ValueError("expected schema_version=1 and a sources list")
    except (ValueError, KeyError, TypeError) as exc:
        rep.fail(f"invalid papers/web_sources.json: {exc}")
        return {"web sources": 0}
    summary = read("SUMMARIES.md")
    synthesis = read("SYNTHESIS.md")
    web = named_section(summary, "Web sources")
    overview = named_section(summary, "Web-source overview")
    timeline = named_section(synthesis, "Web-source timeline")
    entries = list(re.finditer(r"^### (\d{4}(?:-(?:0[1-9]|1[0-2]))?) — (.+)$", web, re.M))
    if len(entries) != len(sources):
        rep.fail(f"web source count mismatch: registry={len(sources)}, summary entries={len(entries)}")
    dates = [entry.group(1) for entry in entries]
    dated = [date for date in dates if len(date) == 7]
    if dated != sorted(dated) or [date[:4] for date in dates] != sorted(date[:4] for date in dates):
        rep.fail("web-source summaries are not chronological; unknown months do not imply an order within their year")
    known_ids, known_keys = set(), set()
    for source in sources:
        if not isinstance(source, dict):
            rep.fail("web registry contains a non-object record")
            continue
        item_key = source.get("zotero_item_key", "")
        key = source.get("citation_key", "")
        if not item_key or item_key in known_ids:
            rep.fail(f"missing/duplicate web Zotero item key: {item_key!r}")
        if not key or key in known_keys:
            rep.fail(f"missing/duplicate web citation key: {key!r}")
        known_ids.add(item_key)
        known_keys.add(key)
        if not source.get("title") or not source.get("url") or not source.get("status"):
            rep.fail(f"web source {item_key}: title, URL and status are required")
        archive = source.get("archive_path")
        if archive and not (_ROOT / archive).is_file():
            rep.fail(f"web source {item_key}: archive file missing: {archive}")
        matches = []
        for i, entry in enumerate(entries):
            body = web[entry.end(): entries[i + 1].start() if i + 1 < len(entries) else len(web)]
            if f"`{key}`" in body:
                matches.append((entry, body))
        if len(matches) != 1:
            rep.fail(f"web source {item_key}: expected one summary with citation key {key!r}, found {len(matches)}")
            continue
        entry, body = matches[0]
        date = source.get("verified_publication_date") or source.get("publication_date") or ""
        if date and re.match(r"^\d{4}(?:-\d{2})?", date):
            expected = date[:7] if len(date) >= 7 else date[:4]
            if entry.group(1) != expected:
                rep.fail(f"web source {item_key}: summary date {entry.group(1)} differs from recorded date {expected}")
        for section in ("Where it fits", "What it contains", "Strengths", "Limitations"):
            if not re.search(r"\*\*" + re.escape(section) + r"\b", body):
                rep.fail(f"web source {item_key}: missing {section}")
        if not re.search(r"\*\*(?:Venue|Provenance)", body, re.I):
            rep.fail(f"web source {item_key}: missing venue/provenance")
        if source.get("url") not in body:
            rep.fail(f"web source {item_key}: summary does not link its primary URL")
        if archive and archive not in links(body):
            rep.fail(f"web source {item_key}: summary does not link its archive")
        anchor = "web-" + item_key.lower()
        if anchor not in anchors(summary):
            rep.fail(f"web source {item_key}: missing explicit anchor #{anchor}")
        for label, table, target in (("overview", overview, "#" + anchor), ("timeline", timeline, "SUMMARIES.md#" + anchor)):
            count = links(table).count(target)
            if count != 1:
                rep.fail(f"web {label}: {target} occurs {count} times (expected 1)")
    return {"web sources": len(sources)}


def check_links_and_anchors(rep: Report) -> None:
    for doc in DOCS:
        path = _ROOT / doc
        if not path.is_file():
            rep.fail(f"missing document: {doc}")
            continue
        text = re.sub(r"^```[^\n]*\n.*?^```[^\n]*$", "", read(doc), flags=re.M | re.S)
        for target in links(text):
            split = urlsplit(target)
            if split.scheme or split.netloc:
                continue
            dest = path.parent / split.path if split.path else path
            if not dest.exists():
                rep.fail(f"{doc}: broken link -> {target}")
            elif split.fragment and dest.is_file() and dest.suffix.lower() == ".md":
                if split.fragment not in anchors(dest.read_text(encoding="utf-8")):
                    rep.fail(f"{doc}: unresolved anchor -> {target}")


def check_changelog(rep: Report) -> None:
    dates = re.findall(r"^## (\d{4}-\d{2}-\d{2})", read("CHANGELOG.md"), re.M)
    if not dates:
        rep.fail("CHANGELOG.md has no dated sections")
    today = datetime.date.today()
    for value in dates:
        try:
            date = datetime.date.fromisoformat(value)
            if date > today:
                rep.fail(f"CHANGELOG.md has future date {value}")
        except ValueError:
            rep.fail(f"CHANGELOG.md has invalid date {value}")
    if len(set(dates)) != len(dates):
        rep.fail("CHANGELOG.md has duplicate dated sections")
    if dates != sorted(dates, reverse=True):
        rep.fail("CHANGELOG.md sections are not newest-first")


def check_neutrality(rep: Report) -> None:
    for doc in NEUTRAL_DOCS:
        text = read(doc)
        for marker in PROJECT_MARKERS:
            if re.search(r"(?<![A-Za-z0-9])" + re.escape(marker) + r"(?![A-Za-z0-9])", text, re.I):
                rep.fail(f"{doc}: consuming project name {marker!r} belongs in PROJECT_SPECIFIC.md")
        # Upstream source maps may legitimately cite src/train; require local context.
        for line in text.splitlines():
            if re.search(r"[A-Za-z]:[\\/]Users[\\/]|/home/[^/]+/|/Users/[^/]+/", line):
                rep.fail(f"{doc}: private absolute filesystem path belongs in PROJECT_SPECIFIC.md")
            if re.search(r"\b(?:our|my|this project's)\s+`?(?:src/|config/|data/processed)", line, re.I):
                rep.fail(f"{doc}: project pipeline detail belongs in PROJECT_SPECIFIC.md")


def check_placeholders(rep: Report) -> None:
    for doc in ("SUMMARIES.md", "SYNTHESIS.md", "CHANGELOG.md"):
        for number, line in enumerate(read(doc).splitlines(), 1):
            if "TODO(new-paper)" in re.sub(r"`[^`]*`", "", line):
                rep.fail(f"{doc}:{number}: unfinished new-paper scaffold")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)
    rep = Report()
    counts = check_coverage(rep)
    counts.update(check_web_sources(rep))
    check_links_and_anchors(rep)
    check_changelog(rep)
    check_neutrality(rep)
    check_placeholders(rep)
    if not args.quiet:
        for key, value in counts.items():
            print(f"{key}: {value}")
    # --quiet suppresses success chatter only; every problem stays visible.
    for problem in rep.problems:
        print(f"[PROBLEM] {problem}")
    print(f"{len(rep.problems)} document problem(s)." if rep.problems else "Documents are internally consistent.")
    return int(bool(rep.problems))


if __name__ == "__main__":
    raise SystemExit(main())
