"""Tests for gatekeeper limits."""

import pytest

from bookgen.shared.config import load_rate_limits_config
from bookgen.shared.gatekeeper import ApiGatekeeper, BudgetExceededError, GatekeeperConfig

ROOT = __import__("pathlib").Path(__file__).resolve().parents[2]


def test_gatekeeper_allows_under_limit() -> None:
    cfg = GatekeeperConfig(enabled=True, max_total_requests=2, agent_limits={"a": 2})
    gk = ApiGatekeeper(cfg)
    gk.check("a")
    gk.record("a")
    assert gk.total_requests == 1


def test_gatekeeper_blocks_agent_limit() -> None:
    cfg = GatekeeperConfig(enabled=True, max_total_requests=5, agent_limits={"a": 1})
    gk = ApiGatekeeper(cfg)
    gk.check("a")
    gk.record("a")
    with pytest.raises(BudgetExceededError):
        gk.check("a")


def test_load_rate_limits_from_file() -> None:
    cfg = load_rate_limits_config(ROOT / "config" / "rate_limits.json")
    assert cfg.enabled is True
    assert cfg.max_total_requests == 50
    assert cfg.agent_limits["chapter_writer"] == 20
