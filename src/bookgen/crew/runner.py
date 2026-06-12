"""Run the CrewAI book pipeline."""

from __future__ import annotations

import uuid
from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel

from bookgen.crew.assemble import assemble_latex, build_review
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
from bookgen.models import BookOutline, BuildReport, ResearchBrief, ReviewReport, SectionDraftBundle
from bookgen.reporting.cost_report import write_cost_report
from bookgen.sdk.llm_client import LlmClient, append_jsonl
from bookgen.shared.config import BookConfig, SetupConfig
from bookgen.shared.gatekeeper import ApiGatekeeper
from bookgen.shared.json_io import save_json


class PipelineMode(StrEnum):
    DEMO = "demo"
    PRODUCTION = "production"
    LIVE = "live"


@dataclass(frozen=True)
class PipelineResult:
    session_id: str
    session_dir: Path
    log_path: Path
    review: ReviewReport
    build: BuildReport
    mode: PipelineMode
    cost_report_path: Path


def run_book_pipeline(
    *,
    setup: SetupConfig,
    book: BookConfig,
    gatekeeper: ApiGatekeeper,
    compile_pdf: Callable[[], BuildReport],
    project_root: Path,
    mode: PipelineMode = PipelineMode.PRODUCTION,
) -> PipelineResult:
    """Execute demo, production fixtures, or live CrewAI, then assemble and compile."""
    session_id = uuid.uuid4().hex[:8]
    ctx = PipelineContext.create(
        session_id=session_id,
        setup=setup,
        book=book,
        project_root=project_root,
    )

    def log_fn(payload: dict[str, object]) -> None:
        payload["session_id"] = session_id
        append_jsonl(ctx.log_path, payload)

    llm = LlmClient(gatekeeper, log_fn=log_fn)
    brief, outline, bundle = _load_content(ctx, llm, mode)

    save_json(ctx.session_dir / "01_research.json", brief)
    save_json(ctx.session_dir / "02_outline.json", outline)
    save_json(ctx.session_dir / "03_sections.json", bundle)

    assemble_latex(ctx.latex_root, ctx.main_tex, outline, bundle)
    review = build_review(
        outline,
        bundle,
        words_per_page=book.words_per_page,
        tolerance=book.page_tolerance,
    )
    save_json(ctx.session_dir / "05_review.json", review)

    build = compile_pdf()
    save_json(ctx.session_dir / "06_build.json", build)

    cost_path = ctx.session_dir / "COST.md"
    write_cost_report(ctx.log_path, cost_path, mode=mode.value)
    docs_cost = project_root / "docs" / "COST.md"
    write_cost_report(ctx.log_path, docs_cost, mode=mode.value)

    return PipelineResult(session_id, ctx.session_dir, ctx.log_path, review, build, mode, cost_path)


def _load_content(
    ctx: PipelineContext,
    llm: LlmClient,
    mode: PipelineMode,
) -> tuple[ResearchBrief, BookOutline, SectionDraftBundle]:
    if mode is PipelineMode.DEMO:
        brief = build_demo_brief(ctx.book)
        outline = build_demo_outline(ctx.book)
        bundle = build_demo_sections(outline)
        return brief, outline, bundle
    if mode is PipelineMode.PRODUCTION:
        brief = build_production_brief(ctx.book)
        outline = build_production_outline(ctx.book)
        bundle = build_production_sections(outline, words_per_page=ctx.book.words_per_page)
        return brief, outline, bundle
    return _run_live_crew(ctx, llm)


def _run_live_crew(
    ctx: PipelineContext,
    llm: LlmClient,
) -> tuple[ResearchBrief, BookOutline, SectionDraftBundle]:
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
