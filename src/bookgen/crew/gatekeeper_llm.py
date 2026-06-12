"""CrewAI LLM adapter that routes calls through ApiGatekeeper."""

from __future__ import annotations

from typing import Any

from crewai.llms.base_llm import BaseLLM
from crewai.utilities.types import LLMMessage
from pydantic import BaseModel, PrivateAttr
from typing_extensions import override

from bookgen.sdk.llm_client import LlmClient
from bookgen.shared.json_io import extract_json_block

_ROLE_TO_KEY = {
    "chief researcher": "research_director",
    "publishing strategist": "outline_architect",
    "technical author": "chapter_writer",
    "latex copy editor": "latex_editor",
    "build engineer": "build_engineer",
}

class GatekeeperLLM(BaseLLM):
    """Wrap LlmClient so CrewAI tasks honor gatekeeper limits."""

    model: str = "bookgen-gatekeeper"
    provider: str = "bookgen"
    temperature: float = 0.4

    _client: LlmClient = PrivateAttr()
    _default_agent_key: str = PrivateAttr(default="research_director")

    def __init__(
        self,
        client: LlmClient,
        *,
        default_agent_key: str = "research_director",
        **kwargs: Any,
    ) -> None:
        super().__init__(model="bookgen-gatekeeper", temperature=0.4, **kwargs)
        self._client = client
        self._default_agent_key = default_agent_key

    @override
    def call(
        self,
        messages: str | list[LLMMessage],
        tools: list[dict[str, Any]] | None = None,
        callbacks: list[Any] | None = None,
        available_functions: dict[str, Any] | None = None,
        from_task: Any | None = None,
        from_agent: Any | None = None,
        response_model: type[BaseModel] | None = None,
    ) -> str | Any:
        system, user = _split_messages(messages)
        agent_key = _resolve_agent_key(from_agent, self._default_agent_key)
        response = self._client.complete(
            agent_key=agent_key,
            system=system,
            user=user,
            temperature=self.temperature or 0.4,
        )
        text = response.text.strip()
        if response_model is None:
            return text
        return response_model.model_validate_json(extract_json_block(text))

    def supports_function_calling(self) -> bool:
        """CrewAI's converter fallback probes this; we parse JSON from text."""
        return False


def _split_messages(messages: str | list[LLMMessage]) -> tuple[str, str]:
    if isinstance(messages, str):
        return ("You are a helpful assistant.", messages)
    system_parts: list[str] = []
    user_parts: list[str] = []
    for message in messages:
        role = str(message.get("role", "user"))
        content = str(message.get("content", ""))
        if role == "system":
            system_parts.append(content)
        else:
            user_parts.append(content)
    system = "\n".join(system_parts) or "You are a helpful assistant."
    user = "\n".join(user_parts) or system
    return system, user


def _resolve_agent_key(from_agent: Any | None, default: str) -> str:
    if from_agent is None:
        return default
    role = str(getattr(from_agent, "role", "")).lower().strip()
    return _ROLE_TO_KEY.get(role, default)
