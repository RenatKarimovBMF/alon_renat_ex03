"""Research phase schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class Finding(BaseModel):
    """One researched claim with provenance."""

    claim: str
    evidence_summary: str
    source_tag: Literal["course_pdf", "external", "team_analysis"]


class SourceRef(BaseModel):
    """One real published source for the bibliography (live runs).

    The key doubles as the BibTeX citation key, so it must be a safe slug.
    """

    key: str = Field(pattern=r"^[a-z][a-z0-9_]{2,30}$")
    title: str = Field(min_length=4, max_length=200)
    author: str = Field(min_length=2, max_length=120)
    year: int = Field(ge=1400, le=2100)
    publisher: str = Field(default="", max_length=120)


class ResearchBrief(BaseModel):
    """Output of the Research Director task."""

    topic: str
    thesis: str
    findings: list[Finding] = Field(min_length=1)
    open_questions: list[str] = Field(default_factory=list)
    # Real published sources about the topic; live runs generate the book's
    # bibliography from these (fixtures keep the curated references.bib).
    sources: list[SourceRef] = Field(default_factory=list)
    version: str = "1.0"
