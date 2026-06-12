"""Tests for the CrewAI gatekeeper LLM adapter."""

import pytest

pytest.importorskip("crewai")

from pydantic import BaseModel  # noqa: E402

from bookgen.crew.gatekeeper_llm import (  # noqa: E402
    GatekeeperLLM,
    _resolve_agent_key,
    _split_messages,
)
from bookgen.sdk.llm_client import LlmClient  # noqa: E402
from bookgen.sdk.providers import MockProvider  # noqa: E402
from bookgen.shared.gatekeeper import ApiGatekeeper, GatekeeperConfig  # noqa: E402
from bookgen.shared.json_io import extract_json_block  # noqa: E402


def _client(text: str) -> LlmClient:
    gk = ApiGatekeeper(GatekeeperConfig(enabled=False, max_total_requests=10, agent_limits={}))
    return LlmClient(gk, provider=MockProvider(text=text))


def test_split_messages_from_string() -> None:
    system, user = _split_messages("just a prompt")
    assert system == "You are a helpful assistant."
    assert user == "just a prompt"


def test_split_messages_from_list() -> None:
    system, user = _split_messages(
        [{"role": "system", "content": "S"}, {"role": "user", "content": "U"}]
    )
    assert system == "S"
    assert user == "U"


def test_resolve_agent_key_maps_role() -> None:
    agent = type("A", (), {"role": "Technical Author"})()
    assert _resolve_agent_key(agent, "default") == "chapter_writer"
    assert _resolve_agent_key(None, "default") == "default"


def test_extract_json_variants() -> None:
    assert extract_json_block('{"a": 1}') == '{"a": 1}'
    assert extract_json_block('noise {"a": 1} tail') == '{"a": 1}'
    with pytest.raises(ValueError):
        extract_json_block("no json here")


def test_call_returns_text() -> None:
    llm = GatekeeperLLM(_client("plain answer"))
    assert llm.call("hi") == "plain answer"


def test_call_parses_response_model() -> None:
    class Item(BaseModel):
        value: int

    llm = GatekeeperLLM(_client('{"value": 42}'))
    result = llm.call("hi", response_model=Item)
    assert isinstance(result, Item)
    assert result.value == 42
