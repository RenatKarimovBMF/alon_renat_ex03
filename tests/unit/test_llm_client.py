"""Tests for LLM SDK."""

from bookgen.sdk.llm_client import LlmClient
from bookgen.sdk.providers import MockProvider
from bookgen.shared.gatekeeper import ApiGatekeeper, GatekeeperConfig


def test_llm_client_uses_mock_provider() -> None:
    cfg = GatekeeperConfig(enabled=True, max_total_requests=5, agent_limits={"writer": 5})
    gk = ApiGatekeeper(cfg)
    mock = MockProvider(text="hello book")
    client = LlmClient(gk, provider=mock)

    response = client.complete(agent_key="writer", system="sys", user="user")

    assert response.text == "hello book"
    assert response.provider == "mock"
    assert gk.total_requests == 1
    assert len(mock.calls) == 1
