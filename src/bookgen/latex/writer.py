"""Write LaTeX chapter files and refresh main.tex inputs."""

from __future__ import annotations

import re
from pathlib import Path

from bookgen.latex.blocks import ChapterExtras, render_section, slugify
from bookgen.latex.escape import escape_latex
from bookgen.latex.media_render import render_chapter_extras
from bookgen.models import SectionDraft

# Re-exported so existing imports (assemble, tests) keep working.
__all__ = [
    "ChapterExtras",
    "guard_latex_path",
    "render_section",
    "update_main_inputs",
    "write_chapter_file",
]

_INPUT_LINE = re.compile(r"^\\input\{chapters/(.+)\}\s*$", re.MULTILINE)


def guard_latex_path(root: Path, relative: str) -> Path:
    """Ensure a target path stays under the LaTeX project root."""
    target = (root / relative).resolve()
    if root.resolve() not in target.parents and target != root.resolve():
        raise ValueError(f"Path escapes latex root: {relative}")
    return target


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
    # Trailing break keeps each chapter (with its summary) on its own pages.
    body = "\n\n".join(parts) + "\n\n\\clearpage\n"
    target.write_text(body, encoding="utf-8")
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
