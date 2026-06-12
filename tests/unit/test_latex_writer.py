"""Tests for LaTeX escaping and writing."""

from pathlib import Path

import pytest

from bookgen.latex.blocks import render_hebrew_summary
from bookgen.latex.escape import escape_latex
from bookgen.latex.writer import guard_latex_path, render_section, write_chapter_file
from bookgen.models import SectionDraft


def test_escape_latex_special_chars() -> None:
    assert escape_latex("100% & _") == r"100\% \& \_"


def test_hebrew_summary_keeps_digits_ltr() -> None:
    # Years inside RTL Hebrew must stay LTR or 1961 renders as 1691.
    rendered = render_hebrew_summary("בשנת 1961 שוגר אפולו 11.")
    assert r"{\beginL 1961\endL}" in rendered
    assert r"{\beginL 11\endL}" in rendered


def test_hebrew_summary_keeps_latin_runs_ltr() -> None:
    # Latin compounds like the N1 rocket must stay LTR inside Hebrew.
    rendered = render_hebrew_summary("כישלונות הטיל N1 בשנת 1969.")
    assert r"{\beginL N1\endL}" in rendered


def test_render_section_adds_citations() -> None:
    section = SectionDraft(
        chapter_number=1,
        section_title="Intro",
        body_paragraphs=["Agents need tools."],
        citations=["crewai2024"],
    )
    rendered = render_section(section)
    assert r"\cite{crewai2024}" in rendered
    assert "Agents need tools." in rendered


def test_guard_latex_path_blocks_escape(tmp_path: Path) -> None:
    root = tmp_path / "latex"
    root.mkdir()
    with pytest.raises(ValueError):
        guard_latex_path(root, "../outside.tex")


def test_write_chapter_file(tmp_path: Path) -> None:
    sections = [
        SectionDraft(
            chapter_number=1,
            section_title="Scope",
            body_paragraphs=["Plain text."],
            citations=[],
        )
    ]
    path = write_chapter_file(tmp_path, 1, "Intro Chapter", sections)
    assert path.exists()
    assert "Plain text." in path.read_text(encoding="utf-8")
