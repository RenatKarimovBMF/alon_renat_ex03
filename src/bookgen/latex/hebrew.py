"""Hebrew RTL block rendering with correct BiDi handling."""

from __future__ import annotations

import re

# Latin/digit runs (incl. compounds like N1, 4.5, U.S-2) inside RTL Hebrew.
_LTR_RUN = re.compile(r"[A-Za-z0-9]+(?:[./-][A-Za-z0-9]+)*")


def _ltr_runs(text: str) -> str:
    """Keep Latin/digit runs left-to-right inside RTL Hebrew text.

    Without this, babel-hebrew typesets such runs right-to-left, so a year
    like 1961 prints as 1691 and ``N1`` prints as ``1N``. The TeX--XeT
    primitives ``\\beginL/\\endL`` create a proper LTR island; a
    ``\\foreignlanguage`` switch scrambles the surrounding RTL word order
    instead.
    """
    return _LTR_RUN.sub(lambda m: rf"{{\beginL {m.group(0)}\endL}}", text)


def render_hebrew_summary(text: str) -> str:
    """Render Hebrew text in an isolated RTL block (no English on same lines).

    No leading page break: the summary stays visually attached to its own
    chapter. Chapter separation is a trailing break in ``write_chapter_file``.
    """
    return (
        "\\bigskip\n"
        "\\begin{otherlanguage}{hebrew}\n"
        "\\subsection*{סיכום הפרק}\n\n"
        f"{_ltr_runs(text.strip())}\n\n"
        "\\end{otherlanguage}\n"
    )
