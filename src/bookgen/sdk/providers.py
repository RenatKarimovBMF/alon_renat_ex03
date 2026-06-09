"""Provider protocol and mock implementation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ProviderResponse:
    text: str
    model: str
    provider: str
    input_tokens: int
    output_tokens: int


class LlmProvider(Protocol):
    """Minimal provider interface for tests and runtime."""

    def complete(self, system: str, user: str) -> ProviderResponse: ...


class MockProvider:
    """Deterministic provider for unit tests."""

    def __init__(self, text: str = "mock response") -> None:
        self._text = text
        self.calls: list[tuple[str, str]] = []

    def complete(self, system: str, user: str) -> ProviderResponse:
        self.calls.append((system, user))
        joined = f"{system}\n{user}"
        return ProviderResponse(
            text=self._text,
            model="mock-model",
            provider="mock",
            input_tokens=max(1, len(joined) // 4),
            output_tokens=max(1, len(self._text) // 4),
        )
