"""Generate full-length production book content (~15 pages)."""

from __future__ import annotations

from bookgen.crew.moon_content import (
    CHAPTERS,
    CITATIONS,
    FINDINGS,
    OPEN_QUESTIONS,
    THESIS,
    paragraph_templates,
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
    words_per_page: int,
) -> SectionDraftBundle:
    target_words = outline.target_total_pages * words_per_page
    section_count = sum(len(ch.section_titles) for ch in outline.chapters)
    words_per_section = max(target_words // max(section_count, 1), 400)

    sections: list[SectionDraft] = []
    for chapter in outline.chapters:
        for section_title in chapter.section_titles:
            sections.append(
                SectionDraft(
                    chapter_number=chapter.number,
                    section_title=section_title,
                    body_paragraphs=_paragraphs_for_section(
                        chapter.title,
                        section_title,
                        words_per_section,
                    ),
                    citations=CITATIONS[: 2 + (chapter.number % 2)],
                )
            )
    return SectionDraftBundle(sections=sections)


def _paragraphs_for_section(chapter_title: str, section_title: str, word_target: int) -> list[str]:
    templates = paragraph_templates(chapter_title, section_title)
    paragraphs: list[str] = []
    words = 0
    idx = 0
    while words < word_target:
        paragraphs.append(templates[idx % len(templates)])
        words += len(paragraphs[-1].split())
        idx += 1
    return paragraphs
