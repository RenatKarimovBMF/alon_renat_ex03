"""Construct the CrewAI crew."""

from __future__ import annotations

from crewai import Crew, Process

from bookgen.crew.agents import build_agents
from bookgen.crew.context import PipelineContext
from bookgen.crew.tasks import build_tasks
from bookgen.latex.bib import read_bib_keys
from bookgen.sdk.llm_client import LlmClient


def build_crew(
    ctx: PipelineContext,
    llm_client: LlmClient,
    *,
    llm_tasks_only: bool = True,
) -> Crew:
    """Build a sequential CrewAI crew for the book pipeline."""
    agents = build_agents(ctx, llm_client)
    tasks = build_tasks(
        agents,
        topic=ctx.book.topic,
        target_pages=ctx.book.target_pages,
        words_per_page=ctx.book.words_per_page,
        bib_keys=read_bib_keys(ctx.latex_root / "references.bib"),
    )
    if llm_tasks_only:
        tasks = tasks[:3]
    used = list(dict.fromkeys(task.agent for task in tasks))
    verbose = bool(ctx.book.crew.get("verbose", True))
    return Crew(
        agents=used,
        tasks=tasks,
        process=Process.sequential,
        verbose=verbose,
    )
