"""Pydantic models for crew handoffs."""

from bookgen.models.build_report import BuildReport
from bookgen.models.draft import SectionDraft
from bookgen.models.outline import BookOutline, ChapterPlan
from bookgen.models.research import Finding, ResearchBrief
from bookgen.models.review import ReviewReport
from bookgen.models.sections import SectionDraftBundle

__all__ = [
    "BookOutline",
    "BuildReport",
    "ChapterPlan",
    "Finding",
    "ResearchBrief",
    "ReviewReport",
    "SectionDraft",
    "SectionDraftBundle",
]
