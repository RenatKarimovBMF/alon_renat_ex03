"""Tests for Pydantic models."""

import pytest

from bookgen.models import BookOutline, ChapterPlan, ResearchBrief


def test_research_brief_min_findings() -> None:
    with pytest.raises(ValueError):
        ResearchBrief.model_validate(
            {"topic": "t", "thesis": "x", "findings": [], "open_questions": []}
        )


def test_book_outline_page_budget_validation() -> None:
    chapters = [
        ChapterPlan(
            number=1,
            title="Intro",
            page_budget=5,
            learning_objectives=["a"],
            section_titles=["s1"],
        ),
        ChapterPlan(
            number=2,
            title="Body",
            page_budget=5,
            learning_objectives=["b"],
            section_titles=["s2"],
        ),
    ]
    outline = BookOutline(title="Book", target_total_pages=10, chapters=chapters)
    assert len(outline.chapters) == 2

    chapters[1].page_budget = 20
    with pytest.raises(ValueError):
        BookOutline(title="Book", target_total_pages=10, chapters=chapters)
