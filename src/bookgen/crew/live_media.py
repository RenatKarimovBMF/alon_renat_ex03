"""Agent-driven media for live runs: fetch web images, render the agent chart.

The outline decides content and placement (which chapter carries the table,
equation, chart, and each image's search query). Python fetches and renders.
Per element, the configured plan acts as a safety net so the compiled book
always satisfies the exercise requirements even if a web fetch fails.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from bookgen.crew.extras import ExtrasPlan, build_chapter_extras
from bookgen.latex.blocks import ChapterExtras
from bookgen.latex.chart import render_chart
from bookgen.latex.image_search import fetch_web_image
from bookgen.models import BookOutline, ChapterPlan

logger = logging.getLogger("bookgen.crew.live_media")

FetchImageFn = Callable[[str, Path], bool]


@dataclass
class LiveMedia:
    """Files produced for agent-specified media, keyed by chapter number."""

    figures: dict[int, str] = field(default_factory=dict)
    charts: dict[int, str] = field(default_factory=dict)


def ensure_live_media(
    outline: BookOutline,
    figures_dir: Path,
    *,
    fetch_image: FetchImageFn | None = None,
    chart_renderer: Callable[..., Path] = render_chart,
) -> LiveMedia:
    """Fetch every agent-requested web image and render the agent chart."""
    fetch_image = fetch_image or fetch_web_image
    figures_dir.mkdir(parents=True, exist_ok=True)
    media = LiveMedia()
    for chapter in outline.chapters:
        if chapter.figure is not None:
            filename = f"ch{chapter.number:02d}_web.jpg"
            if fetch_image(chapter.figure.image_query, figures_dir / filename):
                media.figures[chapter.number] = filename
            else:
                logger.warning(
                    "web image fetch failed; using fallback figure",
                    extra={"extra_data": {"chapter": chapter.number}},
                )
        if chapter.chart is not None:
            filename = f"agent_chart_ch{chapter.number:02d}.pdf"
            chart_renderer(chapter.chart, figures_dir, filename=filename)
            media.charts[chapter.number] = filename
    return media


def compose_live_extras(
    plan: ExtrasPlan,
    chapter: ChapterPlan,
    media: LiveMedia,
    *,
    fallback_table: bool,
    fallback_equation: bool,
    fallback_chart: bool,
) -> ChapterExtras | None:
    """Build extras from the outline's media, falling back per missing element."""
    base = build_chapter_extras(plan, chapter.number, hebrew_override=chapter.hebrew_summary)
    web_figure = media.figures.get(chapter.number)
    figure_file = web_figure or (base.figure_file if base else None)
    figure_caption = (
        chapter.figure.caption
        if (web_figure and chapter.figure)
        else (base.figure_caption if base else None)
    )
    chart_file = media.charts.get(chapter.number)
    return ChapterExtras(
        figure_file=figure_file,
        figure_caption=figure_caption,
        hebrew_summary=base.hebrew_summary if base else chapter.hebrew_summary,
        include_milestones_table=fallback_table and bool(base and base.include_milestones_table),
        include_rocket_equation=fallback_equation and bool(base and base.include_rocket_equation),
        include_timeline_plot=fallback_chart and bool(base and base.include_timeline_plot),
        table_spec=chapter.table,
        equation_spec=chapter.equation,
        chart_file=chart_file,
        chart_caption=chapter.chart.title if (chart_file and chapter.chart) else None,
    )
