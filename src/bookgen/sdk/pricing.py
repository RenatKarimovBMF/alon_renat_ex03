"""Token cost estimation helpers."""

from __future__ import annotations

# USD per 1M tokens (approximate list prices for budgeting).
_MODEL_RATES: dict[str, tuple[float, float]] = {
    "gpt-4o": (2.50, 10.00),
    "gpt-4o-mini": (0.15, 0.60),
    "claude-3-5-sonnet-20241022": (3.00, 15.00),
    "claude-sonnet-4-20250514": (3.00, 15.00),
    "gemini-2.0-flash": (0.10, 0.40),
    "mock-model": (0.0, 0.0),
}


def estimate_usd(model: str, input_tokens: int, output_tokens: int) -> float:
    """Estimate call cost from token counts."""
    in_rate, out_rate = _MODEL_RATES.get(model, (1.0, 3.0))
    return (input_tokens * in_rate + output_tokens * out_rate) / 1_000_000
