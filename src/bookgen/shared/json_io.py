"""JSON artifact helpers."""

from __future__ import annotations

import json
from pathlib import Path


def save_json(path: Path, payload: object) -> None:
    """Write pydantic model or dict as pretty JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if hasattr(payload, "model_dump_json"):
        path.write_text(payload.model_dump_json(indent=2), encoding="utf-8")
    else:
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
