"""Isolated LaTeX workspaces for live runs (``examples/<topic>-<stamp>/``).

A live crew rewrites chapter files and the compiled PDF. Staging a copy of the
LaTeX sources keeps the canonical ``latex/`` tree (the graded artifact)
untouched and unlocked, and turns every live run into a self-contained example
folder: sources, figures, build output, session JSON, and cost report.
"""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from bookgen.latex.blocks import slugify


def example_workspace(project_root: Path, topic: str) -> Path:
    """Pick a fresh example folder for one live run."""
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return project_root / "examples" / f"{slugify(topic)}-{stamp}"


def stage_latex_workspace(src_latex: Path, dst_latex: Path) -> Path:
    """Copy static LaTeX sources into the workspace (chapters are generated)."""
    dst_latex.mkdir(parents=True, exist_ok=True)
    for path in sorted(src_latex.glob("*.tex")):
        shutil.copy2(path, dst_latex / path.name)
    bib = src_latex / "references.bib"
    if bib.exists():
        shutil.copy2(bib, dst_latex / bib.name)
    for sub in ("chapters", "figures", "build"):
        (dst_latex / sub).mkdir(exist_ok=True)
    return dst_latex
