"""Parse human-readable errors out of LaTeX build logs."""

from __future__ import annotations

import re
from pathlib import Path

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


def read_log(build_dir: Path, stem: str) -> list[str]:
    """Read and parse ``<stem>.log`` from the build directory if present."""
    log_path = build_dir / f"{stem}.log"
    if not log_path.exists():
        return []
    return parse_log_errors(log_path.read_text(encoding="utf-8", errors="replace"))
