"""Tests for cost report aggregation."""

from pathlib import Path

from bookgen.reporting.cost_report import load_cost_summary, write_cost_report


def test_cost_summary_aggregates_jsonl(tmp_path: Path) -> None:
    log_path = tmp_path / "crew.jsonl"
    log_path.write_text(
        "\n".join(
            [
                '{"event":"llm_call","agent_key":"writer","model":"mock-model",'
                '"input_tokens":100,"output_tokens":50,"estimated_usd":0.01}',
                '{"event":"llm_call","agent_key":"writer","model":"mock-model",'
                '"input_tokens":200,"output_tokens":80,"estimated_usd":0.02}',
            ]
        ),
        encoding="utf-8",
    )
    summary = load_cost_summary(log_path)
    assert summary.total_input_tokens == 300
    assert summary.total_output_tokens == 130
    assert summary.total_usd == 0.03

    out = tmp_path / "COST.md"
    write_cost_report(log_path, out, mode="live")
    assert "writer" in out.read_text(encoding="utf-8")
