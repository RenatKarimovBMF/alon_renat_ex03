"""Tests for production-length content."""

from bookgen.crew.production_content import (
    build_production_brief,
    build_production_outline,
    build_production_sections,
)
from bookgen.shared.config import load_book_config

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_production_brief_has_eight_findings() -> None:
    book = load_book_config(ROOT / "config" / "book.json")
    brief = build_production_brief(book)
    assert len(brief.findings) >= 8


def test_production_sections_meet_word_target() -> None:
    book = load_book_config(ROOT / "config" / "book.json")
    outline = build_production_outline(book)
    bundle = build_production_sections(outline, words_per_page=book.words_per_page)
    words = sum(
        len(" ".join(section.body_paragraphs).split()) for section in bundle.sections
    )
    assert words >= 6000
