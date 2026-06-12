"""LLM-backed gap-filling for live media (keeps the pipeline subject-generic).

If the outline agent omitted the table/equation/chart, or a web image fetch
failed, the *same LLM API* (via the gatekeeper) generates the missing spec or
an alternative image query — instead of falling back to subject-specific
curated content. The configured image pool stays as the bare-minimum last
resort, and a chapter may simply end up without an image.
"""

from __future__ import annotations

import json
import logging

from pydantic import BaseModel

from bookgen.models import BookOutline, ChartSpec, EquationSpec, TableSpec
from bookgen.sdk.llm_client import LlmClient
from bookgen.shared.json_io import extract_json_block

logger = logging.getLogger("bookgen.crew.media_gapfill")

_AGENT_KEY = "outline_architect"
_SYSTEM = "You output ONLY one valid JSON object, no prose and no markdown fences."

_KIND_SCHEMAS: dict[str, tuple[type[BaseModel], str]] = {
    "table": (
        TableSpec,
        '{"chapter_number": <int>, "table": {"caption": str, '
        '"columns": [2-5 strings], "rows": [3-8 rows of matching cells]}}',
    ),
    "equation": (
        EquationSpec,
        '{"chapter_number": <int>, "equation": {"intro": str, '
        '"latex": "display math body, no $", "explanation": str}}',
    ),
    "chart": (
        ChartSpec,
        '{"chapter_number": <int>, "chart": {"title": str, "y_label": str, '
        '"points": [3-10 {"label": str, "value": number}]}}',
    ),
}


def fill_missing_media(outline: BookOutline, llm: LlmClient, topic: str) -> None:
    """Generate any missing table/equation/chart spec with one LLM call each."""
    for kind in ("table", "equation", "chart"):
        if any(getattr(chapter, kind) is not None for chapter in outline.chapters):
            continue
        _fill_one(outline, llm, topic, kind)


def _fill_one(outline: BookOutline, llm: LlmClient, topic: str, kind: str) -> None:
    model_type, schema = _KIND_SCHEMAS[kind]
    chapters = "; ".join(f"{c.number}: {c.title}" for c in outline.chapters)
    user = (
        f"Book topic: {topic}. Chapters: {chapters}. The outline is missing "
        f"its {kind}. Pick the best-fitting chapter and return real, factual "
        f"content about the topic as JSON: {schema}"
    )
    try:
        response = llm.complete(agent_key=_AGENT_KEY, system=_SYSTEM, user=user)
        payload = json.loads(extract_json_block(response.text))
        spec = model_type.model_validate(payload[kind])
        number = int(payload.get("chapter_number", outline.chapters[0].number))
    except Exception as error:  # noqa: BLE001 - degrade, never break the run
        logger.warning(
            "media gap-fill failed",
            extra={"extra_data": {"kind": kind, "error": str(error)}},
        )
        return
    target = next(
        (c for c in outline.chapters if c.number == number), outline.chapters[0]
    )
    setattr(target, kind, spec)


def alternate_image_queries(
    llm: LlmClient,
    topic: str,
    failed: dict[int, str],
) -> dict[int, str]:
    """Ask the LLM for one simpler, alternative image query per failed chapter."""
    if not failed:
        return {}
    listing = "; ".join(f"{num}: {query}" for num, query in failed.items())
    user = (
        f"Book topic: {topic}. These public-web image searches returned no "
        f"usable result: {listing}. For each chapter number, return ONE "
        "simpler, more generic query likely to match stock/archive photos. "
        'JSON: {"<chapter_number>": "<query>", ...}'
    )
    try:
        response = llm.complete(agent_key=_AGENT_KEY, system=_SYSTEM, user=user)
        payload = json.loads(extract_json_block(response.text))
        return {int(num): str(query) for num, query in payload.items()}
    except Exception as error:  # noqa: BLE001 - degrade, never break the run
        logger.warning(
            "alternate image queries failed",
            extra={"extra_data": {"error": str(error)}},
        )
        return {}
