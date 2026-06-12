"""Render LaTeX content blocks (sections, figure, table, equation, summary)."""

from __future__ import annotations

import re
from dataclasses import dataclass

from bookgen.latex.escape import escape_latex
from bookgen.latex.hebrew import render_hebrew_summary
from bookgen.models import SectionDraft


@dataclass(frozen=True)
class ChapterExtras:
    """Optional per-chapter LaTeX blocks (figure, Hebrew summary, table, plot)."""

    figure_file: str | None = None
    figure_caption: str | None = None
    hebrew_summary: str | None = None
    include_milestones_table: bool = False
    include_rocket_equation: bool = False
    include_timeline_plot: bool = False


def slugify(title: str) -> str:
    """Build a filesystem-safe slug."""
    lowered = title.lower().strip()
    cleaned = re.sub(r"[^a-z0-9]+", "_", lowered).strip("_")
    return cleaned or "section"


def render_section(section: SectionDraft) -> str:
    """Render one section draft to LaTeX source.

    Citations are attached once, after the final paragraph, so a section reads
    as prose rather than repeating the same ``\\cite`` markers on every line.
    """
    lines = [rf"\subsection{{{escape_latex(section.section_title)}}}"]
    cite_suffix = " ".join(rf"\cite{{{key}}}" for key in section.citations)
    last_index = len(section.body_paragraphs) - 1
    for index, paragraph in enumerate(section.body_paragraphs):
        body = escape_latex(paragraph)
        if cite_suffix and index == last_index:
            body = f"{body} {cite_suffix}"
        lines.append(body)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_figure(filename: str, caption: str) -> str:
    """Render a centered figure from latex/figures/."""
    return (
        "\\begin{figure}[htbp]\n"
        "\\centering\n"
        f"\\includegraphics[width=0.88\\linewidth]{{figures/{filename}}}\n"
        f"\\caption{{{escape_latex(caption)}}}\n"
        f"\\label{{fig:ch_{slugify(caption)[:32]}}}\n"
        "\\end{figure}\n"
    )


def render_milestones_table() -> str:
    """Render the required missions table (English only)."""
    return (
        "\\begin{table}[htbp]\n"
        "\\centering\n"
        "\\caption{Selected Moon Race milestones}\n"
        "\\label{tab:milestones}\n"
        "\\begin{tabular}{@{}lll@{}}\n"
        "\\toprule\n"
        "Year & Program & Milestone \\\\\n"
        "\\midrule\n"
        "1957 & Sputnik & First artificial satellite \\\\\n"
        "1961 & Vostok & First human orbital flight \\\\\n"
        "1965 & Gemini & Rendezvous and EVA practice \\\\\n"
        "1969 & Apollo 11 & First crewed lunar landing \\\\\n"
        "1975 & Apollo--Soyuz & Post-race cooperation \\\\\n"
        "\\bottomrule\n"
        "\\end{tabular}\n"
        "\\end{table}\n"
    )


def render_rocket_equation() -> str:
    """Render Tsiolkovsky rocket equation (fancy math, English caption)."""
    return (
        "The ideal rocket equation relates velocity change to mass ratio:\n"
        "\\begin{equation}\n"
        "\\Delta v = v_e \\ln\\!\\left(\\frac{m_0}{m_f}\\right)\n"
        "\\label{eq:rocket}\n"
        "\\end{equation}\n"
        "where $v_e$ is effective exhaust velocity, $m_0$ initial mass, and $m_f$ final mass.\n"
    )


def render_timeline_plot() -> str:
    """Include the Python-generated matplotlib chart."""
    return (
        "\\begin{figure}[htbp]\n"
        "\\centering\n"
        "\\includegraphics[width=0.92\\linewidth]{figures/mission_timeline.pdf}\n"
        "\\caption{Moon Race milestones chart generated with Python (matplotlib).}\n"
        "\\label{fig:timeline}\n"
        "\\end{figure}\n"
    )




def render_chapter_extras(extras: ChapterExtras | None) -> str:
    """Render optional blocks appended after English sections."""
    if extras is None:
        return ""
    blocks: list[str] = []
    if extras.include_milestones_table:
        blocks.append(render_milestones_table().rstrip())
    if extras.include_rocket_equation:
        blocks.append(render_rocket_equation().rstrip())
    if extras.figure_file and extras.figure_caption:
        blocks.append(render_figure(extras.figure_file, extras.figure_caption).rstrip())
    if extras.include_timeline_plot:
        blocks.append(render_timeline_plot().rstrip())
    if extras.hebrew_summary:
        blocks.append(render_hebrew_summary(extras.hebrew_summary).rstrip())
    return "\n\n".join(blocks)
