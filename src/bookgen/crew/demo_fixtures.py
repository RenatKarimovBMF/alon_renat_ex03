"""Demo fixtures for offline and --demo runs."""

from __future__ import annotations

from bookgen.models import (
    BookOutline,
    ChapterPlan,
    Finding,
    ResearchBrief,
    SectionDraft,
    SectionDraftBundle,
)
from bookgen.shared.config import BookConfig


def build_demo_brief(book: BookConfig) -> ResearchBrief:
    return ResearchBrief(
        topic=book.topic,
        thesis="The Moon Race paired Soviet early firsts with an American lunar landing goal.",
        findings=[
            Finding(
                claim="Sputnik opened the space age in 1957",
                evidence_summary="The USSR placed the first artificial satellite in orbit",
                source_tag="external",
            ),
            Finding(
                claim="Gagarin's 1961 flight shocked American planners",
                evidence_summary="Human orbital flight arrived before US Mercury success",
                source_tag="external",
            ),
            Finding(
                claim="Apollo 11 reached the Moon in 1969",
                evidence_summary="NASA fulfilled Kennedy's landing pledge first",
                source_tag="external",
            ),
        ],
        open_questions=["Why did Soviet crewed lunar plans stall after the mid-1960s?"],
    )


def build_demo_outline(book: BookConfig) -> BookOutline:
    chapters = [
        ChapterPlan(
            number=1,
            title="Origins of the Moon Race",
            page_budget=7.5,
            learning_objectives=["Explain Cold War context"],
            section_titles=["Superpower rivalry", "Rocket technology"],
        ),
        ChapterPlan(
            number=2,
            title="From Sputnik to Apollo 11",
            page_budget=7.5,
            learning_objectives=["Compare Soviet and US milestones"],
            section_titles=["Early Soviet lead", "US lunar landing"],
        ),
    ]
    return BookOutline(title=book.topic, target_total_pages=15, chapters=chapters)


def build_demo_sections(outline: BookOutline) -> SectionDraftBundle:
    sections: list[SectionDraft] = []
    for chapter in outline.chapters:
        for title in chapter.section_titles:
            sections.append(
                SectionDraft(
                    chapter_number=chapter.number,
                    section_title=title,
                    body_paragraphs=[
                        f"This section discusses {title.lower()} during the Moon Race.",
                        "Both superpowers linked orbital achievements to national prestige.",
                    ],
                    citations=["siddiqi2010"],
                )
            )
    return SectionDraftBundle(sections=sections)
