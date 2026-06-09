"""Integration test for demo pipeline."""

from pathlib import Path

from bookgen.crew.runner import PipelineMode
from bookgen.sdk.sdk import BookGenSdk
from bookgen.shared.config import load_book_config, load_rate_limits_config, load_setup_config
from bookgen.shared.gatekeeper import ApiGatekeeper

ROOT = Path(__file__).resolve().parents[2]


def test_demo_pipeline_writes_session_artifacts() -> None:
    setup = load_setup_config(ROOT / "config" / "setup.json")
    book = load_book_config(ROOT / "config" / "book.json")
    limits = load_rate_limits_config(ROOT / "config" / "rate_limits.json")
    sdk = BookGenSdk(book, ApiGatekeeper(limits), project_root=ROOT)
    result = sdk.run_pipeline(setup, mode=PipelineMode.DEMO)

    assert (result.session_dir / "01_research.json").exists()
    assert (result.session_dir / "02_outline.json").exists()
    assert (result.session_dir / "03_sections.json").exists()
    assert (result.session_dir / "05_review.json").exists()
    assert (result.session_dir / "06_build.json").exists()
    assert result.cost_report_path.exists()
