import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))

from zero_human_screen import chart_text_divergence, judge_consistency, shift_birth

LEDGER = {"clauses": [{"text": "cite the 10th lord", "mechanical": True}], "required_grounds": ["10th lord"]}
CHART = {"lagna": {"sign": "Aries", "degree": 10.0}}


class FakeJudgeClient:
    def __init__(self, payloads):
        self.payloads = list(payloads)
        self.calls = []

    def complete(self, system, user, model, temperature, max_tokens, seed=7, reasoning=None):
        self.calls.append(model)
        return {
            "text": self.payloads.pop(0),
            "output_tokens": 50,
            "input_tokens": 100,
            "latency_s": 0.01,
        }


def _judge_json(overall):
    return json.dumps(
        {
            "clauses": [
                {"clause": "cite the 10th lord", "verdict": "pass", "evidence": "10th lord", "reason": "cited"}
            ],
            "overall": overall,
        }
    )


def test_a1_flags_fabricated_degree():
    chart = {"planets": {"Sun": {"degree": 10.0}}}
    result = chart_text_divergence("The Sun is at 99.99°.", "The Sun is at 10.0°.", chart)
    assert result["real_fabrications"] == ["99.99°"]


def test_a2_fails_identical_texts():
    chart = {"planets": {"Sun": {"degree": 10.0}}}
    text = "The Sun is at 10.0°."
    result = chart_text_divergence(text, text, chart)
    assert result["claim_overlap"] == 1.0
    assert result["pass"] is False


def test_a2_passes_when_decoy_diverges():
    chart = {"planets": {"Sun": {"degree": 10.0}}}
    result = chart_text_divergence(
        "The Sun is at 10.0°.", "The Sun is at 22.0° and the Moon is at 5.0°.", chart
    )
    assert result["pass"] is True


def test_shift_birth_changes_time():
    assert (
        shift_birth(
            {"dob": "2000-01-01", "time": "04:20", "lat": 0, "lon": 0, "tz": "UTC"}
        )["time"]
        == "16:20"
    )


def test_judge_consistency_perfect():
    client = FakeJudgeClient([_judge_json("pass")] * 12)
    result = judge_consistency(
        client, {"id": "x", "prompt": "q"}, LEDGER, CHART, "answer", ["m1", "m2"], 3
    )
    assert result["pairwise_agreement"] == 1.0
    assert result["judge_errors"] == 0
    assert result["pass"] is True


def test_judge_consistency_flags_split():
    client = FakeJudgeClient([_judge_json("pass"), _judge_json("fail")] * 6)
    result = judge_consistency(
        client, {"id": "x", "prompt": "q"}, LEDGER, CHART, "answer", ["m1", "m2"], 3
    )
    assert result["pairwise_agreement"] < 0.8
    assert result["pass"] is False


def test_report_keeps_boundary_and_never_says_validated(tmp_path):
    from zero_human_screen import write_report

    write_report(
        {"items": [], "summary": {"a1": [0, 0], "a2": [0, 0], "a4": [0, 0]}},
        str(tmp_path),
    )
    text = (tmp_path / "report.md").read_text()
    assert "not validated against expert judgment" in text
    assert "validated" not in text.lower().replace("not validated", "")


def test_a2_fails_when_decoy_makes_no_claims():
    chart = {"planets": {"Sun": {"degree": 10.0}}}
    result = chart_text_divergence("The Sun is at 10.0°.", "Career will be good.", chart)
    assert result["pass"] is False


def test_a2_fails_when_decoy_contradicts_its_own_chart():
    real_chart = {"planets": {"Sun": {"degree": 10.0}}}
    decoy_chart = {"planets": {"Mars": {"degree": 40.0}}}
    result = chart_text_divergence(
        "The Sun is at 10.0°.", "Mars is at 99.0°.", real_chart, decoy_chart
    )
    assert result["pass"] is False


