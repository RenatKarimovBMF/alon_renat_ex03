"""Load agent prompt YAML files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class AgentPrompt:
    role: str
    goal: str
    backstory: str
    instructions: str


def load_agent_prompt(path: Path) -> AgentPrompt:
    """Load one agent prompt YAML file."""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return AgentPrompt(
        role=str(data["role"]),
        goal=str(data["goal"]).strip(),
        backstory=str(data["backstory"]).strip(),
        instructions=str(data["instructions"]).strip(),
    )


def load_prompts(prompts_dir: Path) -> dict[str, AgentPrompt]:
    """Load all known agent prompts keyed by file stem."""
    keys = (
        "research_director",
        "outline_architect",
        "chapter_writer",
        "latex_editor",
        "build_engineer",
    )
    return {key: load_agent_prompt(prompts_dir / f"{key}.yaml") for key in keys}
