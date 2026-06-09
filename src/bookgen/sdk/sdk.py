"""Single SDK entry point for pipeline operations."""

from __future__ import annotations

from pathlib import Path

from bookgen.crew.runner import PipelineMode, PipelineResult, run_book_pipeline
from bookgen.latex.compiler import compile_latex
from bookgen.models import BuildReport
from bookgen.sdk.llm_client import LlmClient
from bookgen.shared.config import BookConfig, SetupConfig
from bookgen.shared.gatekeeper import ApiGatekeeper


class BookGenSdk:
    """Facade used by CLI and CrewAI integration."""

    def __init__(
        self,
        book: BookConfig,
        gatekeeper: ApiGatekeeper,
        *,
        llm: LlmClient | None = None,
        project_root: Path | None = None,
    ) -> None:
        self._book = book
        self._gatekeeper = gatekeeper
        self._llm = llm or LlmClient(gatekeeper)
        self._project_root = project_root or Path.cwd()

    @property
    def llm(self) -> LlmClient:
        return self._llm

    @property
    def gatekeeper(self) -> ApiGatekeeper:
        return self._gatekeeper

    @property
    def project_root(self) -> Path:
        return self._project_root

    def compile_pdf(self) -> BuildReport:
        """Compile the configured LaTeX main file."""
        latex_cfg = self._book.latex
        main_file = self._project_root / str(latex_cfg.get("main_file", "latex/main.tex"))
        build_dir = self._project_root / str(latex_cfg.get("build_dir", "latex/build"))
        attempts = int(latex_cfg.get("max_compile_attempts", 3))
        return compile_latex(main_file, build_dir=build_dir, max_attempts=attempts)

    def run_pipeline(
        self,
        setup: SetupConfig,
        *,
        mode: PipelineMode = PipelineMode.PRODUCTION,
    ) -> PipelineResult:
        """Run the full CrewAI book pipeline."""
        return run_book_pipeline(
            setup=setup,
            book=self._book,
            gatekeeper=self._gatekeeper,
            compile_pdf=self.compile_pdf,
            project_root=self._project_root,
            mode=mode,
        )
