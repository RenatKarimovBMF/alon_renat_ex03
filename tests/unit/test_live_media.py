"""Tests for agent-driven media: specs, renderers, web fetch, composition."""

from pathlib import Path

import httpx
import pytest

from bookgen.crew.extras import moon_extras_plan
from bookgen.crew.live_media import LiveMedia, compose_live_extras, ensure_live_media
from bookgen.latex.image_search import fetch_web_image
from bookgen.latex.media_render import render_equation_spec, render_table_spec
from bookgen.models import (
    BookOutline,
    ChapterPlan,
    ChartSpec,
    EquationSpec,
    FigureRequest,
    TableSpec,
)


def _chapter(number: int, **kwargs) -> ChapterPlan:
    return ChapterPlan(
        number=number,
        title=f"Chapter {number}",
        page_budget=7.5,
        learning_objectives=["learn"],
        section_titles=["A", "B"],
        **kwargs,
    )


def test_equation_spec_rejects_dangerous_tex() -> None:
    with pytest.raises(ValueError):
        EquationSpec(intro="An equation follows.", latex=r"\input{evil} + 1")


def test_table_spec_rejects_ragged_rows() -> None:
    with pytest.raises(ValueError):
        TableSpec(caption="Bad table rows", columns=["A", "B"], rows=[["1"], ["2", "3"], ["4"]])


def test_render_table_and_equation_specs() -> None:
    table = TableSpec(
        caption="Launches by year",
        columns=["Year", "Launches"],
        rows=[["1957", "2"], ["1961", "5"], ["1969", "9"]],
    )
    rendered = render_table_spec(table)
    assert "\\toprule" in rendered and "1969 & 9" in rendered
    equation = EquationSpec(intro="Orbital velocity:", latex=r"v = \sqrt{GM/r}")
    assert "\\begin{equation}" in render_equation_spec(equation)


def test_fetch_web_image_via_mock_transport(tmp_path: Path) -> None:
    image_bytes = b"\xff\xd8" + b"x" * 40_000  # jpeg magic + bulk

    def handler(request: httpx.Request) -> httpx.Response:
        if "commons.wikimedia.org" in request.url.host:
            payload = {"query": {"pages": {"1": {"imageinfo": [
                {"url": "https://upload.test/img.jpg", "width": 1024, "mime": "image/jpeg"}
            ]}}}}
            return httpx.Response(200, json=payload)
        return httpx.Response(200, content=image_bytes)

    client = httpx.Client(transport=httpx.MockTransport(handler))
    target = tmp_path / "img.jpg"
    assert fetch_web_image("apollo 11", target, client=client)
    assert target.stat().st_size > 30_000


def test_ensure_live_media_renders_chart_and_skips_failed_fetch(tmp_path: Path) -> None:
    outline = BookOutline(
        title="T",
        target_total_pages=15,
        chapters=[
            _chapter(1, figure=FigureRequest(image_query="apollo 11", caption="A caption one.")),
            _chapter(
                2,
                chart=ChartSpec(
                    title="Launches",
                    points=[{"label": "1957", "value": 2}, {"label": "1961", "value": 5},
                            {"label": "1969", "value": 9}],
                ),
            ),
        ],
    )
    media = ensure_live_media(
        outline, tmp_path, fetch_image=lambda q, t: False,
        chart_renderer=lambda spec, d, filename: (d / filename).write_bytes(b"pdf") or d / filename,
    )
    assert media.figures == {}
    assert media.charts == {2: "agent_chart_ch02.pdf"}


def test_compose_live_extras_blocks_offtopic_pool() -> None:
    # A Moon photo must never leak into a different-subject book.
    plan = moon_extras_plan()
    chapter = _chapter(3, hebrew_summary="סיכום.")
    extras = compose_live_extras(
        plan, chapter, LiveMedia(),
        fallback_table=True, fallback_equation=True, fallback_chart=True,
        plan_is_topical=False,
    )
    assert extras.figure_file is None and extras.figure_caption is None
    assert not extras.include_milestones_table
    assert not extras.include_rocket_equation
    assert not extras.include_timeline_plot
    assert extras.hebrew_summary == "סיכום."  # outline Hebrew still used


def test_compose_live_extras_prefers_agent_media_with_fallbacks() -> None:
    plan = moon_extras_plan()
    chapter = _chapter(
        1,
        hebrew_summary="סיכום בעברית.",
        figure=FigureRequest(image_query="sputnik launch", caption="Web caption."),
        table=TableSpec(caption="Data table", columns=["A", "B"],
                        rows=[["1", "2"], ["3", "4"], ["5", "6"]]),
    )
    media = LiveMedia(figures={1: "ch01_web.jpg"})
    extras = compose_live_extras(
        plan, chapter, media,
        fallback_table=False, fallback_equation=True, fallback_chart=True,
    )
    assert extras.figure_file == "ch01_web.jpg" and extras.figure_caption == "Web caption."
    assert extras.table_spec is chapter.table
    assert not extras.include_milestones_table  # agent table exists somewhere
    assert extras.hebrew_summary == "סיכום בעברית."
