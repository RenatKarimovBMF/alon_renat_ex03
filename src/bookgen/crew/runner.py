"""Run the CrewAI book pipeline."""

from __future__ import annotations

import shutil
import uuid
from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from functools import partial
from pathlib import Path

from bookgen.crew.assemble import assemble_latex, build_review
from bookgen.crew.content_loader import load_content
from bookgen.crew.context import PipelineContext
from bookgen.crew.extras import load_extras_plan
from bookgen.latex.figures import ensure_figures
from bookgen.latex.workspace import stage_latex_workspace
from bookgen.models import BuildReport, ReviewReport
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
    compile_pdf: Callable[[Path, Path], BuildReport],
    project_root: Path,
    mode: PipelineMode = PipelineMode.PRODUCTION,
    workspace: Path | None = None,
) -> PipelineResult:
    """Execute demo, production fixtures, or live CrewAI, then assemble and compile.

    With ``workspace`` set (live runs), all artifacts land in an isolated
    example folder and the canonical ``latex/`` tree and ``docs/COST.md``
    are left untouched.
    """
    session_id = uuid.uuid4().hex[:8]
    if workspace is not None:
        stage_latex_workspace(project_root / "latex", workspace / "latex")
    ctx = PipelineContext.create(
        session_id=session_id,
        setup=setup,
        book=book,
        project_root=project_root,
        workspace=workspace,
    )

    def log_fn(payload: dict[str, object]) -> None:
        payload["session_id"] = session_id
        append_jsonl(ctx.log_path, payload)

    llm = LlmClient(gatekeeper, log_fn=log_fn)
    brief, outline, bundle = load_content(ctx, llm, mode.value)

    save_json(ctx.session_dir / "01_research.json", brief)
    save_json(ctx.session_dir / "02_outline.json", outline)
    save_json(ctx.session_dir / "03_sections.json", bundle)

    plan = load_extras_plan(book)
    figures_fn = partial(
        ensure_figures,
        figures=plan.figure_tuples(),
        bundled_dir=project_root / "assets" / "chapter-figures",
    )
    assemble_latex(
        ctx.latex_root,
        ctx.main_tex,
        outline,
        bundle,
        ensure_figures_fn=figures_fn,
        extras_plan=plan,
    )
    review = build_review(
        outline,
        bundle,
        words_per_page=book.words_per_page,
        tolerance=book.page_tolerance,
    )
    save_json(ctx.session_dir / "05_review.json", review)

    build = compile_pdf(ctx.main_tex, ctx.build_dir)
    save_json(ctx.session_dir / "06_build.json", build)

    cost_path = ctx.session_dir / "COST.md"
    write_cost_report(ctx.log_path, cost_path, mode=mode.value)
    if workspace is None:
        write_cost_report(ctx.log_path, project_root / "docs" / "COST.md", mode=mode.value)
    elif build.success and build.pdf_path:
        shutil.copy2(build.pdf_path, workspace / "book.pdf")

    return PipelineResult(session_id, ctx.session_dir, ctx.log_path, review, build, mode, cost_path)
