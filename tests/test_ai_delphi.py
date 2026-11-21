import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))

from ai_delphi import run_delphi


def test_delphi_counts_mentions():
    class C:
        def complete(self, system, user, **k):
            return {
                "text": "- chart-fact accuracy\n- rule fidelity",
                "output_tokens": 1,
                "input_tokens": 1,
                "latency_s": 0.0,
            }

    result = run_delphi(C(), "rubric", ["p1", "p2"], 1, "m", 100)
    assert result["items"][0]["mentions"] == 2
    assert 0.0 <= result["panel_disagreement"] <= 1.0
