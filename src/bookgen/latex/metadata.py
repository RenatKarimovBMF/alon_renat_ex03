"""Update LaTeX metadata for the generated book."""

from __future__ import annotations

from pathlib import Path

from bookgen.latex.escape import escape_latex


def update_metadata(metadata_path: Path, *, title: str, authors: str) -> None:
    """Rewrite metadata.tex with escaped title and authors.

    ``\\BookTitle`` is also defined so the cover and the running header stay
    topic-dynamic (nothing about the subject is hardcoded in the template).
    """
    safe_title = escape_latex(title).replace("\n", " ")
    lines = [
        rf"\title{{{safe_title}}}",
        rf"\newcommand{{\BookTitle}}{{{safe_title}}}",
        rf"\author{{{authors}}}",
        r"\date{\today}",
        "",
    ]
    metadata_path.write_text("\n".join(lines), encoding="utf-8")