def test_a2_passes_when_decoy_fits_its_own_chart():
    real_chart = {"planets": {"Sun": {"degree": 10.0}}}
    decoy_chart = {"planets": {"Mars": {"degree": 40.0}}}
    result = chart_text_divergence(
        "The Sun is at 10.0°.", "Mars is at 40.0°.", real_chart, decoy_chart
    )
    assert result["pass"] is True


def test_cast_decoy_keeps_transit():
    import zero_human_screen as zhs

    item = {
        "birth": {
            "dob": "1953-12-17",
            "time": "19:13",
            "lat": 34.052,
            "lon": -118.243,
            "tz": "UTC",
        },
        "transit_date": "2026-01-01",
    }
    assert "transit" in zhs.cast_decoy(item)


LEDGER2 = {
    "clauses": [
        {"text": "cite the 10th lord", "mechanical": True},
        {"text": "cite the dasha", "mechanical": True},
    ],
    "required_grounds": [],
}


def _judge_json2(overall, verdicts):
    clauses = ["cite the 10th lord", "cite the dasha"]
    return json.dumps(
        {
            "clauses": [
                {"clause": text, "verdict": verdict, "evidence": "", "reason": ""}
                for text, verdict in zip(clauses, verdicts)
            ],
            "overall": overall,
        }
    )


def test_judge_consistency_reports_clause_agreement():
    client = FakeJudgeClient(
        [_judge_json2("fail", ["fail", "pass"]), _judge_json2("fail", ["pass", "fail"])]
    )
    result = judge_consistency(
        client, {"id": "x", "prompt": "q"}, LEDGER2, CHART, "answer", ["m1"], 2
    )
    assert result["pairwise_agreement"] == 1.0
    assert result["clause_agreement"] == 0.0


def test_report_records_provenance(tmp_path):
    from zero_human_screen import write_report

    write_report(
        {
            "items": [],
            "summary": {"a1": [0, 0], "a2": [0, 0], "a4": [0, 0], "tokens": 123},
            "config": {
                "transport": "opencode-go",
                "arm_model": "arm-x",
                "judge_models": ["judge-y", "judge-z"],
                "trials": 3,
                "budget": 700,
                "items": "grounding.jsonl",
                "generated_at": "2026-11-20T00:00:00Z",
            },
        },
        str(tmp_path),
    )
    text = (tmp_path / "report.md").read_text()
    assert "opencode-go" in text
    assert "arm-x" in text
    assert "judge-y" in text and "judge-z" in text
    assert "123" in text


def test_screen_item_marks_zero_claim_a1_not_exercised():
    import zero_human_screen as zhs

    class Fake:
        def complete(self, *a, **k):
            return {
                "text": "Career will be good.",
                "output_tokens": 1,
                "input_tokens": 1,
                "latency_s": 0.0,
            }

    item = {
        "id": "x",
        "prompt": "q",
        "birth": {
            "dob": "1953-12-17",
            "time": "19:13",
            "lat": 34.052,
            "lon": -118.243,
            "tz": "UTC",
        },
    }
    result = zhs.screen_item(item, {"clauses": [], "required_grounds": []}, Fake(), "doctrine", "m", 100)
    assert result["a1"]["claims_checked"] == 0
    assert result["a1"]["pass"] is False
    assert result["a1"]["exercised"] is False


def test_main_offline_uses_ledger_items(tmp_path, monkeypatch):
    import zero_human_screen as zhs

    class FakeClient:
        def __init__(self, *a, **k):
            pass

        def complete(self, *a, **k):
            return {
                "text": "Career will be good.",
                "output_tokens": 1,
                "input_tokens": 1,
                "latency_s": 0.0,
            }

    monkeypatch.setattr(zhs, "ChatClient", FakeClient)
    assert zhs.main(["--limit", "1", "--out", str(tmp_path)]) == 0
    report = (tmp_path / "report.md").read_text()
    assert "A1 chart-fact" in report
