"""Render the agent-specified data chart with matplotlib (Python-generated)."""

from __future__ import annotations

from pathlib import Path

from bookgen.models import ChartSpec


def render_chart(spec: ChartSpec, figures_dir: Path, *, filename: str = "agent_chart.pdf") -> Path:
    """Draw the ChartSpec as a labeled bar chart and save it as a vector PDF."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    labels = [point.label for point in spec.points]
    values = [point.value for point in spec.points]

    fig, ax = plt.subplots(figsize=(7, 3.8))
    bars = ax.bar(labels, values, color="#2980b9", edgecolor="black")
    ax.bar_label(bars, fmt="%g", fontsize=8, padding=2)
    if spec.y_label:
        ax.set_ylabel(spec.y_label)
    ax.set_title(spec.title)
    ax.tick_params(axis="x", labelrotation=20)
    fig.tight_layout()

    figures_dir.mkdir(parents=True, exist_ok=True)
    target = figures_dir / filename
    fig.savefig(target, format="pdf")
    plt.close(fig)
    return target
