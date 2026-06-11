"""Write LaTeX chapter files from structured drafts."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from bookgen.latex.escape import escape_latex
from bookgen.models import SectionDraft

_INPUT_LINE = re.compile(r"^\\input\{chapters/(.+)\}\s*$", re.MULTILINE)


@dataclass(frozen=True)
class ChapterExtras:
    """Optional per-chapter LaTeX blocks (figure, Hebrew summary, table, plot)."""

    figure_file: str | None = None
    figure_caption: str | None = None
    hebrew_summary: str | None = None
    include_milestones_table: bool = False
    include_rocket_equation: bool = False
    include_timeline_plot: bool = False


def guard_latex_path(root: Path, relative: str) -> Path:
    """Ensure a target path stays under the LaTeX project root."""
    target = (root / relative).resolve()
    if root.resolve() not in target.parents and target != root.resolve():
        raise ValueError(f"Path escapes latex root: {relative}")
    return target


def slugify(title: str) -> str:
    """Build a filesystem-safe slug."""
    lowered = title.lower().strip()
    cleaned = re.sub(r"[^a-z0-9]+", "_", lowered).strip("_")
    return cleaned or "section"


def render_section(section: SectionDraft) -> str:
    """Render one section draft to LaTeX source."""
    lines = [rf"\subsection{{{escape_latex(section.section_title)}}}"]
    cite_suffix = " ".join(rf"\cite{{{key}}}" for key in section.citations)
    for paragraph in section.body_paragraphs:
        body = escape_latex(paragraph)
        if cite_suffix:
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


def render_hebrew_summary(text: str) -> str:
    """Render Hebrew text in an isolated RTL block (no English on same lines)."""
    return (
        "\\clearpage\n"
        "\\begin{otherlanguage}{hebrew}\n"
        "\\subsection*{סיכום הפרק}\n\n"
        f"{text.strip()}\n\n"
        "\\end{otherlanguage}\n"
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


def write_chapter_file(
    latex_root: Path,
    chapter_number: int,
    chapter_title: str,
    sections: list[SectionDraft],
    *,
    extras: ChapterExtras | None = None,
) -> Path:
    """Write one chapter file from ordered sections."""
    slug = slugify(chapter_title or f"chapter_{chapter_number}")
    filename = f"ch{chapter_number:02d}_{slug}.tex"
    target = guard_latex_path(latex_root, f"chapters/{filename}")
    target.parent.mkdir(parents=True, exist_ok=True)
    parts = [rf"\section{{{escape_latex(chapter_title)}}}"]
    for section in sections:
        parts.append(render_section(section).rstrip())
    extra_block = render_chapter_extras(extras)
    if extra_block:
        parts.append(extra_block)
    target.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    return target


def update_main_inputs(main_tex: Path, chapter_paths: list[Path]) -> None:
    """Replace chapter \\input lines in main.tex deterministically."""
    content = main_tex.read_text(encoding="utf-8")
    inputs = [f"\\input{{chapters/{path.name}}}" for path in chapter_paths]
    block = "\n".join(inputs)
    if _INPUT_LINE.search(content):
        content = _INPUT_LINE.sub("", content)
    marker = "\\bibliographystyle"
    if marker not in content:
        raise ValueError("main.tex missing bibliography marker")
    head, tail = content.split(marker, maxsplit=1)
    cleaned = head.rstrip() + "\n\n" + block + "\n\n" + marker + tail
    main_tex.write_text(cleaned, encoding="utf-8")
