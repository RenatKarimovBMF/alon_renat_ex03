# Mechanism PRD — LLM SDK

**Component:** Provider facade for CrewAI  
**Module:** `bookgen.sdk.llm_client`  
**Version:** 0.10  
**Authors:** Renat Karimov, Alon Engel  
**Last updated:** 2026-06-09

---

## 1. Summary

Single SDK entry for all LLM providers used by CrewAI agents. Mirrors Exercise 02 provider priority pattern.

---

## 2. Provider priority

1. Anthropic API (if `ANTHROPIC_API_KEY`)
2. OpenAI API (if `OPENAI_API_KEY`) — CrewAI default
3. Google Gemini API (if `GOOGLE_API_KEY`)

Selection via `config/setup.json` override or first available key in `.env`.

---

## 3. Public API

```python
class LlmClient:
    def __init__(self, gatekeeper: ApiGatekeeper, config: SetupConfig): ...

    def complete(
        self,
        *,
        agent_key: str,
        system: str,
        user: str,
        temperature: float = 0.4,
    ) -> LlmResponse: ...


class LlmResponse(BaseModel):
    text: str
    model: str
    input_tokens: int
    output_tokens: int
    estimated_usd: float
```

---

## 4. CrewAI integration

CrewAI agents use a custom LLM wrapper or callback that delegates to `LlmClient.complete()` so gatekeeper + cost logging stay centralized.

---

## 5. Cost logging

Each response appends to `logs/crew_run_<session>.jsonl`:

```json
{
  "event": "llm_call",
  "agent_key": "chapter_writer",
  "model": "gpt-4o",
  "input_tokens": 2100,
  "output_tokens": 890,
  "estimated_usd": 0.03
}
```

README must include a rollup cost table after full run (Guidelines §11).

---

## 6. Acceptance criteria

- [ ] Mocked unit tests for each provider branch
- [ ] No API keys in source or config JSON
- [ ] `.env-example` documents required variables
- [ ] `--dry-run` never calls providers

---

## 7. Security

- Load secrets via `os.environ` / `python-dotenv`
- Never log full API keys
- `.gitignore` includes `.env`
