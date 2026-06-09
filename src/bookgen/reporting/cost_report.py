"""Summarize LLM cost logs into markdown tables."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CostRow:
    agent_key: str
    model: str
    input_tokens: int
    output_tokens: int
    estimated_usd: float
    calls: int = 1


@dataclass
class CostSummary:
    rows: list[CostRow] = field(default_factory=list)
    total_usd: float = 0.0
    total_input_tokens: int = 0
    total_output_tokens: int = 0

    def add(self, row: CostRow) -> None:
        self.rows.append(row)
        self.total_usd += row.estimated_usd
        self.total_input_tokens += row.input_tokens
        self.total_output_tokens += row.output_tokens


def load_cost_summary(log_path: Path) -> CostSummary:
    """Aggregate llm_call events from a JSONL crew log."""
    summary = CostSummary()
    if not log_path.exists():
        return summary

    buckets: dict[tuple[str, str], CostRow] = {}
    for line in log_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        payload = json.loads(line)
        if payload.get("event") != "llm_call":
            continue
        key = (str(payload["agent_key"]), str(payload["model"]))
        row = buckets.get(key)
        if row is None:
            row = CostRow(
                agent_key=key[0],
                model=key[1],
                input_tokens=int(payload.get("input_tokens", 0)),
                output_tokens=int(payload.get("output_tokens", 0)),
                estimated_usd=float(payload.get("estimated_usd", 0.0)),
            )
            buckets[key] = row
        else:
            row.calls += 1
            row.input_tokens += int(payload.get("input_tokens", 0))
            row.output_tokens += int(payload.get("output_tokens", 0))
            row.estimated_usd += float(payload.get("estimated_usd", 0.0))

    for row in buckets.values():
        summary.add(row)
    return summary


def render_cost_markdown(summary: CostSummary, *, mode: str) -> str:
    """Render Guidelines-style API cost table."""
    lines = [
        "# API Cost Breakdown",
        "",
        f"**Run mode:** `{mode}`",
        "",
        "| Agent | Model | Calls | Input tokens | Output tokens | Est. USD |",
        "|-------|-------|------:|-------------:|--------------:|---------:|",
    ]
    if not summary.rows:
        lines.append("| _none_ | fixture/offline | 0 | 0 | 0 | 0.00 |")
    else:
        for row in sorted(summary.rows, key=lambda item: item.agent_key):
            lines.append(
                f"| {row.agent_key} | {row.model} | {row.calls} | "
                f"{row.input_tokens:,} | {row.output_tokens:,} | "
                f"${row.estimated_usd:.4f} |"
            )
    lines.extend(
        [
            "",
            f"**Total:** ${summary.total_usd:.4f} · "
            f"{summary.total_input_tokens:,} input · "
            f"{summary.total_output_tokens:,} output tokens",
            "",
        ]
    )
    return "\n".join(lines)


def write_cost_report(log_path: Path, output_path: Path, *, mode: str) -> CostSummary:
    """Write COST markdown from a session log."""
    summary = load_cost_summary(log_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_cost_markdown(summary, mode=mode), encoding="utf-8")
    return summary
