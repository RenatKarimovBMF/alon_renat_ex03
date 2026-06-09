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


def compile_latex(
    main_file: Path,
    *,
    build_dir: Path,
    max_attempts: int = 3,
) -> BuildReport:
    """Compile main.tex using latexmk when available."""
    if not main_file.exists():
        return BuildReport(success=False, attempts=0, errors=[f"Missing main file: {main_file}"])

    build_dir.mkdir(parents=True, exist_ok=True)
    latexmk = shutil.which("latexmk")
    if latexmk is None:
        return BuildReport(
            success=False,
            attempts=0,
            errors=["latexmk not found on PATH — install MiKTeX or TeX Live"],
        )

    cmd = [
        latexmk,
        "-pdf",
        "-interaction=nonstopmode",
        f"-output-directory={build_dir}",
        str(main_file),
    ]
    errors: list[str] = []
    log_path = build_dir / f"{main_file.stem}.log"

    for attempt in range(1, max_attempts + 1):
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if log_path.exists():
            errors = parse_log_errors(log_path.read_text(encoding="utf-8", errors="replace"))
        pdf_path = build_dir / f"{main_file.stem}.pdf"
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

    return BuildReport(
        success=False,
        attempts=max_attempts,
        errors=errors or ["LaTeX build failed without parsed errors"],
        log_path=str(log_path) if log_path.exists() else None,
    )
