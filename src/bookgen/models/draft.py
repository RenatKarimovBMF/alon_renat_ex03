"""Draft writing schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class SectionDraft(BaseModel):
    """One section produced by the Chapter Writer."""

    chapter_number: int = Field(ge=1)
    section_title: str
    body_paragraphs: list[str] = Field(min_length=1)
    citations: list[str] = Field(default_factory=list)
