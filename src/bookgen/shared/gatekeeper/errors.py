"""Gatekeeper exceptions."""

from __future__ import annotations


class BudgetExceededError(RuntimeError):
    """Raised when an LLM call would exceed configured limits."""
