"""Filesystem helpers for LaTeX builds (staging, cleanup, stray PDFs)."""

from __future__ import annotations

import shutil
from pathlib import Path

BUILD_STEM = "_book_build"


def prepare_build(main_file: Path, build_dir: Path) -> None:
    """Create the build directory and stage the bibliography for bibtex."""
    build_dir.mkdir(parents=True, exist_ok=True)
    bib = main_file.parent / "references.bib"
    if bib.exists():
        shutil.copy2(bib, build_dir / "references.bib")


def remove_stray_book_pdfs(latex_root: Path, build_dir: Path, *, keep: Path) -> None:
    """Delete misleading main.pdf copies; keep only the canonical output."""
    keep_resolved = keep.resolve()
    candidates = [
        latex_root / "main.pdf",
        build_dir / "main.pdf",
        build_dir / "main_compile.pdf",
        build_dir / "main_build.pdf",
    ]
    for path in candidates:
        if path is None or not path.exists():
            continue
        if path.resolve() == keep_resolved:
            continue
        path.unlink(missing_ok=True)


def cleanup_build_artifacts(build_dir: Path, compile_stem: str) -> None:
    """Remove temporary LaTeX job files after a successful build."""
    suffixes = (".aux", ".log", ".out", ".toc", ".bbl", ".blg", ".pdf", ".fls", ".fdb_latexmk")
    for suffix in suffixes:
        (build_dir / f"{compile_stem}{suffix}").unlink(missing_ok=True)
    for path in build_dir.glob("main.*"):
        path.unlink(missing_ok=True)
    for path in build_dir.glob("main_build.*"):
        path.unlink(missing_ok=True)
