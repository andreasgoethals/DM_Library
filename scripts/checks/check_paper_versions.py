#!/usr/bin/env python
"""Report newer arXiv versions without replacing papers. Exit 0/1/2: current/outdated/incomplete."""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
USER_AGENT = "literature-maintenance/1.0"
_ROOT = Path(__file__).resolve().parents[2]
_TEXT = _ROOT / "papers/text"
_MONTHS = {name: i + 1 for i, name in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])}
_STAMP = re.compile(
    r"arXiv:((?:\d{4}\.\d{4,5}|[a-zA-Z.\-]+/\d{7}))(?:v(\d+))?\s*(?:\[[a-zA-Z.\-]+\]\s*)?"
    r"(\d{1,2})\s+([A-Z][a-z]{2})\s+(\d{4})")

_API = "https://export.arxiv.org/api/query"
_ATOM = "{http://www.w3.org/2005/Atom}"


def local_papers() -> tuple[dict[str, dict], list[str]]:
    """Use each relative paper path as identity, so duplicate arXiv IDs stay visible."""
    found, unverifiable = {}, []
    for text in sorted(_TEXT.glob("*/*.txt")):
        relative = f"{text.parent.name}/{text.stem}"
        stamp = _STAMP.search(text.read_text(encoding="utf-8")[:16000])
        if not stamp or not stamp.group(2):
            unverifiable.append(relative)
            continue
        aid, version, day, month, year = stamp.groups()
        found[relative] = {"arxiv": aid, "paper": relative,
                           "held_version": int(version),
                           "held_date": f"{year}-{_MONTHS[month]:02d}-{int(day):02d}",
                           "folder_year": text.parent.name, "month_prefix": text.stem[:2]}
    return found, unverifiable


def web_sources() -> list[dict]:
    """Web releases/model cards have no filed PDF version for arXiv to verify."""
    registry = _TEXT.parent / "web_sources.json"
    if not registry.exists():
        return []
    body = json.loads(registry.read_text(encoding="utf-8"))
    if body.get("schema_version") != 1 or not isinstance(body.get("sources"), list):
        raise ValueError(f"invalid web-source registry: {registry}")
    return [{"title": source.get("title", ""), "zotero_item_key": source.get("zotero_item_key", ""),
             "url": source.get("url", ""), "reason": "web source; no filed PDF/arXiv version to check"}
            for source in body["sources"]]


def _query_batch(ids: list[str]) -> dict[str, dict]:
    query = urllib.parse.urlencode({"id_list": ",".join(ids), "max_results": len(ids)})
    root = None
    for attempt, delay in enumerate((5, 15, 40)):
        request = urllib.request.Request(_API + "?" + query, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                root = ET.fromstring(response.read())
            break
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 503) or attempt == 2:
                raise
            print(f"arXiv busy; retrying in {delay}s", file=sys.stderr)
            time.sleep(delay)
    if root is None:
        raise urllib.error.URLError("arXiv did not answer")
    out = {}
    for entry in root.findall(f"{_ATOM}entry"):
        url = entry.findtext(f"{_ATOM}id", "")
        match = re.search(r"/abs/(.+)v(\d+)$", url)
        if match:
            out[match.group(1)] = {
                "latest_version": int(match.group(2)),
                "updated": entry.findtext(f"{_ATOM}updated", "")[:10],
                "title": " ".join(entry.findtext(f"{_ATOM}title", "").split()),
            }
    return out


def query_arxiv(ids: list[str]) -> dict[str, dict]:
    out = {}
    ids = sorted(set(ids))
    for start in range(0, len(ids), 100):
        if start:
            time.sleep(3)
        batch = ids[start:start + 100]
        try:
            out.update(_query_batch(batch))
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 503):
                raise
            print(f"arXiv API unavailable ({exc.code}); checking primary submission-history pages.",
                  file=sys.stderr)
            for index, aid in enumerate(batch):
                if index:
                    time.sleep(3)
                request = urllib.request.Request(
                    "https://arxiv.org/abs/" + urllib.parse.quote(aid, safe="/"),
                    headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(request, timeout=45) as response:
                    body = response.read().decode("utf-8")
                out[aid] = parse_submission_history(body)
    return out


def parse_submission_history(body: str) -> dict:
    section = re.search(r'<div class="submission-history">(.*?)</div>', body, re.S)
    if not section:
        raise ValueError("Primary arXiv page has no submission history")
    text = html.unescape(re.sub(r"<[^>]+>", " ", section.group(1)))
    versions = re.findall(r"\[v(\d+)\]\s*(?:\w+,\s*)?(\d{1,2})\s+([A-Z][a-z]{2})\s+(\d{4})", text)
    if not versions:
        raise ValueError("Primary arXiv submission history could not be parsed")
    version, day, month, year = max(versions, key=lambda row: int(row[0]))
    title = re.search(r'<meta name="citation_title" content="([^"]*)"', body)
    return {"latest_version": int(version),
            "updated": f"{year}-{_MONTHS[month]:02d}-{int(day):02d}",
            "title": html.unescape(title.group(1)) if title else "",
            "source": "primary arXiv submission-history page"}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        local, unverifiable = local_papers()
        web_unverifiable = web_sources()
        remote = query_arxiv([row["arxiv"] for row in local.values()]) if local else {}
    except (urllib.error.URLError, ET.ParseError, TimeoutError, OSError, ValueError) as exc:
        message = f"Could not complete arXiv version check: {exc}"
        print(json.dumps({"error": message}, indent=2) if args.json else f"ERROR: {message}")
        return 2
    outdated, current, unknown = [], [], []
    for info in local.values():
        latest = remote.get(info["arxiv"])
        if latest is None:
            unknown.append(info)
        else:
            row = {**info, **latest}
            (outdated if latest["latest_version"] > info["held_version"] else current).append(row)
    result = {"outdated": outdated, "current": current, "unknown": unknown,
              "unverifiable": unverifiable, "web_unverifiable": web_unverifiable}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Paper versions: {len(current)} current, {len(outdated)} outdated, {len(unknown)} unresolved, {len(unverifiable)} unverifiable PDFs, {len(web_unverifiable)} unverifiable web sources")
        for row in outdated:
            print(f"NEWER: {row['paper']}: held v{row['held_version']} ({row['held_date']}); latest v{row['latest_version']} ({row['updated']})")
            print(f"  https://arxiv.org/abs/{row['arxiv']}")
        for row in unknown:
            print(f"UNRESOLVED: {row['paper']} ({row['arxiv']}); API returned no matching version")
        for paper in unverifiable:
            print(f"UNVERIFIABLE: {paper}: no explicit arXiv version banner; inspect publisher manually")
        for source in web_unverifiable:
            print(f"UNVERIFIABLE WEB: {source['zotero_item_key']} | {source['title']}: {source['reason']}")
        if not local:
            print("No version-stamped arXiv papers to query. No claim is made about other publications.")
        if outdated:
            print("Replacement is manual: review date, filename, extraction and summary evidence before replacing a PDF.")
    return 1 if outdated else 2 if unknown else 0


if __name__ == "__main__":
    raise SystemExit(main())
