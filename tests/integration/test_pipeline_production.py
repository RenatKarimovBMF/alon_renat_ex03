"""Integration test for production pipeline."""

from pathlib import Path

from bookgen.crew.runner import PipelineMode
from bookgen.reporting.page_metrics import count_pdf_pages, count_words_in_text
from bookgen.sdk.sdk import BookGenSdk
from bookgen.shared.config import load_book_config, load_rate_limits_config, load_setup_config
from bookgen.shared.gatekeeper import ApiGatekeeper

ROOT = Path(__file__).resolve().parents[2]


def test_production_pipeline_writes_artifacts_and_cost() -> None:
    setup = load_setup_config(ROOT / "config" / "setup.json")
    book = load_book_config(ROOT / "config" / "book.json")
    limits = load_rate_limits_config(ROOT / "config" / "rate_limits.json")
    sdk = BookGenSdk(book, ApiGatekeeper(limits), project_root=ROOT)
    result = sdk.run_pipeline(setup, mode=PipelineMode.PRODUCTION)

    assert result.mode is PipelineMode.PRODUCTION
    assert (result.session_dir / "01_research.json").exists()
    assert (result.session_dir / "03_sections.json").exists()
    assert result.cost_report_path.exists()
    assert (ROOT / "docs" / "COST.md").exists()

    sections_text = (result.session_dir / "03_sections.json").read_text(encoding="utf-8")
    assert count_words_in_text(sections_text) > 1000

    if result.build.success and result.build.pdf_path:
        pages = count_pdf_pages(Path(result.build.pdf_path))
        if pages is not None:
            assert pages >= 10
