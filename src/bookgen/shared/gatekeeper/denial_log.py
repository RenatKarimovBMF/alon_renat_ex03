"""Structured logging for gatekeeper denials."""

from __future__ import annotations

import logging

logger = logging.getLogger("bookgen.gatekeeper")


def log_denial(
    *,
    agent_key: str,
    reason: str,
    total_requests: int,
    per_agent: dict[str, int],
) -> None:
    """Emit a warning when a request is blocked."""
    logger.warning(
        "gatekeeper_denied",
        extra={
            "extra_data": {
                "event": "gatekeeper_denied",
                "agent_key": agent_key,
                "reason": reason,
                "total_requests": total_requests,
                "per_agent": per_agent,
            }
        },
    )
