"""CLI entry point for the book generation pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path

from dotenv import load_dotenv

from bookgen.crew.runner import PipelineMode
from bookgen.latex.workspace import example_workspace
from bookgen.reporting.page_metrics import count_pdf_pages
from bookgen.sdk.sdk import BookGenSdk
from bookgen.shared.config import load_book_config, load_rate_limits_config, load_setup_config
from bookgen.shared.gatekeeper import ApiGatekeeper


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate a LaTeX book using a CrewAI agent pipeline.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/book.json"),
        help="Path to book.json",
    )
    parser.add_argument(
        "--setup",
        type=Path,
        default=Path("config/setup.json"),
        help="Path to setup.json",
    )
    parser.add_argument(
        "--rate-limits",
        type=Path,
        default=Path("config/rate_limits.json"),
        help="Path to rate_limits.json",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Project root directory",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Validate config only")
    mode.add_argument("--demo", action="store_true", help="Short 2-chapter smoke test")
    mode.add_argument(
        "--live",
        action="store_true",
        help="Run live CrewAI crew (uses API keys, costs money)",
    )
    parser.add_argument(
        "--compile-only",
        action="store_true",
        help="Compile existing LaTeX without running the crew",
    )
    return parser


def _resolve_mode(args: argparse.Namespace) -> PipelineMode:
    if args.demo:
        return PipelineMode.DEMO
    if args.live:
        return PipelineMode.LIVE
    return PipelineMode.PRODUCTION


def main() -> int:
    """Run the CLI."""
    load_dotenv()  # populate API keys from .env for --live runs (no-op if absent)
    args = build_parser().parse_args()
    setup = load_setup_config(args.project_root / args.setup)
    book = load_book_config(args.project_root / args.config)
    limits = load_rate_limits_config(args.project_root / args.rate_limits)

    print(f"Project: {setup.project_name} v{setup.version}")
    print(f"Topic:   {book.topic}")
    print(f"Target:  {book.target_pages} pages (+/- {book.page_tolerance})")
    print(f"Budget:  {limits.max_total_requests} total LLM calls")

    if args.dry_run:
        print("Dry run OK — configs valid.")
        return 0

    sdk = BookGenSdk(
        book,
        ApiGatekeeper(limits),
        project_root=args.project_root,
    )

    if args.compile_only:
        report = sdk.compile_pdf()
        if report.success:
            pages = count_pdf_pages(Path(report.pdf_path)) if report.pdf_path else None
            print(f"PDF built: {report.pdf_path}")
            if pages is not None:
                print(f"Pages:     {pages}")
            return 0
        print("LaTeX build failed:")
        for err in report.errors:
            print(f"  - {err}")
        return 1

    mode = _resolve_mode(args)
    print(f"Mode:    {mode.value}")
    workspace = None
    if mode is PipelineMode.LIVE:
        # Each live run becomes a self-contained example folder; the canonical
        # latex/ tree (the graded artifact) is never touched or locked.
        workspace = example_workspace(args.project_root, book.topic)
        print(f"Example: {workspace}")
    result = sdk.run_pipeline(setup, mode=mode, workspace=workspace)

    print(f"Session:  {result.session_id}")
    print(f"Artifacts: {result.session_dir}")
    print(f"Log:       {result.log_path}")
    print(f"Cost:      {result.cost_report_path} (+ docs/COST.md)")
    print(f"Review:    approved={result.review.approved}, pages~={result.review.estimated_pages}")

    if result.build.success:
        pages = count_pdf_pages(Path(result.build.pdf_path)) if result.build.pdf_path else None
        print(f"PDF built: {result.build.pdf_path}")
        if pages is not None:
            print(f"Pages:     {pages}")
        return 0

    print("LaTeX build failed:")
    for err in result.build.errors:
        print(f"  - {err}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
