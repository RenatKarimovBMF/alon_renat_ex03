"""Tests for HTTP LLM providers using httpx MockTransport (no network)."""

import httpx
import pytest

from bookgen.sdk.http_providers import (
    AnthropicProvider,
    GeminiProvider,
    OpenAiProvider,
    env_key,
)


def _patch_client(monkeypatch, handler) -> None:
    real_client = httpx.Client  # capture before patching to avoid recursion

    def fake_client(*_args, **_kwargs):
        return real_client(transport=httpx.MockTransport(handler))

    monkeypatch.setattr(httpx, "Client", fake_client)


def test_env_key_filters_blank_and_placeholders(monkeypatch) -> None:
    monkeypatch.delenv("SOME_KEY", raising=False)
    assert env_key("SOME_KEY") is None
    monkeypatch.setenv("SOME_KEY", "   ")
    assert env_key("SOME_KEY") is None
    monkeypatch.setenv("SOME_KEY", "your-key-here")
    assert env_key("SOME_KEY") is None
    monkeypatch.setenv("SOME_KEY", "sk-real-value")
    assert env_key("SOME_KEY") == "sk-real-value"


def test_openai_provider_parses_response(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "sk-real")

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "choices": [{"message": {"content": "Hello"}}],
                "usage": {"prompt_tokens": 11, "completion_tokens": 4},
            },
        )

    _patch_client(monkeypatch, handler)
    result = OpenAiProvider(timeout=5).complete("sys", "user")
    assert result.text == "Hello"
    assert result.provider == "openai"
    assert result.input_tokens == 11
    assert result.output_tokens == 4


def test_anthropic_provider_parses_response(monkeypatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-real")

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "content": [{"text": "Hi "}, {"text": "there"}],
                "usage": {"input_tokens": 7, "output_tokens": 2},
            },
        )

    _patch_client(monkeypatch, handler)
    result = AnthropicProvider(timeout=5).complete("sys", "user")
    assert result.text == "Hi there"
    assert result.provider == "anthropic"
    assert result.input_tokens == 7


def test_gemini_provider_parses_response(monkeypatch) -> None:
    monkeypatch.setenv("GOOGLE_API_KEY", "g-real")

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "candidates": [{"content": {"parts": [{"text": "Salut"}]}}],
                "usageMetadata": {"promptTokenCount": 9, "candidatesTokenCount": 5},
            },
        )

    _patch_client(monkeypatch, handler)
    result = GeminiProvider(timeout=5).complete("sys", "user")
    assert result.text == "Salut"
    assert result.provider == "gemini"
    assert result.output_tokens == 5


def test_openai_provider_requires_key(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(RuntimeError):
        OpenAiProvider(timeout=5).complete("sys", "user")
