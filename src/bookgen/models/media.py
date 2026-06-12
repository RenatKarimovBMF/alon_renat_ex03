"""Agent-specified media for live runs (images, table, equation, chart).

The crew decides the content *and* the placement (which chapter carries each
element); Python only fetches, renders, and compiles. Validators reject unsafe
or malformed specs at parse time so CrewAI's converter retries the task.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

# TeX primitives that have no business inside a display equation.
_TEX_DENYLIST = (
    "\\input", "\\include", "\\write", "\\read", "\\openout", "\\openin",
    "\\catcode", "\\def", "\\csname", "\\usepackage", "\\RequirePackage",
    "\\newcommand", "\\renewcommand", "\\expandafter", "\\begin{document}",
    "\\end{document}", "\\immediate", "\\loop",
)


class FigureRequest(BaseModel):
    """One chapter image, fetched from the public web at run time."""

    image_query: str = Field(min_length=3, max_length=120)
    caption: str = Field(min_length=8, max_length=240)


class TableSpec(BaseModel):
    """Agent-provided data table (rendered with booktabs)."""

    caption: str = Field(min_length=8, max_length=160)
    columns: list[str] = Field(min_length=2, max_length=5)
    rows: list[list[str]] = Field(min_length=3, max_length=8)

    @field_validator("rows")
    @classmethod
    def rows_match_columns(cls, rows: list[list[str]], info) -> list[list[str]]:
        width = len(info.data.get("columns", []))
        if width and any(len(row) != width for row in rows):
            raise ValueError("every table row must have exactly one cell per column")
        return rows


class EquationSpec(BaseModel):
    """Agent-provided display equation (math body only, no $$ wrappers)."""

    intro: str = Field(min_length=8, max_length=300)
    latex: str = Field(min_length=3, max_length=300)
    explanation: str = Field(default="", max_length=300)

    @field_validator("latex")
    @classmethod
    def latex_is_safe_math(cls, latex: str) -> str:
        lowered = latex.replace(" ", "")
        for token in _TEX_DENYLIST:
            if token in lowered:
                raise ValueError(f"equation may not contain {token}")
        if "$" in latex:
            raise ValueError("provide the math body only, without $ delimiters")
        return latex


class ChartPoint(BaseModel):
    """One labeled value in the agent-specified chart."""

    label: str = Field(min_length=1, max_length=40)
    value: float


class ChartSpec(BaseModel):
    """Agent-provided data chart, rendered with matplotlib (Python-generated)."""

    title: str = Field(min_length=4, max_length=120)
    y_label: str = Field(default="", max_length=60)
    points: list[ChartPoint] = Field(min_length=3, max_length=10)
