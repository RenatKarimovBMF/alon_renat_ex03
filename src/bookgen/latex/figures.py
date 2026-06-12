"""Resolve chapter images and generate the Python mission-timeline plot.

Resolution order is bundled-first: a committed copy in
``assets/chapter-figures/`` is used before any network call, so the default
pipeline (and the test suite) runs fully offline. The remote NASA URLs are only
a fallback, and the fetch function is injectable so tests never hit the network.
"""

from __future__ import annotations

import shutil
from collections.abc import Callable
from pathlib import Path

_USER_AGENT = "Mozilla/5.0 (compatible; bookgen-ex03/1.0; Haifa University educational project)"
_MIN_IMAGE_BYTES = 80_000
# Bump when chapter URLs/captions change so stale JPEGs are replaced.
_FIGURE_MANIFEST_VERSION = "moon-race-figures-v2"

FetchFn = Callable[[list[str], Path], bool]


def _sync_manifest(figures_dir: Path) -> None:
    """Drop cached chapter JPEGs when the figure manifest version changes."""
    manifest = figures_dir / ".figure_manifest"
    if manifest.exists() and manifest.read_text(encoding="utf-8").strip() == _FIGURE_MANIFEST_VERSION:
        return
    for path in figures_dir.glob("ch*.jpg"):
        path.unlink(missing_ok=True)
    manifest.write_text(f"{_FIGURE_MANIFEST_VERSION}\n", encoding="utf-8")


def _bundled_dir(latex_root: Path) -> Path:
    return latex_root.parent / "assets" / "chapter-figures"


def _is_valid_image(path: Path) -> bool:
    if not path.exists() or path.stat().st_size < _MIN_IMAGE_BYTES:
        return False
    header = path.read_bytes()[:4]
    return header[:2] == b"\xff\xd8" or header == b"\x89PNG"


def _http_fetch(urls: list[str], target: Path) -> bool:
    """Default fetcher: try each URL in turn (only used when bundled is missing)."""
    import httpx

    headers = {"User-Agent": _USER_AGENT}
    try:
        with httpx.Client(follow_redirects=True, timeout=60.0, headers=headers) as client:
            for url in urls:
                try:
                    response = client.get(url)
                except httpx.HTTPError:
                    continue
                if response.status_code == 200 and len(response.content) >= _MIN_IMAGE_BYTES:
                    target.write_bytes(response.content)
                    return True
    except httpx.HTTPError:
        return False
    return False


def ensure_figures(
    latex_root: Path,
    *,
    fetch: FetchFn | None = None,
    bundled_dir: Path | None = None,
    make_plot: bool = True,
    figures: list[tuple[str, list[str], str]] | None = None,
) -> list[Path]:
    """Ensure every chapter image exists (bundled-first) and build the plot.

    ``figures`` is the subject's (file, urls, caption) list; defaults to the
    Moon Race set so existing callers keep working.
    """
    if figures is None:
        from bookgen.crew.moon_content import CHAPTER_FIGURES

        figures = CHAPTER_FIGURES

    fetch = fetch or _http_fetch
    figures_dir = latex_root / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    _sync_manifest(figures_dir)
    bundled = bundled_dir or _bundled_dir(latex_root)
    saved: list[Path] = []

    for filename, urls, caption in figures:
        target = figures_dir / filename
        if _is_valid_image(target):
            saved.append(target)
            continue
        bundled_file = bundled / filename
        if _is_valid_image(bundled_file):
            shutil.copy2(bundled_file, target)
            saved.append(target)
            continue
        if target.exists():
            target.unlink()
        if fetch(urls, target) and _is_valid_image(target):
            saved.append(target)
            continue
        raise RuntimeError(f"Could not resolve chapter figure {filename!r} ({caption})")

    if make_plot:
        saved.append(_write_timeline_plot(figures_dir))
    return saved


def _write_timeline_plot(figures_dir: Path) -> Path:
    """Render a simple bar chart of major Moon Race milestones (Python)."""
    target = figures_dir / "mission_timeline.pdf"
    if target.exists() and target.stat().st_size > 0:
        return target

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    years = [1957, 1961, 1965, 1969, 1975]
    labels = ["Sputnik", "Gagarin", "Gemini V", "Apollo 11", "Apollo-Soyuz"]
    colors = ["#c0392b", "#c0392b", "#2980b9", "#2980b9", "#27ae60"]

    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.bar([str(y) for y in years], [1] * len(years), color=colors, edgecolor="black")
    for idx, label in enumerate(labels):
        ax.text(idx, 0.55, label, ha="center", fontsize=9, rotation=25)
    ax.set_ylim(0, 1.2)
    ax.set_ylabel("Milestone marker")
    ax.set_title("Moon Race milestones (Python / matplotlib)")
    ax.set_yticks([])
    fig.tight_layout()
    fig.savefig(target, format="pdf")
    plt.close(fig)
    return target
