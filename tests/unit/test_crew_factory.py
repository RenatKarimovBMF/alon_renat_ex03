"""Tests for CrewAI crew construction."""

import sys

import pytest

pytest.importorskip("crewai")
pytestmark = pytest.mark.skipif(
    sys.version_info >= (3, 14),
    reason="CrewAI/chromadb is not compatible with Python 3.14+",
)

from pathlib import Path

from bookgen.crew.context import PipelineContext
from bookgen.crew.factory import build_crew
from bookgen.sdk.llm_client import LlmClient
from bookgen.sdk.providers import MockProvider
from bookgen.shared.config import load_book_config, load_setup_config
from bookgen.shared.gatekeeper import ApiGatekeeper, GatekeeperConfig

ROOT = Path(__file__).resolve().parents[2]


def test_build_crew_has_three_llm_tasks() -> None:
    setup = load_setup_config(ROOT / "config" / "setup.json")
    book = load_book_config(ROOT / "config" / "book.json")
    ctx = PipelineContext.create(
        session_id="testcrew",
        setup=setup,
        book=book,
        project_root=ROOT,
    )
    gk = ApiGatekeeper(
        GatekeeperConfig(enabled=False, max_total_requests=10, agent_limits={"a": 10})
    )
    llm = LlmClient(gk, provider=MockProvider())
    crew = build_crew(ctx, llm, llm_tasks_only=True)
    assert len(crew.tasks) == 3
    assert len(crew.agents) == 3
