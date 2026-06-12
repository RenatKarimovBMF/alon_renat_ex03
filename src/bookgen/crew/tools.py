"""CrewAI tools for the book pipeline."""

from __future__ import annotations

import json

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

    @tool("load_topic_context")
    def load_topic_context() -> str:
        """Return research framing for the configured book topic."""
        topic = ctx.book.topic
        target = ctx.book.target_pages
        lines = [
            f"Book topic: {topic}.",
            f"Target length: about {target} pages of readable, well-structured prose.",
            "Produce findings specific to this topic, each with a credible source tag",
            "(external or team_analysis), and frame open questions the book should answer.",
            "Do not summarize the course tooling; research the topic itself.",
        ]
        return "\n".join(f"- {line}" for line in lines)

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
        "load_topic_context": load_topic_context,
        "estimate_pages": estimate_pages,
        "latex_compile": latex_compile,
    }
