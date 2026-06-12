"""Config-driven per-chapter extras (figure, Hebrew summary, table, equation, plot).

The book's required LaTeX elements are attached per chapter. The plan comes
from the optional ``extras`` block in ``config/book.json`` so a different
subject can supply its own figures and Hebrew summaries; when the block is
absent the built-in Moon Race plan is used, preserving existing behavior.
"""

from __future__ import annotations

from dataclasses import dataclass

from bookgen.latex.blocks import ChapterExtras
from bookgen.shared.config import BookConfig


@dataclass(frozen=True)
class FigureSpec:
    """One chapter figure: bundled/remote image plus its caption."""

    file: str
    urls: list[str]
    caption: str


@dataclass(frozen=True)
class ExtrasPlan:
    """Which extra blocks each chapter receives."""

    figures: list[FigureSpec]
    hebrew_summaries: list[str]
    table_chapter: int | None
    equation_chapter: int | None
    plot_chapter: int | None

    def figure_tuples(self) -> list[tuple[str, list[str], str]]:
        """Shape expected by ``latex.figures.ensure_figures``."""
        return [(f.file, list(f.urls), f.caption) for f in self.figures]


def moon_extras_plan() -> ExtrasPlan:
    """Built-in plan for the default Moon Race subject."""
    from bookgen.crew.moon_figures import CHAPTER_FIGURES, HEBREW_SUMMARIES

    return ExtrasPlan(
        figures=[FigureSpec(file, list(urls), caption) for file, urls, caption in CHAPTER_FIGURES],
        hebrew_summaries=list(HEBREW_SUMMARIES),
        table_chapter=1,
        equation_chapter=3,
        plot_chapter=4,
    )


def load_extras_plan(book: BookConfig) -> ExtrasPlan:
    """Read the ``extras`` block from book.json, falling back to Moon defaults."""
    cfg = book.extras
    base = moon_extras_plan()
    if not cfg:
        return base
    figures = [
        FigureSpec(str(row["file"]), [str(u) for u in row.get("urls", [])], str(row["caption"]))
        for row in cfg.get("figures", [])
    ]
    return ExtrasPlan(
        figures=figures or base.figures,
        hebrew_summaries=[str(s) for s in cfg.get("hebrew_summaries", [])]
        or base.hebrew_summaries,
        table_chapter=cfg.get("table_chapter", base.table_chapter),
        equation_chapter=cfg.get("equation_chapter", base.equation_chapter),
        plot_chapter=cfg.get("plot_chapter", base.plot_chapter),
    )


def build_chapter_extras(
    plan: ExtrasPlan,
    chapter_number: int,
    *,
    hebrew_override: str | None = None,
) -> ChapterExtras | None:
    """Assemble one chapter's extras; outline-provided Hebrew wins over the plan."""
    index = chapter_number - 1
    figure = plan.figures[index] if 0 <= index < len(plan.figures) else None
    hebrew = hebrew_override
    if not hebrew and 0 <= index < len(plan.hebrew_summaries):
        hebrew = plan.hebrew_summaries[index]
    flags = (
        chapter_number == plan.table_chapter,
        chapter_number == plan.equation_chapter,
        chapter_number == plan.plot_chapter,
    )
    if figure is None and hebrew is None and not any(flags):
        return None
    return ChapterExtras(
        figure_file=figure.file if figure else None,
        figure_caption=figure.caption if figure else None,
        hebrew_summary=hebrew,
        include_milestones_table=flags[0],
        include_rocket_equation=flags[1],
        include_timeline_plot=flags[2],
    )
