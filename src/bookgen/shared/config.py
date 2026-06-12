"""Load JSON configuration files with version validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from bookgen.shared.gatekeeper import GatekeeperConfig
from bookgen.shared.version import validate_config_version


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
    services: dict[str, dict[str, int]] = Field(default_factory=dict)
    agents: dict[str, AgentLimitRow]


def load_json(path: Path) -> dict[str, Any]:
    """Read and parse a JSON file."""
    return json.loads(path.read_text(encoding="utf-8"))


def load_setup_config(path: Path) -> SetupConfig:
    """Load setup.json, validate schema, and check the version."""
    config = SetupConfig.model_validate(load_json(path))
    validate_config_version("setup.json", config.version)
    return config


def load_book_config(path: Path) -> BookConfig:
    """Load book.json, validate schema, and check the version."""
    config = BookConfig.model_validate(load_json(path))
    validate_config_version("book.json", config.version)
    return config


def load_rate_limits_config(path: Path) -> GatekeeperConfig:
    """Load rate_limits.json into a GatekeeperConfig (version-checked)."""
    parsed = RateLimitsFile.model_validate(load_json(path))
    validate_config_version("rate_limits.json", parsed.version)
    agent_limits = {
        key: row.max_requests_per_session for key, row in parsed.agents.items()
    }
    total = parsed.max_total_requests
    if total is None:
        total = sum(agent_limits.values())
    # Derive inter-call spacing from requests-per-minute so rate-limited calls
    # WAIT (queue) rather than fail; an explicit min_interval_ms wins if set.
    rpm = parsed.services.get("default", {}).get("requests_per_minute", 0)
    min_interval = parsed.min_interval_ms or (round(60_000 / rpm) if rpm > 0 else 0)
    return GatekeeperConfig(
        enabled=parsed.enabled,
        max_total_requests=total,
        agent_limits=agent_limits,
        min_interval_ms=min_interval,
        log_denials=parsed.log_denials,
    )
