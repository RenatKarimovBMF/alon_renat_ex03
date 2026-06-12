"""Build CrewAI agents from YAML prompts."""

from __future__ import annotations

from crewai import Agent

from bookgen.crew.context import PipelineContext
from bookgen.crew.gatekeeper_llm import GatekeeperLLM
from bookgen.crew.prompts import load_prompts
from bookgen.crew.tools import build_tools
from bookgen.sdk.llm_client import LlmClient


def _agent(
    prompt: object,
    llm: GatekeeperLLM,
    tools: list[object],
) -> Agent:
    return Agent(
        role=prompt.role,
        goal=prompt.goal,
        backstory=f"{prompt.backstory}\n\n{prompt.instructions}",
        llm=llm,
        tools=tools,
        verbose=True,
        allow_delegation=False,
    )


def build_agents(ctx: PipelineContext, llm_client: LlmClient) -> dict[str, Agent]:
    """Instantiate all pipeline agents."""
    prompts = load_prompts(ctx.project_root / "config" / "prompts")
    tool_map = build_tools(ctx)
    llm = GatekeeperLLM(llm_client)

    return {
        "research_director": _agent(
            prompts["research_director"],
            llm,
            [tool_map["load_topic_context"], tool_map["write_session_artifact"]],
        ),
        "outline_architect": _agent(
            prompts["outline_architect"],
            llm,
            [tool_map["write_session_artifact"]],
        ),
        "chapter_writer": _agent(
            prompts["chapter_writer"],
            llm,
            [tool_map["write_session_artifact"]],
        ),
        "latex_editor": _agent(
            prompts["latex_editor"],
            llm,
            [tool_map["estimate_pages"], tool_map["write_session_artifact"]],
        ),
        "build_engineer": _agent(
            prompts["build_engineer"],
            llm,
            [tool_map["latex_compile"], tool_map["write_session_artifact"]],
        ),
    }
