"""Generate full-length production book content (~15 pages)."""

from __future__ import annotations

from bookgen.crew.moon_content import (
    CHAPTERS,
    FINDINGS,
    OPEN_QUESTIONS,
    THESIS,
    section_citations,
    section_paragraphs,
)
from bookgen.models import (
    BookOutline,
    ChapterPlan,
    Finding,
    ResearchBrief,
    SectionDraft,
    SectionDraftBundle,
)
from bookgen.shared.config import BookConfig


def build_production_brief(book: BookConfig) -> ResearchBrief:
    findings = [
        Finding(
            claim=claim,
            evidence_summary=evidence,
            source_tag=source_tag,  # noqa: PGH003
        )
        for claim, evidence, source_tag in FINDINGS
    ]
    return ResearchBrief(
        topic=book.topic,
        thesis=THESIS,
        findings=findings,
        open_questions=OPEN_QUESTIONS,
    )


def build_production_outline(book: BookConfig) -> BookOutline:
    per_chapter = round(book.target_pages / len(CHAPTERS), 2)
    chapters = [
        ChapterPlan(
            number=index,
            title=title,
            page_budget=per_chapter,
            learning_objectives=[f"Understand {title.lower()}"],
            section_titles=sections,
        )
        for index, (title, sections) in enumerate(CHAPTERS, start=1)
    ]
    return BookOutline(title=book.topic, target_total_pages=book.target_pages, chapters=chapters)


def build_production_sections(
    outline: BookOutline,
    *,
    words_per_page: int,  # noqa: ARG001 - kept for API symmetry with the live writer
) -> SectionDraftBundle:
    """Build sections from curated, non-repeating prose (one entry per section)."""
    sections: list[SectionDraft] = []
    for chapter in outline.chapters:
        for section_title in chapter.section_titles:
            sections.append(
                SectionDraft(
                    chapter_number=chapter.number,
                    section_title=section_title,
                    body_paragraphs=section_paragraphs(chapter.title, section_title),
                    citations=section_citations(section_title),
                )
            )
    return SectionDraftBundle(sections=sections)
