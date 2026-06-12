"""Tests for LLM SDK."""

import httpx
import pytest

from bookgen.sdk.llm_client import LlmClient
from bookgen.sdk.providers import MockProvider, ProviderResponse
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


class _FlakyProvider:
    """Raises HTTP 429 a fixed number of times, then succeeds."""

    def __init__(self, fail_times: int) -> None:
        self._fail_times = fail_times
        self.calls = 0

    def complete(self, system: str, user: str) -> ProviderResponse:
        self.calls += 1
        if self.calls <= self._fail_times:
            request = httpx.Request("POST", "https://example.test")
            response = httpx.Response(429, request=request)
            raise httpx.HTTPStatusError("rate limited", request=request, response=response)
        return ProviderResponse("ok", "mock-model", "mock", 1, 1)


def test_llm_client_retries_transient_then_succeeds() -> None:
    cfg = GatekeeperConfig(
        enabled=True,
        max_total_requests=5,
        agent_limits={"writer": 5},
        retry_after_seconds=0,
        max_retries=3,
    )
    provider = _FlakyProvider(fail_times=2)
    client = LlmClient(ApiGatekeeper(cfg), provider=provider)

    response = client.complete(agent_key="writer", system="s", user="u")

    assert response.text == "ok"
    assert provider.calls == 3  # two 429s + one success


def test_llm_client_reraises_after_max_retries() -> None:
    cfg = GatekeeperConfig(
        enabled=True,
        max_total_requests=5,
        agent_limits={"writer": 5},
        retry_after_seconds=0,
        max_retries=1,
    )
    provider = _FlakyProvider(fail_times=5)
    client = LlmClient(ApiGatekeeper(cfg), provider=provider)

    with pytest.raises(httpx.HTTPStatusError):
        client.complete(agent_key="writer", system="s", user="u")
    assert provider.calls == 2  # initial attempt + one retry
