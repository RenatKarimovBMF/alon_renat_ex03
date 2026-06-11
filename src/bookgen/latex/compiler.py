"""Compile LaTeX projects and parse build logs."""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

from bookgen.models import BuildReport

_ERROR_PATTERNS = (
    re.compile(r"^! (.+)$"),
    re.compile(r"LaTeX Error: (.+)$"),
    re.compile(r"Package \w+ Error: (.+)$"),
)


def parse_log_errors(log_text: str) -> list[str]:
    """Extract human-readable errors from a LaTeX log file."""
    errors: list[str] = []
    for line in log_text.splitlines():
        stripped = line.strip()
        for pattern in _ERROR_PATTERNS:
            match = pattern.search(stripped)
            if match is not None:
                errors.append(match.group(1))
                break
    return errors


def _read_log(build_dir: Path, stem: str) -> list[str]:
    log_path = build_dir / f"{stem}.log"
    if not log_path.exists():
        return []
    return parse_log_errors(log_path.read_text(encoding="utf-8", errors="replace"))


def _prepare_build(main_file: Path, build_dir: Path) -> None:
    """Copy bibliography into the build directory for bibtex."""
    build_dir.mkdir(parents=True, exist_ok=True)
    bib = main_file.parent / "references.bib"
    if bib.exists():
        shutil.copy2(bib, build_dir / "references.bib")


def _compile_with_pdflatex(main_file: Path, build_dir: Path) -> BuildReport:
    """Fallback when latexmk is unavailable (e.g. missing Perl on MiKTeX)."""
    pdflatex = shutil.which("pdflatex")
    bibtex = shutil.which("bibtex")
    if pdflatex is None:
        return BuildReport(
            success=False,
            attempts=0,
            errors=["pdflatex not found on PATH — install MiKTeX or TeX Live"],
        )

    _prepare_build(main_file, build_dir)
    stem = main_file.stem
    compile_stem = f"{stem}_compile"
    workdir = main_file.parent
    pdf_path = build_dir / f"{stem}.pdf"
    temp_pdf = build_dir / f"{compile_stem}.pdf"

    args = [
        pdflatex,
        "-interaction=nonstopmode",
        f"-output-directory={build_dir}",
        f"-jobname={compile_stem}",
        str(main_file.name),
    ]
    errors: list[str] = []

    for _ in range(2):
        subprocess.run(args, cwd=workdir, capture_output=True, text=True, check=False)
        errors = _read_log(build_dir, compile_stem)

    if bibtex is not None:
        subprocess.run([bibtex, compile_stem], cwd=build_dir, capture_output=True, text=True, check=False)

    proc = subprocess.run(args, cwd=workdir, capture_output=True, text=True, check=False)
    errors = _read_log(build_dir, compile_stem)
    for _ in range(2):
        proc = subprocess.run(args, cwd=workdir, capture_output=True, text=True, check=False)
        errors = _read_log(build_dir, compile_stem)

    if proc.returncode != 0 or not temp_pdf.exists():
        if not errors and proc.stderr:
            errors = [proc.stderr.strip()]
        return BuildReport(
            success=False,
            attempts=6,
            errors=errors or ["pdflatex build failed"],
            log_path=str(build_dir / f"{compile_stem}.log"),
        )

    try:
        temp_pdf.replace(pdf_path)
        final_pdf = pdf_path
    except OSError:
        final_pdf = temp_pdf

    return BuildReport(
        success=True,
        pdf_path=str(final_pdf),
        attempts=6,
        errors=[],
        log_path=str(build_dir / f"{compile_stem}.log"),
    )


def compile_latex(
    main_file: Path,
    *,
    build_dir: Path,
    max_attempts: int = 3,
) -> BuildReport:
    """Compile main.tex using latexmk when available, else pdflatex+bibtex."""
    if not main_file.exists():
        return BuildReport(success=False, attempts=0, errors=[f"Missing main file: {main_file}"])

    build_dir.mkdir(parents=True, exist_ok=True)
    latexmk = shutil.which("latexmk")
    if latexmk is None:
        return _compile_with_pdflatex(main_file, build_dir)

    cmd = [
        latexmk,
        "-pdf",
        "-interaction=nonstopmode",
        f"-output-directory={build_dir}",
        str(main_file),
    ]
    errors: list[str] = []
    log_path = build_dir / f"{main_file.stem}.log"
    stem = main_file.stem

    for attempt in range(1, max_attempts + 1):
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        errors = _read_log(build_dir, stem)
        combined = f"{proc.stdout}\n{proc.stderr}\n{' '.join(errors)}".lower()
        if "perl" in combined or "script engine" in combined:
            return _compile_with_pdflatex(main_file, build_dir)
        pdf_path = build_dir / f"{stem}.pdf"
        if proc.returncode == 0 and pdf_path.exists():
            return BuildReport(
                success=True,
                pdf_path=str(pdf_path),
                attempts=attempt,
                errors=[],
                log_path=str(log_path),
            )
        if not errors and proc.stderr:
            errors = [proc.stderr.strip()]

    fallback = _compile_with_pdflatex(main_file, build_dir)
    if fallback.success:
        return fallback

    return BuildReport(
        success=False,
        attempts=max_attempts,
        errors=errors or fallback.errors or ["LaTeX build failed without parsed errors"],
        log_path=str(log_path) if log_path.exists() else fallback.log_path,
    )
