"""Render agent-provided media specs and dispatch per-chapter extra blocks."""

from __future__ import annotations

from bookgen.latex.blocks import (
    ChapterExtras,
    render_figure,
    render_milestones_table,
    render_rocket_equation,
    render_timeline_plot,
)
from bookgen.latex.escape import escape_latex
from bookgen.latex.hebrew import render_hebrew_summary
from bookgen.models import EquationSpec, TableSpec


def render_table_spec(spec: TableSpec) -> str:
    """Render an agent-provided table with booktabs (all cells escaped)."""
    column_format = "@{}" + "l" * len(spec.columns) + "@{}"
    header = " & ".join(escape_latex(col) for col in spec.columns)
    body = "".join(
        " & ".join(escape_latex(cell) for cell in row) + " \\\\\n" for row in spec.rows
    )
    return (
        "\\begin{table}[htbp]\n"
        "\\centering\n"
        f"\\caption{{{escape_latex(spec.caption)}}}\n"
        f"\\begin{{tabular}}{{{column_format}}}\n"
        "\\toprule\n"
        f"{header} \\\\\n"
        "\\midrule\n"
        f"{body}"
        "\\bottomrule\n"
        "\\end{tabular}\n"
        "\\end{table}\n"
    )


def render_equation_spec(spec: EquationSpec) -> str:
    """Render an agent-provided display equation (math validated by the model)."""
    tail = f"\n{escape_latex(spec.explanation)}\n" if spec.explanation else ""
    return (
        f"{escape_latex(spec.intro)}\n"
        "\\begin{equation}\n"
        f"{spec.latex}\n"
        "\\end{equation}\n"
        f"{tail}"
    )


def render_chart_figure(chart_file: str, caption: str) -> str:
    """Include the Python-rendered (matplotlib) chart for an agent ChartSpec."""
    return (
        "\\begin{figure}[htbp]\n"
        "\\centering\n"
        f"\\includegraphics[width=0.92\\linewidth]{{figures/{chart_file}}}\n"
        f"\\caption{{{escape_latex(caption)}}}\n"
        "\\label{fig:agent_chart}\n"
        "\\end{figure}\n"
    )


def render_chapter_extras(extras: ChapterExtras | None) -> str:
    """Render optional blocks appended after a chapter's English sections.

    Agent-provided specs (live runs) take precedence over the built-in Moon
    Race blocks (offline fixtures mode).
    """
    if extras is None:
        return ""
    blocks: list[str] = []
    if extras.table_spec is not None:
        blocks.append(render_table_spec(extras.table_spec).rstrip())
    elif extras.include_milestones_table:
        blocks.append(render_milestones_table().rstrip())
    if extras.equation_spec is not None:
        blocks.append(render_equation_spec(extras.equation_spec).rstrip())
    elif extras.include_rocket_equation:
        blocks.append(render_rocket_equation().rstrip())
    if extras.figure_file and extras.figure_caption:
        blocks.append(render_figure(extras.figure_file, extras.figure_caption).rstrip())
    if extras.chart_file and extras.chart_caption:
        blocks.append(render_chart_figure(extras.chart_file, extras.chart_caption).rstrip())
    elif extras.include_timeline_plot:
        blocks.append(render_timeline_plot().rstrip())
    if extras.hebrew_summary:
        blocks.append(render_hebrew_summary(extras.hebrew_summary).rstrip())
    return "\n\n".join(blocks)
