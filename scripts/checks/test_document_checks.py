"""Offline identity/chronology/link/source-map regression fixtures."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


docs = load("check_docs")
symbols = load("check_symbols")


class DocumentFixtures(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.patch = patch.object(docs, "_ROOT", self.root)
        self.patch.start()
        for doc in docs.DOCS:
            (self.root / doc).write_text("# Document\n", encoding="utf-8")
        self.pdf = "papers/1961/03_Smith_and_Jones_Decisions.pdf"
        self.write(self.pdf, "fixture")
        self.write("papers/text/1961/03_Smith_and_Jones_Decisions.txt", "extracted fixture")
        self.write("SUMMARIES.md", f"""# Summaries
## Overview
| Date | Authors | Title | PDF |
|---|---|---|---|
| 1961-03 | Smith and Jones | Decisions | [pdf]({self.pdf}) |
<a id="decisions"></a>
## 1961-03 — Decisions
**Venue:** Decision Journal.
**Zotero citation key:** `Smith1961`
[PDF]({self.pdf})
**Where it fits:** Decision theory.
**What it contains:** A comparison of actions.
**Strengths:** Clear assumptions.
**Limitations:** Stylized setting.
""")
        self.write("SYNTHESIS.md", "# Synthesis\n| 1961-03 | [Decisions](SUMMARIES.md#decisions) | Theory |\n")
        self.write("CHANGELOG.md", "# Changelog\n## 2026-01-01\nInitial fixture.\n")

    def tearDown(self):
        self.patch.stop()
        self.temp.cleanup()

    def write(self, path, text):
        dest = self.root / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")

    def report(self):
        report = docs.Report()
        docs.check_coverage(report)
        docs.check_links_and_anchors(report)
        docs.check_changelog(report)
        docs.check_placeholders(report)
        return report

    def test_historical_two_author_fixture_passes(self):
        self.assertEqual(self.report().problems, [])

    def test_duplicate_same_month_identity_not_hidden_by_count(self):
        self.write("SYNTHESIS.md", "| 1961-03 | [Missing](SUMMARIES.md#unrelated) |\n")
        problems = self.report().problems
        self.assertTrue(any("identity/order" in message for message in problems))
        self.assertTrue(any("unresolved anchor" in message for message in problems))

    def test_citation_key_and_todo_gates(self):
        summary = (self.root / "SUMMARIES.md").read_text(encoding="utf-8")
        self.write("SUMMARIES.md", summary.replace("**Zotero citation key:** `Smith1961`", "TODO(new-paper)"))
        problems = self.report().problems
        self.assertTrue(any("citation key" in message for message in problems))
        self.assertTrue(any("unfinished" in message for message in problems))

    def test_cross_document_urlencoded_anchor_and_duplicate_heading(self):
        self.write("README.md", "[one](AGENTS.md#timeline--lineage) [two](AGENTS.md#timeline--lineage-1)\n")
        self.write("AGENTS.md", "# Timeline & lineage\n# Timeline & lineage\n")
        report = docs.Report()
        docs.check_links_and_anchors(report)
        self.assertEqual(report.problems, [])

    def test_source_maps_allow_upstream_paths_but_reject_local_context(self):
        self.write("REPOSITORIES.md", "Upstream uses `src/train/`.\n")
        report = docs.Report()
        docs.check_neutrality(report)
        self.assertEqual(report.problems, [])
        self.write("REPOSITORIES.md", "Our `src/train/` configuration is project-specific.\n")
        docs.check_neutrality(report)
        self.assertTrue(report.problems)

    def test_web_source_separate_from_pdf_corpus(self):
        self.write("papers/web_sources.json", json.dumps({"schema_version": 1, "sources": [{
            "zotero_item_key": "AB12", "citation_key": "Web1962", "title": "Web source",
            "publication_date": "1962", "url": "https://example.org/source", "status": "web-only",
            "archive_path": None}]}))
        with (self.root / "SUMMARIES.md").open("a", encoding="utf-8") as output:
            output.write("""
## Web-source overview
| 1962 | [Web source](#web-ab12) |
## Web sources
<a id="web-ab12"></a>
### 1962 — Web source
**Venue:** Example.
**Zotero citation key:** `Web1962`
[Source](https://example.org/source)
**Where it fits:** Context.
**What it contains:** Overview.
**Strengths:** Primary release.
**Limitations:** No paper or immutable PDF.
""")
        with (self.root / "SYNTHESIS.md").open("a", encoding="utf-8") as output:
            output.write("\n## Web-source timeline\n| 1962 | [Web](SUMMARIES.md#web-ab12) |\n")
        report = self.report()
        docs.check_web_sources(report)
        self.assertEqual(report.problems, [])


class SymbolFixtures(unittest.TestCase):
    def test_identifier_boundaries(self):
        self.assertFalse(symbols.symbol_present("old_symbol", "new_old_symbol"))
        self.assertTrue(symbols.symbol_present("old_symbol", "def old_symbol():"))

    def test_heading_attribution_ends_at_peer_section(self):
        parts = symbols.dump_sections("## `Demo.txt`\n`solve_problem`\n### Detail\n`data.json`\n## Refresh\n`unrelated_symbol`\n")
        self.assertEqual(len(parts), 2)
        self.assertNotIn("unrelated_symbol", " ".join(body for _, body in parts))

    def test_missing_snapshot_and_symbol_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "repositories").mkdir()
            (root / "REPOSITORIES.md").write_text("## `Demo.txt`\n`solve_problem`\n", encoding="utf-8")
            with patch.object(symbols, "ROOT", root), patch.object(symbols, "REPOSITORIES", root / "repositories"), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(symbols.main(["--doc", "REPOSITORIES.md"]), 1)
                (root / "repositories/Demo.txt").write_text("def wrong_symbol(): pass", encoding="utf-8")
                self.assertEqual(symbols.main(["--doc", "REPOSITORIES.md"]), 1)
                (root / "repositories/Demo.txt").write_text("def solve_problem(): pass", encoding="utf-8")
                self.assertEqual(symbols.main(["--doc", "REPOSITORIES.md"]), 0)


if __name__ == "__main__":
    unittest.main()
