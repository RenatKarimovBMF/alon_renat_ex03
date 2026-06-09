"""Bundled section drafts for CrewAI task output."""

from __future__ import annotations

from pydantic import BaseModel, Field

from bookgen.models.draft import SectionDraft


class SectionDraftBundle(BaseModel):
    """Chapter Writer task output."""

    sections: list[SectionDraft] = Field(min_length=1)
