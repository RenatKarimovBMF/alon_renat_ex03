"""Update LaTeX metadata for the generated book."""

from __future__ import annotations

from pathlib import Path

from bookgen.latex.escape import escape_latex


def update_metadata(metadata_path: Path, *, title: str, authors: str) -> None:
    """Rewrite metadata.tex with escaped title and authors."""
    safe_title = escape_latex(title).replace("\n", " ")
    lines = [
        rf"\title{{{safe_title}}}",
        rf"\author{{{authors}}}",
        r"\date{\today}",
        "",
    ]
    metadata_path.write_text("\n".join(lines), encoding="utf-8")
