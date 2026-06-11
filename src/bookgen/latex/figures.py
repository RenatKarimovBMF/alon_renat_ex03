"""Download chapter images and generate the Python mission timeline plot."""

from __future__ import annotations

from pathlib import Path

import httpx

_USER_AGENT = "bookgen-ex03/1.0 (Haifa University; educational project)"


def ensure_figures(latex_root: Path) -> list[Path]:
    """Download remote chapter images and build the matplotlib timeline chart."""
    from bookgen.crew.moon_content import CHAPTER_FIGURES

    figures_dir = latex_root / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    saved: list[Path] = []
    headers = {"User-Agent": _USER_AGENT}
    with httpx.Client(follow_redirects=True, timeout=10.0, headers=headers) as client:
        for filename, url, caption in CHAPTER_FIGURES:
            target = figures_dir / filename
            if target.exists() and target.stat().st_size > 0:
                saved.append(target)
                continue
            try:
                response = client.get(url)
                response.raise_for_status()
                target.write_bytes(response.content)
            except httpx.HTTPError:
                saved.append(_write_placeholder(figures_dir, filename, caption))
                continue
            saved.append(target)
    saved.append(_write_timeline_plot(figures_dir))
    return saved


def _write_placeholder(figures_dir: Path, filename: str, caption: str) -> Path:
    """Create a simple placeholder PNG when remote download fails."""
    target = figures_dir / filename
    if target.exists() and target.stat().st_size > 0:
        return target

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.set_facecolor("#1a1a2e")
    fig.patch.set_facecolor("#1a1a2e")
    ax.text(
        0.5,
        0.55,
        caption,
        ha="center",
        va="center",
        color="white",
        wrap=True,
        fontsize=10,
    )
    ax.text(0.5, 0.15, "Moon Race illustration (offline placeholder)", ha="center", color="#cccccc")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(target, dpi=120)
    plt.close(fig)
    return target


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
