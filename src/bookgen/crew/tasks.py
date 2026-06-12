"""Build CrewAI tasks for the book pipeline."""

from __future__ import annotations

from crewai import Task

from bookgen.models import BookOutline, BuildReport, ResearchBrief, ReviewReport, SectionDraftBundle


def build_tasks(
    agents: dict[str, object],
    *,
    topic: str,
    target_pages: int,
    words_per_page: int = 300,
    bib_keys: list[str] | None = None,
) -> list[Task]:
    """Create sequential tasks wired to pydantic outputs."""
    # LLMs systematically undershoot word floors, so ask ~15% above target.
    target_words = int(target_pages * words_per_page * 1.15)
    keys = ", ".join(bib_keys) if bib_keys else "siddiqi2010"
    research = Task(
        description=(
            f"Research the topic '{topic}'. Use load_topic_context for framing. "
            "Return ResearchBrief JSON only."
        ),
        expected_output="Valid ResearchBrief JSON",
        agent=agents["research_director"],
        output_pydantic=ResearchBrief,
    )
    outline = Task(
        description=(
            f"Build a BookOutline with target_total_pages={target_pages}. "
            "Use the research brief context. Every chapter must include "
            "hebrew_summary: 1-2 complete Hebrew sentences summarizing it."
        ),
        expected_output="Valid BookOutline JSON",
        agent=agents["outline_architect"],
        context=[research],
        output_pydantic=BookOutline,
    )
    writer = Task(
        description=(
            "Write SectionDraftBundle JSON covering every outline section. "
            f"HARD LENGTH RULE: 5 paragraphs of 80-95 words EACH per section "
            f"(5 x ~85 = 400-450 words per section, no exceptions); "
            f"at least {target_words} words across the whole book. Before "
            "returning, recount every section and expand any under 400 words. "
            f"CITATIONS: choose 2-3 keys per section ONLY from [{keys}]; "
            "every key in that list MUST be cited at least once in the book. "
            "Plain paragraphs only."
        ),
        expected_output="Valid SectionDraftBundle JSON",
        agent=agents["chapter_writer"],
        context=[research, outline],
        output_pydantic=SectionDraftBundle,
    )
    review = Task(
        description=(
            "Review the drafted content and estimate pages with estimate_pages. "
            "Return ReviewReport JSON."
        ),
        expected_output="Valid ReviewReport JSON",
        agent=agents["latex_editor"],
        context=[outline, writer],
        output_pydantic=ReviewReport,
    )
    build = Task(
        description=(
            "Compile LaTeX using latex_compile and return BuildReport JSON. "
            "Do not claim success without a PDF path."
        ),
        expected_output="Valid BuildReport JSON",
        agent=agents["build_engineer"],
        context=[review],
        output_pydantic=BuildReport,
    )
    return [research, outline, writer, review, build]
