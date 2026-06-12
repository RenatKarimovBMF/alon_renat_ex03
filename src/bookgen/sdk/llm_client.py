"""Unified LLM client with gatekeeper integration."""

from __future__ import annotations

import json
import logging
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import httpx

from bookgen.sdk.http_providers import AnthropicProvider, GeminiProvider, OpenAiProvider, env_key
from bookgen.sdk.pricing import estimate_usd
from bookgen.sdk.providers import LlmProvider, MockProvider, ProviderResponse
from bookgen.shared.gatekeeper import ApiGatekeeper

logger = logging.getLogger("bookgen.sdk.llm")


@dataclass(frozen=True)
class LlmResponse:
    text: str
    model: str
    provider: str
    input_tokens: int
    output_tokens: int
    estimated_usd: float


class LlmClient:
    """Route LLM calls through gatekeeper and log usage."""

    def __init__(
        self,
        gatekeeper: ApiGatekeeper,
        *,
        provider: LlmProvider | None = None,
        log_fn: Callable[[dict[str, object]], None] | None = None,
        timeout_seconds: int = 120,
    ) -> None:
        self._gatekeeper = gatekeeper
        self._provider = provider
        self._log_fn = log_fn
        self._timeout = timeout_seconds

    def complete(
        self,
        *,
        agent_key: str,
        system: str,
        user: str,
        temperature: float = 0.4,
    ) -> LlmResponse:
        """Execute one LLM call for an agent."""
        self._gatekeeper.check(agent_key)
        provider = self._provider or self._build_runtime_provider()
        raw = self._complete_with_retry(provider, system, user)
        self._gatekeeper.record(agent_key)
        estimated = estimate_usd(raw.model, raw.input_tokens, raw.output_tokens)
        response = LlmResponse(
            text=raw.text,
            model=raw.model,
            provider=raw.provider,
            input_tokens=raw.input_tokens,
            output_tokens=raw.output_tokens,
            estimated_usd=estimated,
        )
        self._emit_log(agent_key, response, temperature)
        return response

    def _complete_with_retry(
        self, provider: LlmProvider, system: str, user: str
    ) -> ProviderResponse:
        """Call the provider, retrying transient 429/5xx errors per config.

        Wires up ``retry_after_seconds`` and ``max_retries`` from
        ``rate_limits.json`` (Guidelines: gatekeeper retries on transient
        failures); permanent errors (4xx other than 429) are not retried.
        """
        attempts = max(0, self._gatekeeper.max_retries) + 1
        delay = self._gatekeeper.retry_after_seconds
        for attempt in range(attempts):
            try:
                return provider.complete(system, user)
            except httpx.HTTPStatusError as exc:
                status = exc.response.status_code
                transient = status == 429 or status >= 500
                if not transient or attempt == attempts - 1:
                    raise
                logger.warning(
                    "llm_retry",
                    extra={"extra_data": {"status": status, "attempt": attempt + 1}},
                )
                if delay > 0:
                    time.sleep(delay)
        raise RuntimeError("unreachable retry state")  # pragma: no cover

    def _build_runtime_provider(self) -> LlmProvider:
        if env_key("ANTHROPIC_API_KEY"):
            return AnthropicProvider(timeout=self._timeout)
        if env_key("OPENAI_API_KEY"):
            return OpenAiProvider(timeout=self._timeout)
        if env_key("GOOGLE_API_KEY") or env_key("GEMINI_API_KEY"):
            return GeminiProvider(timeout=self._timeout)
        return MockProvider(
            text=(
                "No API key configured. Set OPENAI_API_KEY, ANTHROPIC_API_KEY, "
                "or GOOGLE_API_KEY in .env for live runs."
            )
        )

    def _emit_log(self, agent_key: str, response: LlmResponse, temperature: float) -> None:
        payload = {
            "event": "llm_call",
            "agent_key": agent_key,
            "model": response.model,
            "provider": response.provider,
            "input_tokens": response.input_tokens,
            "output_tokens": response.output_tokens,
            "estimated_usd": response.estimated_usd,
            "temperature": temperature,
        }
        logger.info("llm_call", extra={"extra_data": payload})
        if self._log_fn is not None:
            self._log_fn(payload)


def append_jsonl(path: Path, payload: dict[str, object]) -> None:
    """Append one JSON object as a line (for crew cost logs)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
