"""Distinct, human-readable prose for each Moon Race section.

Every section has its own paragraphs and citation keys, so the assembled book
reads as continuous narrative instead of a rotating template. The prose is
sized so the subject chapters alone fill at least 15 PDF pages (hard rule);
the data lives in ``moon_prose_early`` / ``moon_prose_late`` to honor the
150-line file cap. Citation keys are spread across all bibliography entries
so each source is actually referenced.
"""

from __future__ import annotations

from bookgen.crew.moon_prose_early import SECTIONS_EARLY
from bookgen.crew.moon_prose_late import SECTIONS_LATE

_SECTION_CONTENT: list[tuple[str, list[str], list[str]]] = SECTIONS_EARLY + SECTIONS_LATE

_PARAGRAPHS: dict[str, list[str]] = {title: paras for title, paras, _ in _SECTION_CONTENT}
_CITATIONS: dict[str, list[str]] = {title: cites for title, _, cites in _SECTION_CONTENT}


def section_paragraphs(chapter_title: str, section_title: str) -> list[str]:
    """Return distinct paragraphs for a section, with a safe generic fallback."""
    paragraphs = _PARAGRAPHS.get(section_title)
    if paragraphs:
        return list(paragraphs)
    return [
        f"This section of {chapter_title} examines {section_title.lower()} and its "
        "place in the wider Moon Race narrative.",
    ]


def section_citations(section_title: str) -> list[str]:
    """Return the bibliography keys assigned to a section."""
    return list(_CITATIONS.get(section_title, ["siddiqi2010"]))
