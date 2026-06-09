"""LaTeX build result schema."""

from __future__ import annotations

from pydantic import BaseModel, Field


class BuildReport(BaseModel):
    """Output of the Build Engineer compile step."""

    success: bool
    pdf_path: str | None = None
    attempts: int = Field(ge=0)
    errors: list[str] = Field(default_factory=list)
    log_path: str | None = None
    version: str = "1.0"
