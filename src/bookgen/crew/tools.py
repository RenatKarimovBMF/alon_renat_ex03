"""CrewAI tools for the book pipeline."""

from __future__ import annotations

import json
from pathlib import Path

from crewai.tools import tool

from bookgen.crew.context import PipelineContext
from bookgen.latex.compiler import compile_latex


def build_tools(ctx: PipelineContext) -> dict[str, object]:
    """Create CrewAI tools bound to a session context."""

    @tool("write_session_artifact")
    def write_session_artifact(name: str, payload_json: str) -> str:
        """Persist JSON payload under the current session directory."""
        path = ctx.session_dir / name
        path.write_text(payload_json, encoding="utf-8")
        ctx.artifacts[name] = path
        return str(path)

    @tool("load_course_context")
    def load_course_context() -> str:
        """Return short course context snippets for research tasks."""
        snippets = [
            "LangChain fits linear chains; LangGraph adds stateful orchestration.",
            "CrewAI models role-based agent teams with sequential tasks.",
            "Production agents need planner, memory, tools, and observability layers.",
            "MCP connects agents to tools; A2A connects agents to agents.",
        ]
        return "\n".join(f"- {line}" for line in snippets)

    @tool("estimate_pages")
    def estimate_pages(text: str) -> str:
        """Estimate page count from word count using configured words_per_page."""
        words = len(text.split())
        pages = words / max(ctx.book.words_per_page, 1)
        return json.dumps({"words": words, "estimated_pages": round(pages, 2)})

    @tool("latex_compile")
    def latex_compile() -> str:
        """Compile latex/main.tex into the configured build directory."""
        report = compile_latex(
            ctx.main_tex,
            build_dir=ctx.build_dir,
            max_attempts=int(ctx.book.latex.get("max_compile_attempts", 3)),
        )
        return report.model_dump_json()

    return {
        "write_session_artifact": write_session_artifact,
        "load_course_context": load_course_context,
        "estimate_pages": estimate_pages,
        "latex_compile": latex_compile,
    }
