"""Tests for LaTeX assembly helpers."""

from pathlib import Path

from bookgen.crew.assemble import assemble_latex, build_review
from bookgen.crew.demo_fixtures import build_demo_outline, build_demo_sections
from bookgen.shared.config import load_book_config

ROOT = Path(__file__).resolve().parents[2]


def test_build_review_approves_demo_content() -> None:
    book = load_book_config(ROOT / "config" / "book.json")
    book.demo_mode["enabled"] = True
    outline = build_demo_outline(book)
    bundle = build_demo_sections(outline)
    review = build_review(outline, bundle, words_per_page=450, tolerance=10)
    assert review.estimated_pages > 0


def test_assemble_latex_writes_chapters(tmp_path: Path) -> None:
    book = load_book_config(ROOT / "config" / "book.json")
    book.demo_mode["enabled"] = True
    outline = build_demo_outline(book)
    bundle = build_demo_sections(outline)
    latex_root = tmp_path / "latex"
    latex_root.mkdir()
    (latex_root / "chapters").mkdir()
    main_tex = latex_root / "main.tex"
    main_tex.write_text(
        "\\documentclass{article}\n\\begin{document}\n\\bibliographystyle{plain}\n\\end{document}\n",
        encoding="utf-8",
    )
    # Inject an offline figures stub: no network, no matplotlib.
    paths = assemble_latex(
        latex_root, main_tex, outline, bundle, ensure_figures_fn=lambda _root: []
    )
    assert paths
    assert paths[0].exists()
