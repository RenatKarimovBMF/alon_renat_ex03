"""Tests for the agent-sourced bibliography writer and citation filter."""

from pathlib import Path

import pytest

from bookgen.latex.bib_write import filter_citations, write_bibliography
from bookgen.models import SectionDraft, SectionDraftBundle, SourceRef


def _sources() -> list[SourceRef]:
    return [
        SourceRef(
            key="weinberg1994",
            title="A World at Arms: A Global History of World War II",
            author="Weinberg, Gerhard L.",
            year=1994,
            publisher="Cambridge University Press",
        ),
        SourceRef(
            key="beevor2012",
            title="The Second World War",
            author="Beevor, Antony",
            year=2012,
        ),
    ]


def test_write_bibliography_renders_entries_and_meta(tmp_path: Path) -> None:
    path = tmp_path / "references.bib"
    valid = write_bibliography(_sources(), path)
    text = path.read_text(encoding="utf-8")
    assert "@book{weinberg1994," in text and "@book{beevor2012," in text
    assert "Cambridge University Press" in text
    assert "@article{team2026," in text and "@misc{crewai2026," in text
    assert valid == {"weinberg1994", "beevor2012", "team2026", "crewai2026"}


def test_write_bibliography_sanitizes_tex(tmp_path: Path) -> None:
    source = SourceRef(
        key="evil2020",
        title=r"Bad \input{x} title with {braces} and % signs",
        author="Doe, J.",
        year=2020,
    )
    text_path = tmp_path / "references.bib"
    write_bibliography([source], text_path)
    text = text_path.read_text(encoding="utf-8")
    assert "\\input" not in text and "{braces}" not in text and "%" not in text


def test_source_key_must_be_slug() -> None:
    with pytest.raises(ValueError):
        SourceRef(key="Bad Key!", title="Some Title", author="A. B.", year=2000)


def test_filter_citations_drops_unknown_keys() -> None:
    bundle = SectionDraftBundle(
        sections=[
            SectionDraft(
                chapter_number=1,
                section_title="S",
                body_paragraphs=["Text."],
                citations=["weinberg1994", "hallucinated2099", "team2026"],
            )
        ]
    )
    dropped = filter_citations(bundle, {"weinberg1994", "team2026"})
    assert dropped == 1
    assert bundle.sections[0].citations == ["weinberg1994", "team2026"]
