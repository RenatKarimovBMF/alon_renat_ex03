"""Write LaTeX chapter files from structured drafts."""

from __future__ import annotations

import re
from pathlib import Path

from bookgen.latex.escape import escape_latex
from bookgen.models import SectionDraft

_INPUT_LINE = re.compile(r"^\\input\{chapters/(.+)\}\s*$", re.MULTILINE)


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


def write_chapter_file(
    latex_root: Path,
    chapter_number: int,
    chapter_title: str,
    sections: list[SectionDraft],
) -> Path:
    """Write one chapter file from ordered sections."""
    slug = slugify(chapter_title or f"chapter_{chapter_number}")
    filename = f"ch{chapter_number:02d}_{slug}.tex"
    target = guard_latex_path(latex_root, f"chapters/{filename}")
    target.parent.mkdir(parents=True, exist_ok=True)
    parts = [rf"\section{{{escape_latex(chapter_title)}}}"]
    for section in sections:
        parts.append(render_section(section).rstrip())
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
