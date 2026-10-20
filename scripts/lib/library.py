"""Shared helpers for the maintenance scripts.

Everything that more than one script needs to know about the shape of this
repository lives here, so the scripts cannot drift apart in how they find
papers, parse identifiers, or slugify headings. That drift is not
hypothetical: two scripts once implemented GitHub's heading-slug rule
slightly differently, and the wrong one reported twelve valid anchors as
broken.

Import it from any script, at any nesting depth::

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from lib.library import ROOT, house_filename
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

# scripts/lib/library.py -> scripts/lib -> scripts -> <repo root>
ROOT = Path(__file__).resolve().parents[2]

PAPERS = ROOT / "papers"
TEXT = PAPERS / "text"
REPOSITORIES = ROOT / "repositories"

SUMMARIES = ROOT / "SUMMARIES.md"
SYNTHESIS = ROOT / "SYNTHESIS.md"
REPOS_DOC = ROOT / "REPOSITORIES.md"
CHANGELOG = ROOT / "CHANGELOG.md"

# The banner arXiv prints down the left margin of every page:
#   arXiv:2607.27546v1 [cs.LG] 30 Jul 2026
# It carries the date of the exact version on disk, which is what decides
# a paper's year folder and month prefix.
_ARXIV_STAMP = re.compile(
    r"arXiv:((?:\d{4}\.\d{4,5}|[a-zA-Z.\-]+/\d{7}))(?:v(\d+))?\s*(?:\[[a-zA-Z.\-]+\]\s*)?"
    r"(\d{1,2})\s+([A-Z][a-z]{2})\s+(\d{4})"
)
MONTHS = {m: i + 1 for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
     "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])}


def github_slug(heading: str) -> str:
    """Slugify a heading the way GitHub does.

    Lowercase, delete anything that is not a word character, space or
    hyphen, then replace each remaining space with a hyphen — **without**
    collapsing runs. ``Timeline & lineage`` becomes ``timeline--lineage``
    (two hyphens), because deleting the ``&`` leaves the spaces that
    surrounded it. Collapsing whitespace here produces a false failure on
    every heading containing punctuation.
    """
    s = heading.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    return s.replace(" ", "-")


def ascii_fold(s: str) -> str:
    """``Müller`` -> ``Muller``, as the paper filenames require."""
    s = s.translate(str.maketrans({"ß": "ss", "ẞ": "SS", "ø": "o", "Ø": "O", "ł": "l", "Ł": "L", "æ": "ae", "Æ": "AE", "œ": "oe", "Œ": "OE"}))
    return "".join(c for c in unicodedata.normalize("NFKD", s)
                   if not unicodedata.combining(c)).encode("ascii", "ignore").decode("ascii")


def house_filename(authors: list[str], month: str, title: str) -> str:
    """Build ``MM_Author_et_al._Title.pdf`` from metadata (AGENTS.md rule 3)."""
    def clean(s: str) -> str:
        s = ascii_fold(s)
        s = re.sub(r"[,?!:;'\"()\[\]&<>|*]", "", s)
        s = re.sub(r"[-–—/\\\s]+", "_", s)
        return re.sub(r"_+", "_", s).strip("_").rstrip(".")

    if not authors:
        seg = ""
    elif len(authors) == 1:
        seg = clean(authors[0])
    elif len(authors) == 2:
        seg = f"{clean(authors[0])}_and_{clean(authors[1])}"
    else:
        seg = f"{clean(authors[0])}_et_al."
    title_segment = clean(title)
    if not title_segment:
        raise ValueError("Title has no usable ASCII filename characters; provide a transliterated title override.")
    return f"{month}_{seg + '_' if seg else ''}{title_segment}.pdf"
