"""Tests for configuration loading."""

from pathlib import Path

from bookgen.shared.config import load_book_config, load_rate_limits_config, load_setup_config

ROOT = Path(__file__).resolve().parents[2]


def test_load_setup_config() -> None:
    cfg = load_setup_config(ROOT / "config" / "setup.json")
    assert cfg.version == "1.00"
    assert cfg.project_name == "crewai-latex-book"


def test_load_book_config() -> None:
    cfg = load_book_config(ROOT / "config" / "book.json")
    assert cfg.target_pages == 15
    assert "Moon Race" in cfg.topic


def test_load_rate_limits_config() -> None:
    cfg = load_rate_limits_config(ROOT / "config" / "rate_limits.json")
    assert cfg.max_total_requests == 50
