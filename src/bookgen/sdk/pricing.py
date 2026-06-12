"""Token cost estimation helpers."""

from __future__ import annotations

# USD per 1M tokens (base input, output) — published list prices for budgeting.
# Cache pricing is not modeled; the pipeline makes a handful of uncached calls.
_MODEL_RATES: dict[str, tuple[float, float]] = {
    # OpenAI
    "gpt-4o": (2.50, 10.00),
    "gpt-4o-mini": (0.15, 0.60),
    # Anthropic (Claude)
    "claude-fable-5": (10.00, 50.00),
    "claude-mythos-5": (10.00, 50.00),
    "claude-opus-4-8": (5.00, 25.00),
    "claude-opus-4-7": (5.00, 25.00),
    "claude-opus-4-6": (5.00, 25.00),
    "claude-opus-4-5": (5.00, 25.00),
    "claude-opus-4-1": (15.00, 75.00),
    "claude-opus-4": (15.00, 75.00),
    "claude-sonnet-4-6": (3.00, 15.00),
    "claude-sonnet-4-5": (3.00, 15.00),
    "claude-sonnet-4": (3.00, 15.00),
    "claude-3-5-sonnet-20241022": (3.00, 15.00),
    "claude-sonnet-4-20250514": (3.00, 15.00),
    "claude-haiku-4-5": (1.00, 5.00),
    # Google
    "gemini-2.0-flash": (0.10, 0.40),
    "gemini-2.5-flash-lite": (0.10, 0.40),
    "gemini-3.1-flash-lite": (0.10, 0.40),
    # Tests
    "mock-model": (0.0, 0.0),
}


def _rates_for(model: str) -> tuple[float, float]:
    """Exact match first, then longest-prefix match for dated ids
    (e.g. ``claude-opus-4-8-20260115`` matches ``claude-opus-4-8``)."""
    exact = _MODEL_RATES.get(model)
    if exact is not None:
        return exact
    for key in sorted(_MODEL_RATES, key=len, reverse=True):
        if model.startswith(key):
            return _MODEL_RATES[key]
    return (1.0, 3.0)


def estimate_usd(model: str, input_tokens: int, output_tokens: int) -> float:
    """Estimate call cost from token counts."""
    in_rate, out_rate = _rates_for(model)
    return (input_tokens * in_rate + output_tokens * out_rate) / 1_000_000
