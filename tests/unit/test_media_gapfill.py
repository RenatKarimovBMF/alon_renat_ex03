"""Tests for LLM-backed media gap-filling (subject-generic fallbacks)."""

from pathlib import Path

from bookgen.crew.live_media import ensure_live_media
from bookgen.crew.media_gapfill import alternate_image_queries, fill_missing_media
from bookgen.models import BookOutline, ChapterPlan, FigureRequest
from bookgen.sdk.llm_client import LlmClient
from bookgen.sdk.providers import MockProvider
from bookgen.shared.gatekeeper import ApiGatekeeper, GatekeeperConfig


def _client(reply: str) -> LlmClient:
    cfg = GatekeeperConfig(
        enabled=True, max_total_requests=10, agent_limits={"outline_architect": 10}
    )
    return LlmClient(ApiGatekeeper(cfg), provider=MockProvider(text=reply))


def _outline() -> BookOutline:
    chapters = [
        ChapterPlan(
            number=n,
            title=f"Chapter {n}",
            page_budget=7.5,
            learning_objectives=["learn"],
            section_titles=["A", "B"],
        )
        for n in (1, 2)
    ]
    return BookOutline(title="T", target_total_pages=15, chapters=chapters)


def test_fill_missing_media_attaches_llm_specs() -> None:
    outline = _outline()
    reply = (
        '{"chapter_number": 2, "table": {"caption": "Key milestones", '
        '"columns": ["Year", "Event"], "rows": [["1957", "Sputnik"], '
        '["1961", "Vostok"], ["1969", "Apollo 11"]]}, '
        '"equation": {"intro": "The rocket equation:", "latex": "v = v_e"}, '
        '"chart": {"title": "Launches per year", "points": '
        '[{"label": "1957", "value": 2}, {"label": "1961", "value": 5}, '
        '{"label": "1969", "value": 9}]}}'
    )
    fill_missing_media(outline, _client(reply), "Any Topic")
    assert outline.chapters[1].table is not None
    assert outline.chapters[1].equation is not None
    assert outline.chapters[1].chart is not None
    assert outline.chapters[0].table is None


def test_fill_missing_media_survives_bad_llm_output() -> None:
    outline = _outline()
    fill_missing_media(outline, _client("sorry, no JSON here"), "Any Topic")
    assert all(c.table is None and c.chart is None for c in outline.chapters)


def test_alternate_image_queries_parses_mapping() -> None:
    queries = alternate_image_queries(
        _client('{"1": "satellite photo", "3": "rocket launch"}'),
        "Any Topic",
        {1: "obscure query", 3: "another"},
    )
    assert queries == {1: "satellite photo", 3: "rocket launch"}


def test_ensure_live_media_retries_with_llm_query(tmp_path: Path) -> None:
    outline = _outline()
    outline.chapters[0].figure = FigureRequest(
        image_query="hopeless first query", caption="A caption sentence."
    )
    attempts: list[str] = []

    def fetch(query: str, target: Path) -> bool:
        attempts.append(query)
        if query == "better query":
            target.write_bytes(b"img")
            return True
        return False

    media = ensure_live_media(
        outline,
        tmp_path,
        fetch_image=fetch,
        llm=_client('{"1": "better query"}'),
        topic="Any Topic",
    )
    assert attempts == ["hopeless first query", "better query"]
    assert media.figures == {1: "ch01_web.jpg"}
