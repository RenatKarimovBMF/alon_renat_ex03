"""Research phase schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class Finding(BaseModel):
    """One researched claim with provenance."""

    claim: str
    evidence_summary: str
    source_tag: Literal["course_pdf", "external", "team_analysis"]


class ResearchBrief(BaseModel):
    """Output of the Research Director task."""

    topic: str
    thesis: str
    findings: list[Finding] = Field(min_length=1)
    open_questions: list[str] = Field(default_factory=list)
    version: str = "1.0"
