"""Download chapter images and generate the Python mission timeline plot."""

from __future__ import annotations

import shutil
from pathlib import Path

import httpx

_USER_AGENT = "Mozilla/5.0 (compatible; bookgen-ex03/1.0; Haifa University educational project)"
_MIN_IMAGE_BYTES = 80_000


def _bundled_dir(latex_root: Path) -> Path:
    return latex_root.parent / "assets" / "chapter-figures"


def _is_valid_image(path: Path) -> bool:
    if not path.exists() or path.stat().st_size < _MIN_IMAGE_BYTES:
        return False
    header = path.read_bytes()[:4]
    return header[:2] == b"\xff\xd8" or header == b"\x89PNG"


def _download_image(client: httpx.Client, urls: list[str], target: Path) -> bool:
    for url in urls:
        try:
            response = client.get(url)
            if response.status_code == 200 and len(response.content) >= _MIN_IMAGE_BYTES:
                target.write_bytes(response.content)
                return True
        except httpx.HTTPError:
            continue
    return False


def ensure_figures(latex_root: Path) -> list[Path]:
    """Download remote chapter images and build the matplotlib timeline chart."""
    from bookgen.crew.moon_content import CHAPTER_FIGURES

    figures_dir = latex_root / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    bundled = _bundled_dir(latex_root)
    saved: list[Path] = []
    headers = {"User-Agent": _USER_AGENT}

    with httpx.Client(follow_redirects=True, timeout=60.0, headers=headers) as client:
        for filename, urls, caption in CHAPTER_FIGURES:
            target = figures_dir / filename
            if _is_valid_image(target):
                saved.append(target)
                continue

            if target.exists():
                target.unlink()

            if _download_image(client, urls, target):
                saved.append(target)
                continue

            bundled_file = bundled / filename
            if _is_valid_image(bundled_file):
                shutil.copy2(bundled_file, target)
                saved.append(target)
                continue

            msg = f"Could not download chapter figure {filename!r} ({caption})"
            raise RuntimeError(msg)

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
