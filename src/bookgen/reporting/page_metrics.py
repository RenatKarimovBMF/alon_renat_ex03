"""PDF and document metrics."""

from __future__ import annotations

from pathlib import Path


def count_pdf_pages(pdf_path: Path) -> int | None:
    """Return page count when pypdf is available."""
    if not pdf_path.exists():
        return None
    try:
        from pypdf import PdfReader
    except ImportError:
        return None
    reader = PdfReader(str(pdf_path))
    return len(reader.pages)


def count_words_in_text(text: str) -> int:
    return len(text.split())
