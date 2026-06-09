"""Tests for LaTeX compiler helpers."""

from bookgen.latex.compiler import compile_latex, parse_log_errors


def test_parse_log_errors_extracts_latex_error() -> None:
    log = "Line 1\n! Undefined control sequence.\nLine 3"
    errors = parse_log_errors(log)
    assert errors == ["Undefined control sequence."]


def test_compile_missing_main_file(tmp_path) -> None:
    report = compile_latex(tmp_path / "missing.tex", build_dir=tmp_path / "build")
    assert report.success is False
    assert report.attempts == 0
