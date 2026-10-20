"""Offline regression coverage for DM Library's actual ingestion and live-audit adapters."""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "papers"))
import check_zotero_sync as sync
import check_paper_versions as versions
import extract_paper_text as extraction
import new_paper as ingest


def item(key="ITEM1", date="1955-06", title="Optimal Actions under Uncertainty"):
    return {"key": key, "data": {
        "title": title, "itemType": "journalArticle", "date": date,
        "citationKey": "Muller1955", "publicationTitle": "Decision Research",
        "DOI": "10.1234/example", "url": "https://example.test/paper",
        "collections": ["COLL"], "abstractNote": "A decision-theory fixture.",
        "creators": [{"creatorType": "author", "firstName": "Ada", "lastName": "Müller"},
                     {"creatorType": "author", "firstName": "Louis", "lastName": "van der Waals"}]}}


class FakeZotero:
    def __init__(self, items, pdf=None):
        self.references, self.pdf = items, pdf

    def collection(self, name):
        return {"key": "COLL", "data": {"name": "07. Decision Models"}}

    def get(self, route):
        key = route.rsplit("/", 1)[-1]
        return next(i for i in self.references if i["key"] == key)

    def items(self, key):
        return self.references

    def pdfs(self, key):
        return [{"key": "PDF1", "data": {"contentType": "application/pdf"}}] if self.pdf else []

    def file_path(self, key):
        return self.pdf


def write_pdf(path, text="A real PDF extraction fixture for historical decision models."):
    from pypdf import PdfWriter
    from pypdf.generic import DictionaryObject, NameObject, DecodedStreamObject
    writer = PdfWriter()
    page = writer.add_blank_page(width=500, height=500)
    font = DictionaryObject({NameObject("/Type"): NameObject("/Font"),
                             NameObject("/Subtype"): NameObject("/Type1"),
                             NameObject("/BaseFont"): NameObject("/Helvetica")})
    page[NameObject("/Resources")] = DictionaryObject({NameObject("/Font"): DictionaryObject({NameObject("/F1"): writer._add_object(font)})})
    stream = DecodedStreamObject()
    stream.set_data(("BT /F1 10 Tf 10 450 Td (" + text + ") Tj ET").encode("ascii"))
    page[NameObject("/Contents")] = writer._add_object(stream)
    writer.add_metadata({"/Title": "Historical decisions", "/Author": "Ada Muller", "/CreationDate": "D:20261019000000"})
    with path.open("wb") as output:
        writer.write(output)


class WorkflowCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.papers = self.root / "papers"
        self.papers.mkdir()
        self.pdf = self.root / "input.pdf"
        write_pdf(self.pdf)
        self.summaries = self.root / "SUMMARIES.md"
        self.synthesis = self.root / "SYNTHESIS.md"
        self.changelog = self.root / "CHANGELOG.md"
        self.summaries.write_text("# Summaries\n\n| Date | Authors | Title | Contribution | Source |\n|---|---|---|---|---|\n", encoding="utf-8")
        self.synthesis.write_text("# Synthesis\n\n| Date | Paper | Contribution | Limits |\n|---|---|---|---|\n", encoding="utf-8")
        self.changelog.write_text("# Changelog\n", encoding="utf-8")
        self.stack = contextlib.ExitStack()
        self.stack.enter_context(patch.multiple(ingest, ROOT=self.root, PAPERS=self.papers,
                SUMMARIES=self.summaries, SYNTHESIS=self.synthesis, CHANGELOG=self.changelog))
        self.stack.enter_context(patch.multiple(sync, _ROOT=self.root, _PAPERS=self.papers))
        self.stack.enter_context(patch.multiple(extraction, _ROOT=self.root, _PAPERS=self.papers, _TEXT=self.papers / "text"))
        self.stack.enter_context(patch.object(versions, "_TEXT", self.papers / "text"))

    def tearDown(self):
        self.stack.close()
        self.temp.cleanup()

    def run_ingest(self, reference=None, *args):
        reference = reference or item()
        with patch.object(ingest, "ZoteroReader", return_value=FakeZotero([reference], self.pdf)), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return ingest.main(["--zotero", reference["key"], "--yes", *args])

    def compare(self, references=None, pdf=True):
        fake = FakeZotero(references or [item()], self.pdf if pdf else None)
        return sync.compare(fake, fake.collection("Decision Models"))

    def test_historical_ingestion_preserves_curated_metadata_and_source(self):
        source = self.pdf.read_bytes()
        self.assertEqual(self.run_ingest(), 0)
        filed = next((self.papers / "1955").glob("*.pdf"))
        self.assertIn("06_Muller_and_van_der_Waals_", filed.name)
        self.assertEqual(filed.read_bytes(), source)
        self.assertEqual(self.pdf.read_bytes(), source)
        registry = json.loads((self.papers / "manifest.json").read_text())
        record = next(iter(registry["papers"].values()))
        self.assertEqual(record["citation_key"], "Muller1955")
        self.assertEqual(record["publication_date"], "1955-06")
        self.assertEqual(record["abstract"], "A decision-theory fixture.")
        self.assertEqual(record["sha256"], hashlib.sha256(source).hexdigest())
        self.assertIn("real PDF extraction fixture", next((self.papers / "text/1955").glob("*.txt")).read_text())
        self.assertIn("TODO(new-paper)", self.summaries.read_text())
        self.assertIn("1955-06", self.synthesis.read_text())
        self.assertEqual(self.compare()[1].total, 0)

    def test_year_only_never_invents_month_and_override_works(self):
        reference = item(date="1850")
        self.assertEqual(self.run_ingest(reference), 1)
        self.assertFalse((self.papers / "manifest.json").exists())
        self.assertEqual(self.run_ingest(reference, "--month", "3"), 0)
        record = next(iter(json.loads((self.papers / "manifest.json").read_text())["papers"].values()))
        self.assertEqual(record["publication_date"], "1850")
        self.assertEqual(record["filed_date"], "1850-03")
        self.assertEqual(record["date_source"], "explicit override")

    def test_pdf_creation_timestamp_not_a_publication_date(self):
        meta = ingest.from_pdf(self.pdf)
        self.assertEqual((meta.year, meta.month), ("", ""))

    def test_invalid_month_does_not_create_output(self):
        self.assertEqual(self.run_ingest(item(), "--month", "13"), 1)
        self.assertEqual(list(self.papers.iterdir()), [])

    def test_zotero_missing_date_can_be_overridden_before_validation(self):
        self.assertEqual(self.run_ingest(item(date=""), "--year", "1901", "--month", "4"), 0)
        self.assertTrue((self.papers / "1901").is_dir())

    def test_item_outside_collection_refused_even_with_pdf_fallback(self):
        reference = item()
        reference["data"]["collections"] = ["OTHER"]
        with self.assertRaisesRegex(ValueError, "not a live top-level"):
            ingest.from_zotero("ITEM1", self.pdf, reader=FakeZotero([reference]))

    def test_pdf_fallback_uses_zotero_metadata(self):
        meta, path = ingest.from_zotero("ITEM1", self.pdf, reader=FakeZotero([item()]))
        self.assertEqual(meta.title, item()["data"]["title"])
        self.assertEqual(path, self.pdf)

    def test_filed_version_banner_beats_publication_date(self):
        write_pdf(self.pdf, "arXiv:math/9912345v3 [math.OC] 15 Dec 1999")
        reference = item(date="2001-07")
        self.assertEqual(self.run_ingest(reference), 0)
        record = next(iter(json.loads((self.papers / "manifest.json").read_text())["papers"].values()))
        self.assertEqual((record["filed_date"], record["publication_date"], record["arxiv_version"]), ("1999-12", "2001-07", 3))
        _, report, notes = self.compare([reference])
        self.assertEqual(report.total, 0)
        self.assertTrue(notes)

    def test_dry_run_is_content_read_only(self):
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(self.run_ingest(item(), "--dry-run"), 0)
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_zotero_move_refused(self):
        self.assertEqual(self.run_ingest(item(), "--move"), 1)
        self.assertTrue(self.pdf.is_file())

    def test_duplicate_zotero_key_refused(self):
        self.assertEqual(self.run_ingest(), 0)
        self.assertEqual(self.run_ingest(item(), "--title", "Different Title"), 1)
        self.assertEqual(len(list(self.papers.glob("*/*.pdf"))), 1)

    def test_historical_scaffolds_sort_before_existing_rows_and_anchor(self):
        late = ingest.Meta("Later methods", ["An Author"], "2001", "01")
        early = ingest.Meta("Earlier methods", ["An Author"], "1901", "01")
        first = ingest.summaries_text(late, "papers/2001/a.pdf", self.summaries.read_text())
        final = ingest.summaries_text(early, "papers/1901/b.pdf", first)
        self.assertLess(final.index("| 1901-01"), final.index("| 2001-01"))
        self.assertLess(final.index("## 1901-01"), final.index('<a id="later-methods"'))

    def test_mixed_source_summaries_keep_new_papers_before_web_section(self):
        existing = ingest.Meta("Existing paper", ["An Author"], "2026", "10")
        paper_part = ingest.summaries_text(existing, "papers/2026/existing.pdf", self.summaries.read_text())
        web_part = ("## Web-source overview\n\n"
                    "| Date | Authors | Title | Contribution | Summary |\n"
                    "|---|---|---|---|---|\n"
                    "| 2026-11-03 | Provider | Dated release | Web only | [summary](#dated) |\n"
                    "| 2026 | Provider | Year-only release | Web only | [summary](#year-only) |\n\n"
                    '<a id="dated"></a>\n\n### 2026-11-03 — Dated release\n\nWeb prose.\n\n'
                    '<a id="year-only"></a>\n\n### 2026 — Year-only release\n\nWeb prose.\n')
        mixed = paper_part + "\n" + web_part
        for year, month, title in (("2031", "11", "Future paper"), ("1850", "03", "Historical paper")):
            with self.subTest(year=year):
                meta = ingest.Meta(title, ["A Researcher"], year, month)
                final = ingest.summaries_text(meta, f"papers/{year}/new.pdf", mixed)
                web_at = final.index("## Web-source overview")
                first_entry = final.index('<a id="')
                row_at = final.index(f"| {year}-{month} |")
                heading_at = final.index(f"## {year}-{month} —")
                self.assertLess(row_at, first_entry, "new overview row escaped the first table")
                self.assertLess(heading_at, web_at, "new PDF summary escaped the paper section")
                self.assertEqual(final[web_at:], web_part, "web rows or source summaries changed")
                if year == "1850":
                    self.assertLess(heading_at, final.index('<a id="existing-paper"'))
                    self.assertLess(row_at, final.index("| 2026-10 |"))
                else:
                    self.assertGreater(heading_at, final.index("## 2026-10 —"))
                    self.assertGreater(row_at, final.index("| 2026-10 |"))

    def test_mixed_source_timeline_insertion_never_enters_web_table(self):
        web_part = ("## Web-source timeline\n\n| Date | Source | Role |\n|---|---|---|\n"
                    "| 2026-11-03 | Dated release | Web only |\n"
                    "| 2026 | Year-only card | Month unresolved |\n\n## Argument\n\nCross-source prose.\n")
        paper_part = ingest.synthesis_text(ingest.Meta("Existing paper", ["An Author"], "2026", "10"), self.synthesis.read_text())
        mixed = paper_part + "\n" + web_part
        for year in ("1850", "2031"):
            with self.subTest(year=year):
                meta = ingest.Meta("New paper", ["A Researcher"], year, "03")
                final = ingest.synthesis_text(meta, mixed)
                web_at = final.index("## Web-source timeline")
                self.assertLess(final.index(f"| {year}-03 |"), web_at)
                self.assertEqual(final[web_at:], web_part)
                self.assertIn("[New paper](SUMMARIES.md#new-paper)", final[:web_at])
                dates = [line.split("|")[1].strip() for line in final[:web_at].splitlines()
                         if line.startswith("| 1") or line.startswith("| 2")]
                self.assertEqual(dates, sorted(dates))

    def test_atomic_failure_restores_prior_contents(self):
        first, second = self.root / "first.txt", self.root / "second.txt"
        first.write_bytes(b"original")
        original_replace, calls = os.replace, []
        def replace(src, dst):
            calls.append(dst)
            if len(calls) == 2:
                raise OSError("simulated replacement failure")
            return original_replace(src, dst)
        with patch.object(ingest.os, "replace", side_effect=replace):
            with self.assertRaises(OSError):
                ingest.atomic_batch({first: b"new", second: b"other"})
        self.assertEqual(first.read_bytes(), b"original")
        self.assertFalse(second.exists())
        self.assertFalse(list(self.root.glob("*.tmp")))

    def test_checker_reports_missing_extra_duplicate_and_metadata_drift(self):
        self.assertEqual(self.run_ingest(), 0)
        filed = next(self.papers.glob("*/*.pdf"))
        duplicate = filed.with_name("06_duplicate.pdf")
        duplicate.write_bytes(filed.read_bytes())
        extra = item(key="MISSING", title="A different research paper")
        changed = item()
        changed["data"]["title"] = "Changed curated title"
        report = self.compare([changed, extra])[1]
        self.assertIn("Registered metadata differs from Zotero", report.sections)
        self.assertIn("In Zotero collection but NOT in papers/", report.sections)
        self.assertIn("In papers/ but NOT in Zotero collection", report.sections)
        self.assertIn("PDFs with no text extraction", report.sections)
        registry_path = self.papers / "manifest.json"
        registry = json.loads(registry_path.read_text())
        registry["papers"][duplicate.relative_to(self.root).as_posix()] = next(iter(registry["papers"].values()))
        registry_path.write_text(json.dumps(registry))
        self.assertIn("Missing or duplicate registry Zotero key", self.compare()[1].sections)

    def test_checker_detects_orphan_text_and_hash_drift(self):
        self.assertEqual(self.run_ingest(), 0)
        filed = next(self.papers.glob("*/*.pdf"))
        filed.write_bytes(filed.read_bytes() + b"changed")
        (self.papers / "text/1955/orphan.txt").write_text("orphan")
        report = self.compare()[1]
        self.assertIn("PDF content differs from provenance hash", report.sections)
        self.assertIn("Text extraction without PDF", report.sections)

    def test_web_source_without_fake_pdf_is_covered(self):
        reference = item(date="1955")
        reference["data"]["itemType"] = "blogPost"
        web = {"zotero_item_key": "ITEM1", "title": reference["data"]["title"],
               "authors": sync.author_names(reference)[0], "publication_date": "1955",
               "citation_key": "Muller1955", "url": reference["data"]["url"],
               "archive_path": None, "status": "web-only"}
        (self.papers / "web_sources.json").write_text(json.dumps({"schema_version": 1, "sources": [web]}))
        stats, report, notes = self.compare([reference], pdf=False)
        self.assertEqual(report.total, 0)
        self.assertEqual(stats["registered web sources"], 1)
        self.assertTrue(notes)
        reference["data"]["itemType"] = "journalArticle"
        self.assertIn("Research source incorrectly registered as web-only", self.compare([reference], pdf=False)[1].sections)

    def test_web_snapshot_and_outside_collection_entries_checked(self):
        reference = item()
        reference["data"]["itemType"] = "blogPost"
        record = {"zotero_item_key": "ITEM1", "title": reference["data"]["title"],
                  "authors": sync.author_names(reference)[0], "publication_date": "1955-06", "citation_key": "Muller1955",
                  "url": reference["data"]["url"], "archive_path": "papers/web/missing.html"}
        unrelated = {**record, "zotero_item_key": "UNRELATED"}
        (self.papers / "web_sources.json").write_text(json.dumps({"schema_version": 1, "sources": [record, unrelated]}))
        report = self.compare([reference], pdf=False)[1]
        self.assertIn("Registered web snapshot absent", report.sections)
        self.assertIn("Registered source outside selected Zotero collection", report.sections)

    def test_no_arxiv_corpus_reports_unverifiable_and_succeeds(self):
        self.assertEqual(self.run_ingest(), 0)
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), patch.object(versions, "query_arxiv") as query:
            self.assertEqual(versions.main(["--json"]), 0)
        query.assert_not_called()
        self.assertEqual(len(json.loads(stdout.getvalue())["unverifiable"]), 1)

    def test_web_source_version_limits_are_informational_in_json_and_text(self):
        registry = {"schema_version": 1, "sources": [{"zotero_item_key": "WEB1",
                    "title": "Decision model release", "url": "https://example.test/release"}]}
        (self.papers / "web_sources.json").write_text(json.dumps(registry))
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), patch.object(versions, "query_arxiv") as query:
            self.assertEqual(versions.main(["--json"]), 0)
        query.assert_not_called()
        result = json.loads(stdout.getvalue())
        self.assertEqual(result["web_unverifiable"][0]["zotero_item_key"], "WEB1")
        self.assertIn("no filed PDF", result["web_unverifiable"][0]["reason"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.assertEqual(versions.main([]), 0)
        self.assertIn("UNVERIFIABLE WEB: WEB1", stdout.getvalue())
        self.assertIn("1 unverifiable web sources", stdout.getvalue())

    def test_version_checker_retains_duplicate_ids_and_reports_newer(self):
        folder = self.papers / "text/1999"
        folder.mkdir(parents=True)
        for name in ("12_First.txt", "12_Second.txt"):
            (folder / name).write_text("arXiv:math/9912345v2 [math.OC] 5 Dec 1999")
        local, unverified = versions.local_papers()
        self.assertEqual((len(local), len(unverified)), (2, 0))
        remote = {"math/9912345": {"latest_version": 3, "updated": "2000-01-01", "title": "A title"}}
        stdout = io.StringIO()
        with patch.object(versions, "query_arxiv", return_value=remote), contextlib.redirect_stdout(stdout):
            self.assertEqual(versions.main(["--json"]), 1)
        self.assertEqual(len(json.loads(stdout.getvalue())["outdated"]), 2)

    def test_unresolved_api_ids_and_unavailable_api_are_incomplete(self):
        folder = self.papers / "text/2026"
        folder.mkdir(parents=True)
        (folder / "10_A.txt").write_text("arXiv:2610.00001v1 [cs.LG] 4 Oct 2026")
        with patch.object(versions, "query_arxiv", return_value={}), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(versions.main(["--json"]), 2)
        with patch.object(sync.ZoteroReader, "collection", side_effect=urllib.error.URLError("offline")), contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(sync.main(["--json"]), 2)
        self.assertIn("No SQLite", json.loads(output.getvalue())["error"])


class ReaderCase(unittest.TestCase):
    def test_primary_submission_history_uses_latest_version_not_first_date(self):
        page = '''<meta name="citation_title" content="A &amp; B">
        <div class="submission-history">
        <strong>[v1]</strong> Mon, 1 Sep 2025 12:00:00 UTC (1 KB)
        <strong>[v3]</strong> Tue, 20 Oct 2026 08:00:00 UTC (2 KB)
        </div>'''
        result = versions.parse_submission_history(page)
        self.assertEqual(result["latest_version"], 3)
        self.assertEqual(result["updated"], "2026-10-20")
        self.assertEqual(result["title"], "A & B")
        with self.assertRaises(ValueError):
            versions.parse_submission_history("<html>unavailable</html>")

    def test_house_filename_removes_windows_invalid_characters(self):
        filename = ingest.house_filename(["Dœ", "Straße"], "03", 'A < B > C | D * E \\ F / G: "Decisions?"')
        self.assertEqual(filename, "03_Doe_and_Strasse_A_B_C_D_E_F_G_Decisions.pdf")
        self.assertFalse(any(character in filename for character in '<>:"/\\|?*'))

    def test_house_filename_rejects_empty_ascii_title(self):
        for title in ("中文", "<|*>?!", "..."):
            with self.subTest(title=title), self.assertRaisesRegex(ValueError, "transliterated title"):
                ingest.house_filename(["Smith"], "01", title)

    def test_pagination_preserves_query_and_collects_more_than_100(self):
        reader = sync.ZoteroReader()
        with patch.object(reader, "get", side_effect=[[{"key": str(i)} for i in range(100)], [{"key": "100"}]]) as get:
            self.assertEqual(len(reader.all("/items?format=json")), 101)
        self.assertIn("format=json", get.call_args_list[1].args[0])
        self.assertIn("start=100", get.call_args_list[1].args[0])

    def test_collection_selection_rejects_ambiguity_and_numeric_prefix(self):
        reader = sync.ZoteroReader()
        collections = [{"key": "A", "data": {"name": "07. Decision Models"}},
                       {"key": "B", "data": {"name": "10. Other Models"}}]
        with patch.object(reader, "all", return_value=collections):
            self.assertEqual(reader.collection("decision models")["key"], "A")
            for selector in ("Models", "07.", "missing"):
                with self.assertRaises(ValueError):
                    reader.collection(selector)

    def test_file_url_resolution_supports_linked_and_stored_files(self):
        reader = sync.ZoteroReader()
        with tempfile.TemporaryDirectory(prefix="zotero path ") as folder:
            path = Path(folder) / "Paper.pdf"
            path.write_bytes(b"pdf")
            with patch.object(reader, "get", return_value=path.as_uri()):
                self.assertEqual(reader.file_path("STORED").resolve(), path.resolve())
                self.assertEqual(reader.file_path("LINKED").resolve(), path.resolve())

    def test_arxiv_queries_batch_over_100_ids(self):
        with patch.object(versions, "_query_batch", return_value={}) as batch, patch.object(versions.time, "sleep"):
            versions.query_arxiv([str(i) for i in range(205)])
        self.assertEqual([len(call.args[0]) for call in batch.call_args_list], [100, 100, 5])


if __name__ == "__main__":
    unittest.main()
