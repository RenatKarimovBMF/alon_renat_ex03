"""Tests for page and word metrics."""

from pathlib import Path

from bookgen.reporting.page_metrics import count_pdf_pages, count_words_in_text

ROOT = Path(__file__).resolve().parents[2]


def test_count_words_in_text() -> None:
    assert count_words_in_text("one two three") == 3
    assert count_words_in_text("") == 0


def test_count_pdf_pages_missing_returns_none(tmp_path) -> None:
    assert count_pdf_pages(tmp_path / "nope.pdf") is None


def test_count_pdf_pages_on_real_pdf() -> None:
    pdf = ROOT / "latex" / "figures" / "mission_timeline.pdf"
    pages = count_pdf_pages(pdf)
    assert pages is not None
    assert pages >= 1
