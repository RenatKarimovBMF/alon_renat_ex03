"""Outline phase schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field, model_validator


class ChapterPlan(BaseModel):
    """One chapter in the book outline."""

    number: int = Field(ge=1)
    title: str
    page_budget: float = Field(gt=0)
    learning_objectives: list[str] = Field(min_length=1)
    section_titles: list[str] = Field(min_length=1)


class BookOutline(BaseModel):
    """Output of the Outline Architect task."""

    title: str
    target_total_pages: int = Field(default=15, ge=1)
    chapters: list[ChapterPlan] = Field(min_length=1)
    version: str = "1.0"

    @model_validator(mode="after")
    def page_budget_matches_target(self) -> BookOutline:
        total = sum(ch.page_budget for ch in self.chapters)
        delta = abs(total - self.target_total_pages)
        if delta > 1.5:
            msg = f"Chapter page budgets sum to {total}, expected ~{self.target_total_pages}"
            raise ValueError(msg)
        return self
