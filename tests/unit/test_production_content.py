"""Tests for production-length content."""

from pathlib import Path

from bookgen.crew.moon_content import CITATIONS
from bookgen.crew.production_content import (
    build_production_brief,
    build_production_outline,
    build_production_sections,
)
from bookgen.shared.config import load_book_config

ROOT = Path(__file__).resolve().parents[2]


def test_production_brief_has_eight_findings() -> None:
    book = load_book_config(ROOT / "config" / "book.json")
    brief = build_production_brief(book)
    assert len(brief.findings) >= 8


def test_production_sections_have_distinct_prose() -> None:
    book = load_book_config(ROOT / "config" / "book.json")
    outline = build_production_outline(book)
    bundle = build_production_sections(outline, words_per_page=book.words_per_page)

    paragraphs = [p for section in bundle.sections for p in section.body_paragraphs]
    # No verbatim repetition: every paragraph in the book is unique.
    assert len(paragraphs) == len(set(paragraphs))
    # Still substantial, just not padded.
    words = sum(len(" ".join(s.body_paragraphs).split()) for s in bundle.sections)
    assert words >= 1200


def test_production_sections_cover_every_citation() -> None:
    book = load_book_config(ROOT / "config" / "book.json")
    outline = build_production_outline(book)
    bundle = build_production_sections(outline, words_per_page=book.words_per_page)

    used = {key for section in bundle.sections for key in section.citations}
    # Every bibliography source is referenced somewhere in the book.
    assert set(CITATIONS).issubset(used)
