"""Load book content for a pipeline run (fixtures or live CrewAI)."""

from __future__ import annotations

from pydantic import BaseModel

from bookgen.crew.context import PipelineContext
from bookgen.crew.demo_fixtures import (
    build_demo_brief,
    build_demo_outline,
    build_demo_sections,
)
from bookgen.crew.production_content import (
    build_production_brief,
    build_production_outline,
    build_production_sections,
)
from bookgen.models import BookOutline, ResearchBrief, SectionDraftBundle
from bookgen.sdk.llm_client import LlmClient

ContentTriple = tuple[ResearchBrief, BookOutline, SectionDraftBundle]


def load_content(ctx: PipelineContext, llm: LlmClient, mode: str) -> ContentTriple:
    """Return (brief, outline, sections) for ``demo`` / ``production`` / ``live``."""
    if mode == "demo":
        brief = build_demo_brief(ctx.book)
        outline = build_demo_outline(ctx.book)
        return brief, outline, build_demo_sections(outline)
    if mode == "production":
        brief = build_production_brief(ctx.book)
        outline = build_production_outline(ctx.book)
        bundle = build_production_sections(outline, words_per_page=ctx.book.words_per_page)
        return brief, outline, bundle
    return _run_live_crew(ctx, llm)


def _run_live_crew(ctx: PipelineContext, llm: LlmClient) -> ContentTriple:
    from bookgen.crew.factory import build_crew

    crew = build_crew(ctx, llm, llm_tasks_only=True)
    result = crew.kickoff(inputs={"topic": ctx.book.topic})
    outputs = result.tasks_output
    if len(outputs) < 3:
        raise RuntimeError("Crew finished without three LLM task outputs")

    brief = _expect_model(outputs[0].pydantic, ResearchBrief)
    outline = _expect_model(outputs[1].pydantic, BookOutline)
    bundle = _expect_model(outputs[2].pydantic, SectionDraftBundle)
    return brief, outline, bundle


def _expect_model(value: BaseModel | None, model_type: type[BaseModel]) -> BaseModel:
    if value is None or not isinstance(value, model_type):
        raise RuntimeError(f"Expected {model_type.__name__} output from crew task")
    return value
