"""Assemble LaTeX files and compute review metrics."""

from __future__ import annotations

from collections.abc import Callable
from functools import partial
from pathlib import Path

from bookgen.crew.extras import ExtrasPlan, build_chapter_extras, moon_extras_plan
from bookgen.latex.figures import ensure_figures
from bookgen.latex.metadata import update_metadata
from bookgen.latex.writer import update_main_inputs, write_chapter_file
from bookgen.models import BookOutline, ReviewReport, SectionDraft, SectionDraftBundle

FiguresFn = Callable[[Path], object]


def group_sections(sections: list[SectionDraft]) -> dict[int, list[SectionDraft]]:
    grouped: dict[int, list[SectionDraft]] = {}
    for section in sections:
        grouped.setdefault(section.chapter_number, []).append(section)
    return grouped


def assemble_latex(
    latex_root: Path,
    main_tex: Path,
    outline: BookOutline,
    bundle: SectionDraftBundle,
    *,
    ensure_figures_fn: FiguresFn | None = None,
    extras_plan: ExtrasPlan | None = None,
) -> list[Path]:
    """Write chapter files and refresh main.tex inputs.

    ``extras_plan`` carries the subject's figures/Hebrew/table/equation/plot
    assignments (Moon Race plan by default). ``ensure_figures_fn`` is
    injectable so unit tests can run offline without downloads or matplotlib.
    """
    plan = extras_plan or moon_extras_plan()
    if ensure_figures_fn is None:
        ensure_figures_fn = partial(ensure_figures, figures=plan.figure_tuples())
    ensure_figures_fn(latex_root)
    chapter_paths: list[Path] = []
    grouped = group_sections(bundle.sections)
    for chapter in outline.chapters:
        sections = grouped.get(chapter.number, [])
        if not sections:
            continue
        extras = build_chapter_extras(
            plan,
            chapter.number,
            hebrew_override=chapter.hebrew_summary,
        )
        chapter_paths.append(
            write_chapter_file(
                latex_root,
                chapter.number,
                chapter.title,
                sections,
                extras=extras,
            )
        )
    if chapter_paths:
        update_main_inputs(main_tex, chapter_paths)
        update_metadata(
            latex_root / "metadata.tex",
            title=outline.title,
            authors=r"Renat Karimov \and Alon Engel",
        )
    return chapter_paths


def build_review(
    outline: BookOutline,
    bundle: SectionDraftBundle,
    *,
    words_per_page: int,
    tolerance: int,
) -> ReviewReport:
    """Build a deterministic review report from draft word counts."""
    words = sum(len(" ".join(section.body_paragraphs).split()) for section in bundle.sections)
    estimated = round(words / max(words_per_page, 1), 2)
    delta = abs(estimated - outline.target_total_pages)
    issues: list[str] = []
    if delta > tolerance:
        issues.append(
            f"Estimated {estimated} pages vs target {outline.target_total_pages}"
        )
    return ReviewReport(
        estimated_pages=estimated,
        issues=issues,
        approved=delta <= tolerance,
        glossary={"Apollo": "United States crewed lunar landing program"},
    )
