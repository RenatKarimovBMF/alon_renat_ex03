"""Unified LLM client with gatekeeper integration."""

from __future__ import annotations

import json
import logging
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from bookgen.sdk.http_providers import AnthropicProvider, GeminiProvider, OpenAiProvider, env_key
from bookgen.sdk.pricing import estimate_usd
from bookgen.sdk.providers import LlmProvider, MockProvider
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
        raw = provider.complete(system, user)
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
