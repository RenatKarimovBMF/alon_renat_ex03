"""Build CrewAI tasks for the book pipeline."""

from __future__ import annotations

from crewai import Task

from bookgen.models import BookOutline, BuildReport, ResearchBrief, ReviewReport, SectionDraftBundle


def build_tasks(agents: dict[str, object], *, topic: str, target_pages: int) -> list[Task]:
    """Create sequential tasks wired to pydantic outputs."""
    research = Task(
        description=(
            f"Research the topic '{topic}'. Use load_course_context. "
            "Return ResearchBrief JSON only."
        ),
        expected_output="Valid ResearchBrief JSON",
        agent=agents["research_director"],
        output_pydantic=ResearchBrief,
    )
    outline = Task(
        description=(
            f"Build a BookOutline with target_total_pages={target_pages}. "
            "Use the research brief context."
        ),
        expected_output="Valid BookOutline JSON",
        agent=agents["outline_architect"],
        context=[research],
        output_pydantic=BookOutline,
    )
    writer = Task(
        description=(
            "Write SectionDraftBundle JSON covering every outline section. "
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
