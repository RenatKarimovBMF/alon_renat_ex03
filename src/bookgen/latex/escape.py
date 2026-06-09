"""LaTeX escaping helpers."""

from __future__ import annotations

_ESCAPE_MAP = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def escape_latex(text: str) -> str:
    """Escape characters that break LaTeX compilation."""
    escaped = []
    for char in text:
        escaped.append(_ESCAPE_MAP.get(char, char))
    return "".join(escaped)
