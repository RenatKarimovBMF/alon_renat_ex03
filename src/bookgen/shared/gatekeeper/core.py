"""API call budget enforcement."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass

from bookgen.shared.gatekeeper.denial_log import log_denial
from bookgen.shared.gatekeeper.errors import BudgetExceededError


@dataclass
class GatekeeperConfig:
    """Runtime limits loaded from config/rate_limits.json."""

    enabled: bool
    max_total_requests: int
    agent_limits: dict[str, int]
    min_interval_ms: int = 0
    log_denials: bool = True
    retry_after_seconds: int = 0
    max_retries: int = 0
    timeout_seconds: int = 120


@dataclass
class QueueStatus:
    """Snapshot of gatekeeper counters."""

    total_requests: int
    per_agent: dict[str, int]
    denial_count: int


class ApiGatekeeper:
    """Central gate for LLM/API calls.

    Policy (see ADR-005): a per-minute rate limit is honored by *waiting*
    (calls are spaced via ``min_interval_ms``, i.e. queued, never dropped),
    while the per-agent and global request budgets are a hard *cost guard*
    that rejects calls once a run would exceed its allowance.
    """

    def __init__(self, config: GatekeeperConfig) -> None:
        self._config = config
        self._lock = threading.Lock()
        self._total = 0
        self._per_agent: dict[str, int] = {}
        self._last_request_at: float | None = None
        self._denial_count = 0

    @property
    def total_requests(self) -> int:
        return self._total

    @property
    def denial_count(self) -> int:
        return self._denial_count

    @property
    def max_retries(self) -> int:
        return self._config.max_retries

    @property
    def retry_after_seconds(self) -> int:
        return self._config.retry_after_seconds

    @property
    def timeout_seconds(self) -> int:
        return self._config.timeout_seconds

    def check(self, agent_key: str) -> None:
        """Admit one call: wait for the rate window, reject only if over budget.

        Raises ``BudgetExceededError`` when the per-agent or global budget is
        exhausted (cost guard); otherwise blocks until the configured minimum
        interval has elapsed so callers are queued, not dropped.
        """
        with self._lock:
            reason = self._denial_reason(agent_key)
            if reason is not None:
                self._denial_count += 1
                if self._config.log_denials:
                    log_denial(
                        agent_key=agent_key,
                        reason=reason,
                        total_requests=self._total,
                        per_agent=dict(self._per_agent),
                    )
                raise BudgetExceededError(reason)
            self._enforce_min_interval_unlocked()

    def record(self, agent_key: str) -> None:
        """Increment counters after a successful LLM call."""
        if not self._config.enabled:
            return
        with self._lock:
            self._total += 1
            self._per_agent[agent_key] = self._per_agent.get(agent_key, 0) + 1
            self._last_request_at = time.monotonic()

    def requests_for(self, agent_key: str) -> int:
        return self._per_agent.get(agent_key, 0)

    def get_queue_status(self) -> QueueStatus:
        return QueueStatus(
            total_requests=self._total,
            per_agent=dict(self._per_agent),
            denial_count=self._denial_count,
        )

    def _denial_reason(self, agent_key: str) -> str | None:
        if not self._config.enabled:
            return None
        if self._total >= self._config.max_total_requests:
            return "Global request budget exceeded"
        limit = self._config.agent_limits.get(agent_key)
        if limit is None:
            return f"Unknown agent key: {agent_key}"
        if self._per_agent.get(agent_key, 0) >= limit:
            return f"Budget exceeded for {agent_key}"
        return None

    def _enforce_min_interval_unlocked(self) -> None:
        interval_ms = self._config.min_interval_ms
        if interval_ms <= 0 or self._last_request_at is None:
            return
        elapsed_ms = (time.monotonic() - self._last_request_at) * 1000
        wait_ms = interval_ms - elapsed_ms
        if wait_ms > 0:
            time.sleep(wait_ms / 1000)
