"""Review phase schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ReviewReport(BaseModel):
    """LaTeX Editor quality gate before compilation."""

    estimated_pages: float = Field(gt=0)
    issues: list[str] = Field(default_factory=list)
    approved: bool
    glossary: dict[str, str] = Field(default_factory=dict)
    version: str = "1.0"
