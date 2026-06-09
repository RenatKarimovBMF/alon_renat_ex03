# Mechanism PRD — Gatekeeper

**Component:** API call budget manager  
**Module:** `bookgen.shared.gatekeeper`  
**Version:** 0.10  
**Authors:** Renat Karimov, Alon Engel  
**Last updated:** 2026-06-09

---

## 1. Summary

Protect the project from runaway LLM usage during CrewAI development. Every provider call passes through the gatekeeper **before** execution and is **recorded** after success.

Adapted from Exercise 02 (`debate.gatekeeper`) with per-agent session limits from `config/rate_limits.json`.

---

## 2. Config (`config/rate_limits.json`)

```json
{
  "version": "1.00",
  "enabled": true,
  "services": { "default": { "requests_per_minute": 30, ... } },
  "agents": {
    "research_director": { "max_requests_per_session": 5 },
    "chapter_writer": { "max_requests_per_session": 20 }
  }
}
```

---

## 3. Public API

```python
class BudgetExceededError(RuntimeError): ...

class ApiGatekeeper:
    def check(self, agent_key: str) -> None: ...
    def record(self, agent_key: str) -> None: ...
    def get_queue_status(self) -> QueueStatus: ...
```

**Invariant:** one `check` + one `record` per successful LLM call.

---

## 4. Integration point

`bookgen.sdk.llm_client` wraps all CrewAI LLM calls:

```python
gatekeeper.check(agent_key)
response = provider.complete(...)
gatekeeper.record(agent_key)
```

---

## 5. Acceptance criteria

- [ ] Unit tests: under limit passes, over limit raises `BudgetExceededError`
- [ ] Disabled gatekeeper (`enabled: false`) allows unlimited calls (dev only)
- [ ] Token/cost metrics logged separately in `logs/crew_run_*.jsonl`

---

## 6. Out of scope (v1)

- Token-dollar budgets (requests only)
- Cross-session persistence
- Distributed rate limiting
