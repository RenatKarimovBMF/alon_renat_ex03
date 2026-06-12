"""Tests for config-driven extras, the bib-key reader, and live workspaces."""

from pathlib import Path

from bookgen.crew.extras import build_chapter_extras, load_extras_plan, moon_extras_plan
from bookgen.latex.bib import read_bib_keys
from bookgen.latex.workspace import example_workspace, stage_latex_workspace
from bookgen.shared.config import load_book_config

ROOT = Path(__file__).resolve().parents[2]


def test_extras_plan_defaults_to_moon_race() -> None:
    book = load_book_config(ROOT / "config" / "book.json")
    plan = load_extras_plan(book)
    assert len(plan.figures) == 6
    assert len(plan.hebrew_summaries) == 6
    assert (plan.table_chapter, plan.equation_chapter, plan.plot_chapter) == (1, 3, 4)


def test_extras_plan_honors_config_override() -> None:
    book = load_book_config(ROOT / "config" / "book.json")
    book.extras = {
        "figures": [{"file": "x.jpg", "urls": ["https://e.test/x.jpg"], "caption": "X"}],
        "hebrew_summaries": ["סיכום לדוגמה."],
        "table_chapter": 2,
        "equation_chapter": None,
        "plot_chapter": 1,
    }
    plan = load_extras_plan(book)
    assert plan.figures[0].file == "x.jpg"
    assert plan.table_chapter == 2 and plan.equation_chapter is None
    extras = build_chapter_extras(plan, 1)
    assert extras is not None and extras.include_timeline_plot
    assert extras.hebrew_summary == "סיכום לדוגמה."


def test_outline_hebrew_overrides_plan() -> None:
    plan = moon_extras_plan()
    extras = build_chapter_extras(plan, 2, hebrew_override="סיכום מהשרטוט.")
    assert extras is not None and extras.hebrew_summary == "סיכום מהשרטוט."


def test_read_bib_keys_filters_meta_sources() -> None:
    keys = read_bib_keys(ROOT / "latex" / "references.bib")
    assert "siddiqi2010" in keys and "nasaimages" in keys
    assert "team2026" not in keys and "crewai2026" not in keys
    assert "team2026" in read_bib_keys(ROOT / "latex" / "references.bib", include_meta=True)


def test_stage_latex_workspace_copies_sources(tmp_path: Path) -> None:
    dst = stage_latex_workspace(ROOT / "latex", tmp_path / "latex")
    assert (dst / "main.tex").exists()
    assert (dst / "preamble.tex").exists()
    assert (dst / "references.bib").exists()
    for sub in ("chapters", "figures", "build"):
        assert (dst / sub).is_dir()


def test_example_workspace_is_topic_slugged() -> None:
    path = example_workspace(ROOT, "The Moon Race: USSR vs US")
    assert path.parent == ROOT / "examples"
    assert path.name.startswith("the_moon_race_ussr_vs_us-")
