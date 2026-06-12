"""Tests for LaTeX build filesystem helpers."""

from bookgen.latex.build_fs import (
    cleanup_build_artifacts,
    prepare_build,
    remove_stray_book_pdfs,
)


def test_prepare_build_copies_bibliography(tmp_path) -> None:
    latex_root = tmp_path / "latex"
    latex_root.mkdir()
    (latex_root / "references.bib").write_text("@book{x, title={X}}", encoding="utf-8")
    build_dir = tmp_path / "build"

    prepare_build(latex_root / "main.tex", build_dir)
    assert (build_dir / "references.bib").exists()


def test_remove_stray_book_pdfs_keeps_canonical(tmp_path) -> None:
    latex_root = tmp_path / "latex"
    build_dir = latex_root / "build"
    build_dir.mkdir(parents=True)
    keep = build_dir / "book.pdf"
    keep.write_bytes(b"%PDF-keep")
    stray = build_dir / "main.pdf"
    stray.write_bytes(b"%PDF-stray")
    (latex_root / "main.pdf").write_bytes(b"%PDF-root")

    remove_stray_book_pdfs(latex_root, build_dir, keep=keep)
    assert keep.exists()
    assert not stray.exists()
    assert not (latex_root / "main.pdf").exists()


def test_cleanup_build_artifacts_removes_temp_files(tmp_path) -> None:
    build_dir = tmp_path / "build"
    build_dir.mkdir()
    for suffix in (".aux", ".log", ".toc", ".bbl", ".pdf"):
        (build_dir / f"_book_build{suffix}").write_text("tmp", encoding="utf-8")
    (build_dir / "main_build.aux").write_text("tmp", encoding="utf-8")

    cleanup_build_artifacts(build_dir, "_book_build")
    assert not list(build_dir.glob("_book_build.*"))
    assert not list(build_dir.glob("main_build.*"))
