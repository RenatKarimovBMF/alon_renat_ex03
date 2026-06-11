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


def _pick_jobname(build_dir: Path, stem: str) -> str:
    """Use an alternate job name when an existing PDF is open in a viewer."""
    pdf = build_dir / f"{stem}.pdf"
    if not pdf.exists():
        return stem
    try:
        with pdf.open("ab"):
            pass
    except OSError:
        return f"{stem}_build"
    return stem


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

    build_dir.mkdir(parents=True, exist_ok=True)
    stem = _pick_jobname(build_dir, main_file.stem)
    workdir = main_file.parent
    args = [
        pdflatex,
        "-interaction=nonstopmode",
        f"-output-directory={build_dir}",
        f"-jobname={stem}",
        str(main_file.name),
    ]
    errors: list[str] = []
    for _ in range(2):
        proc = subprocess.run(args, cwd=workdir, capture_output=True, text=True, check=False)
        errors = _read_log(build_dir, stem)
        if proc.returncode != 0 and not errors and proc.stderr:
            errors = [proc.stderr.strip()]

    if bibtex is not None:
        subprocess.run([bibtex, stem], cwd=build_dir, capture_output=True, text=True, check=False)

    for _ in range(2):
        proc = subprocess.run(args, cwd=workdir, capture_output=True, text=True, check=False)
        errors = _read_log(build_dir, stem)
        pdf_path = build_dir / f"{stem}.pdf"
        if proc.returncode == 0 and pdf_path.exists():
            return BuildReport(
                success=True,
                pdf_path=str(pdf_path),
                attempts=4,
                errors=[],
                log_path=str(build_dir / f"{stem}.log"),
            )

    return BuildReport(
        success=False,
        attempts=4,
        errors=errors or ["pdflatex build failed"],
        log_path=str(build_dir / f"{stem}.log"),
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
        if "perl" in combined or "script engine" in combined:
            return _compile_with_pdflatex(main_file, build_dir)

    fallback = _compile_with_pdflatex(main_file, build_dir)
    if fallback.success:
        return fallback

    return BuildReport(
        success=False,
        attempts=max_attempts,
        errors=errors or fallback.errors or ["LaTeX build failed without parsed errors"],
        log_path=str(log_path) if log_path.exists() else fallback.log_path,
    )
