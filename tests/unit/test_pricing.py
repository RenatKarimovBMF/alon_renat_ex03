"""Tests for token pricing helpers."""

import pytest

from bookgen.sdk.pricing import estimate_usd


def test_estimate_usd_mock_model_is_free() -> None:
    assert estimate_usd("mock-model", 1000, 1000) == 0.0


def test_estimate_usd_openai_mini() -> None:
    cost = estimate_usd("gpt-4o-mini", 1_000_000, 1_000_000)
    assert cost == pytest.approx(0.75)
