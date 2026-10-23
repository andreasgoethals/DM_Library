"""Regression for Windows locale decoding and split UTF-8 samples."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "dumps"))
from utf8_ingest import ingest_utf8


class Utf8IngestionTests(unittest.TestCase):
    def test_utf8_after_ascii_prefix_and_across_sample_boundary_is_preserved(self):
        from gitingest import ingest
        from gitingest.schemas.filesystem import FileSystemNode
        original = FileSystemNode.content
        sources = {
            "late.md": "a" * 1100 + "中文 — café\n",
            "boundary.md": "a" * 1023 + "é 中文\n",
        }
        with tempfile.TemporaryDirectory() as directory:
            for name, body in sources.items():
                (Path(directory) / name).write_text(body, encoding="utf-8")
            with patch("gitingest.schemas.filesystem._get_preferred_encodings",
                       return_value=["cp1252", "utf-8"]):
                _, _, content = ingest_utf8(ingest, source=directory, output=None)
        for name, body in sources.items():
            self.assertIn("FILE: " + name, content)
            self.assertIn(body, content)
        self.assertNotIn("Error reading file", content)
        self.assertNotIn("[Binary file]", content)
        self.assertIs(FileSystemNode.content, original)

    def test_reader_is_restored_when_ingestion_fails(self):
        from gitingest.schemas.filesystem import FileSystemNode
        original = FileSystemNode.content
        def fail(**kwargs):
            raise OSError("fixture failure")
        with self.assertRaises(OSError):
            ingest_utf8(fail, source="fixture", output=None)
        self.assertIs(FileSystemNode.content, original)
