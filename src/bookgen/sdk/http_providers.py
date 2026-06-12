"""HTTP-backed LLM providers."""

from __future__ import annotations

import os

import httpx

from bookgen.sdk.providers import ProviderResponse

_PLACEHOLDERS = ("your-key", "example", "changeme", "paste", "xxx")


def env_key(name: str) -> str | None:
    value = (os.environ.get(name) or "").strip()
    if not value:
        return None
    lower = value.lower()
    if any(marker in lower for marker in _PLACEHOLDERS):
        return None
    return value


class OpenAiProvider:
    def __init__(self, timeout: int) -> None:
        self._timeout = timeout
        self._model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    def complete(self, system: str, user: str) -> ProviderResponse:
        key = env_key("OPENAI_API_KEY")
        if key is None:
            raise RuntimeError("OPENAI_API_KEY is missing")
        payload = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        with httpx.Client(timeout=self._timeout) as client:
            resp = client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}"},
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()
        text = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})
        return ProviderResponse(
            text=text,
            model=self._model,
            provider="openai",
            input_tokens=int(usage.get("prompt_tokens", 0)),
            output_tokens=int(usage.get("completion_tokens", 0)),
        )


class AnthropicProvider:
    def __init__(self, timeout: int) -> None:
        self._timeout = timeout
        self._model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
        # Ceiling on OUTPUT tokens per response (billed only for what is
        # generated). Book-length JSON needs far more than the old 4096 cap,
        # which silently truncated and broke JSON parsing; keep it generous.
        self._max_tokens = int(os.environ.get("ANTHROPIC_MAX_TOKENS", "32000"))

    def complete(self, system: str, user: str) -> ProviderResponse:
        key = env_key("ANTHROPIC_API_KEY")
        if key is None:
            raise RuntimeError("ANTHROPIC_API_KEY is missing")
        payload = {
            "model": self._model,
            "max_tokens": self._max_tokens,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        }
        with httpx.Client(timeout=self._timeout) as client:
            resp = client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()
        text = "".join(block.get("text", "") for block in data.get("content", []))
        usage = data.get("usage", {})
        return ProviderResponse(
            text=text,
            model=self._model,
            provider="anthropic",
            input_tokens=int(usage.get("input_tokens", 0)),
            output_tokens=int(usage.get("output_tokens", 0)),
        )


class GeminiProvider:
    def __init__(self, timeout: int) -> None:
        self._timeout = timeout
        self._model = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")

    def complete(self, system: str, user: str) -> ProviderResponse:
        key = env_key("GOOGLE_API_KEY") or env_key("GEMINI_API_KEY")
        if key is None:
            raise RuntimeError("GOOGLE_API_KEY or GEMINI_API_KEY is missing")
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self._model}:generateContent?key={key}"
        )
        payload = {"contents": [{"parts": [{"text": f"{system}\n\n{user}"}]}]}
        with httpx.Client(timeout=self._timeout) as client:
            resp = client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        meta = data.get("usageMetadata", {})
        return ProviderResponse(
            text=text,
            model=self._model,
            provider="gemini",
            input_tokens=int(meta.get("promptTokenCount", 0)),
            output_tokens=int(meta.get("candidatesTokenCount", 0)),
        )
