"""Compile LaTeX projects via latexmk, falling back to pdflatex+bibtex."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from bookgen.latex.build_fs import (
    BUILD_STEM,
    cleanup_build_artifacts,
    prepare_build,
    remove_stray_book_pdfs,
)
from bookgen.latex.build_logs import read_log
from bookgen.models import BuildReport


def _finalize_pdf(
    temp_pdf: Path,
    pdf_path: Path,
    *,
    latex_root: Path,
    build_dir: Path,
    attempts: int,
    log_path: Path,
) -> BuildReport | None:
    """Move the temp PDF into place and clean up; None means 'locked output'."""
    try:
        temp_pdf.replace(pdf_path)
    except OSError:
        return BuildReport(
            success=False,
            attempts=attempts,
            errors=[f"Close {pdf_path} in your PDF viewer, then run again."],
            log_path=str(log_path),
        )
    cleanup_build_artifacts(build_dir, BUILD_STEM)
    remove_stray_book_pdfs(latex_root, build_dir, keep=pdf_path)
    return BuildReport(
        success=True, pdf_path=str(pdf_path), attempts=attempts, errors=[], log_path=str(log_path)
    )


def _compile_with_pdflatex(main_file: Path, build_dir: Path, *, output_pdf: str) -> BuildReport:
    """Fallback when latexmk is unavailable (e.g. missing Perl on MiKTeX)."""
    pdflatex = shutil.which("pdflatex")
    if pdflatex is None:
        return BuildReport(
            success=False,
            attempts=0,
            errors=["pdflatex not found on PATH — install MiKTeX or TeX Live"],
        )
    latex_root = main_file.parent
    prepare_build(main_file, build_dir)
    pdf_path = build_dir / output_pdf
    temp_pdf = build_dir / f"{BUILD_STEM}.pdf"
    log_path = build_dir / f"{BUILD_STEM}.log"
    remove_stray_book_pdfs(latex_root, build_dir, keep=pdf_path)

    args = [
        pdflatex,
        "-interaction=nonstopmode",
        f"-output-directory={build_dir}",
        f"-jobname={BUILD_STEM}",
        str(main_file.name),
    ]
    errors: list[str] = []
    bibtex = shutil.which("bibtex")
    for index in range(4):
        proc = subprocess.run(args, cwd=latex_root, capture_output=True, text=True, check=False)
        errors = read_log(build_dir, BUILD_STEM)
        if index == 0 and bibtex is not None:
            subprocess.run([bibtex, BUILD_STEM], cwd=build_dir, capture_output=True, check=False)

    if proc.returncode != 0 or not temp_pdf.exists():
        if not errors and proc.stderr:
            errors = [proc.stderr.strip()]
        return BuildReport(
            success=False, attempts=4, errors=errors or ["pdflatex build failed"], log_path=str(log_path)
        )
    result = _finalize_pdf(
        temp_pdf, pdf_path, latex_root=latex_root, build_dir=build_dir, attempts=4, log_path=log_path
    )
    return result if result is not None else BuildReport(success=False, attempts=4, errors=["finalize failed"])


def compile_latex(
    main_file: Path,
    *,
    build_dir: Path,
    output_pdf: str = "book.pdf",
    max_attempts: int = 3,
) -> BuildReport:
    """Compile main.tex using latexmk when available, else pdflatex+bibtex."""
    if not main_file.exists():
        return BuildReport(success=False, attempts=0, errors=[f"Missing main file: {main_file}"])

    build_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = build_dir / output_pdf
    remove_stray_book_pdfs(main_file.parent, build_dir, keep=pdf_path)

    latexmk = shutil.which("latexmk")
    if latexmk is None:
        return _compile_with_pdflatex(main_file, build_dir, output_pdf=output_pdf)

    cmd = [
        latexmk,
        "-pdf",
        "-interaction=nonstopmode",
        f"-jobname={BUILD_STEM}",
        f"-output-directory={build_dir}",
        str(main_file),
    ]
    errors: list[str] = []
    log_path = build_dir / f"{BUILD_STEM}.log"
    temp_pdf = build_dir / f"{BUILD_STEM}.pdf"

    for attempt in range(1, max_attempts + 1):
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        errors = read_log(build_dir, BUILD_STEM)
        combined = f"{proc.stdout}\n{proc.stderr}\n{' '.join(errors)}".lower()
        if "perl" in combined or "script engine" in combined:
            return _compile_with_pdflatex(main_file, build_dir, output_pdf=output_pdf)
        if proc.returncode == 0 and temp_pdf.exists():
            result = _finalize_pdf(
                temp_pdf, pdf_path,
                latex_root=main_file.parent, build_dir=build_dir,
                attempts=attempt, log_path=log_path,
            )
            if result is not None:
                return result
        if not errors and proc.stderr:
            errors = [proc.stderr.strip()]

    fallback = _compile_with_pdflatex(main_file, build_dir, output_pdf=output_pdf)
    if fallback.success:
        return fallback
    return BuildReport(
        success=False,
        attempts=max_attempts,
        errors=errors or fallback.errors or ["LaTeX build failed without parsed errors"],
        log_path=str(log_path) if log_path.exists() else fallback.log_path,
    )
