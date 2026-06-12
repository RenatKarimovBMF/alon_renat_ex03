"""JSON artifact helpers."""

from __future__ import annotations

import json
import re
from pathlib import Path

_JSON_BLOCK = re.compile(r"\{.*\}", re.DOTALL)


def save_json(path: Path, payload: object) -> None:
    """Write pydantic model or dict as pretty JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if hasattr(payload, "model_dump_json"):
        path.write_text(payload.model_dump_json(indent=2), encoding="utf-8")
    else:
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def extract_json_block(text: str) -> str:
    """Return the JSON object embedded in an LLM reply (fences tolerated)."""
    text = text.strip()
    if text.startswith("{") or text.startswith("["):
        return text
    match = _JSON_BLOCK.search(text)
    if match is None:
        raise ValueError("LLM response did not contain JSON")
    return match.group(0)
