"""Preserve complete UTF-8 source text while gitingest formats a snapshot.

Some gitingest versions sample only the first KiB and prefer the Windows locale:
valid UTF-8 can become mojibake, a binary marker, or a later decoding error.
The override is scoped to one synchronous ingestion and never changes the
installed package, system locale, notebooks, symlinks or binary fallback.
"""
from __future__ import annotations

from unittest.mock import patch


def ingest_utf8(ingest_fn, **kwargs):
    from gitingest.schemas.filesystem import FileSystemNode, FileSystemNodeType

    original = FileSystemNode.content

    def read_content(node):
        if node.type == FileSystemNodeType.FILE and node.path.suffix != ".ipynb":
            try:
                text = node.path.read_bytes().decode("utf-8")
            except (OSError, UnicodeDecodeError):
                pass
            else:
                if "\x00" not in text:
                    return text.replace("\r\n", "\n").replace("\r", "\n") or "[Empty file]"
        return original.fget(node)

    with patch.object(FileSystemNode, "content", property(read_content)):
        return ingest_fn(**kwargs)
