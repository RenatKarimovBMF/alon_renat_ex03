"""Load JSON configuration files with version validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from bookgen.shared.gatekeeper import GatekeeperConfig


class SetupConfig(BaseModel):
    version: str
    project_name: str
    log_level: str = "INFO"
    session_dir: str = "data/sessions"
    logs_dir: str = "logs"


class BookConfig(BaseModel):
    version: str
    topic: str
    target_pages: int = 15
    page_tolerance: int = 1
    words_per_page: int = 450
    demo_mode: dict[str, Any] = Field(default_factory=dict)
    latex: dict[str, Any] = Field(default_factory=dict)
    crew: dict[str, Any] = Field(default_factory=dict)


class AgentLimitRow(BaseModel):
    max_requests_per_session: int = Field(ge=1)


class RateLimitsFile(BaseModel):
    version: str
    enabled: bool = True
    log_denials: bool = True
    min_interval_ms: int = 0
    max_total_requests: int | None = None
    agents: dict[str, AgentLimitRow]


def load_json(path: Path) -> dict[str, Any]:
    """Read and parse a JSON file."""
    return json.loads(path.read_text(encoding="utf-8"))


def load_setup_config(path: Path) -> SetupConfig:
    """Load setup.json and validate schema."""
    return SetupConfig.model_validate(load_json(path))


def load_book_config(path: Path) -> BookConfig:
    """Load book.json and validate schema."""
    return BookConfig.model_validate(load_json(path))


def load_rate_limits_config(path: Path) -> GatekeeperConfig:
    """Load rate_limits.json into a GatekeeperConfig."""
    parsed = RateLimitsFile.model_validate(load_json(path))
    agent_limits = {
        key: row.max_requests_per_session for key, row in parsed.agents.items()
    }
    total = parsed.max_total_requests
    if total is None:
        total = sum(agent_limits.values())
    return GatekeeperConfig(
        enabled=parsed.enabled,
        max_total_requests=total,
        agent_limits=agent_limits,
        min_interval_ms=parsed.min_interval_ms,
        log_denials=parsed.log_denials,
    )
