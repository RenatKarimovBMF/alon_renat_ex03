"""Pipeline session context shared by tools and runner."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from bookgen.shared.config import BookConfig, SetupConfig


@dataclass
class PipelineContext:
    """Mutable runtime context for one book generation session."""

    session_id: str
    setup: SetupConfig
    book: BookConfig
    project_root: Path
    session_dir: Path
    log_path: Path
    latex_root: Path
    main_tex: Path
    build_dir: Path
    artifacts: dict[str, Path] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        session_id: str,
        setup: SetupConfig,
        book: BookConfig,
        project_root: Path,
        workspace: Path | None = None,
    ) -> PipelineContext:
        """Build the session context; ``workspace`` redirects every artifact
        (LaTeX tree, session JSON, logs) into an isolated example folder so the
        canonical ``latex/`` tree stays untouched."""
        if workspace is not None:
            latex_root = workspace / "latex"
            main_tex = latex_root / "main.tex"
            build_dir = latex_root / "build"
            session_dir = workspace / "session"
            log_path = workspace / "logs" / f"crew_run_{session_id}.jsonl"
        else:
            latex_cfg = book.latex
            latex_root = project_root / "latex"
            main_tex = project_root / str(latex_cfg.get("main_file", "latex/main.tex"))
            build_dir = project_root / str(latex_cfg.get("build_dir", "latex/build"))
            session_dir = project_root / setup.session_dir / session_id
            log_path = project_root / setup.logs_dir / f"crew_run_{session_id}.jsonl"
        session_dir.mkdir(parents=True, exist_ok=True)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        return cls(
            session_id=session_id,
            setup=setup,
            book=book,
            project_root=project_root,
            session_dir=session_dir,
            log_path=log_path,
            latex_root=latex_root,
            main_tex=main_tex,
            build_dir=build_dir,
        )
