"""Tests for tools/eval_runner.py — judge, anonymization, orchestration, report.

All model calls are faked. Report discipline is enforced in code: no
proportion without an interval, SE printed before scoring.
"""

import json
import os
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))


class FakeJudgeClient:
    """Returns queued judge JSON; records prompts for anonymization checks."""

    def __init__(self, payloads, tokens=50):
        self.payloads = list(payloads)
        self.tokens = tokens
        self.calls = []

    def complete(self, system, user, model, temperature, max_tokens, seed=7, reasoning=None):
        self.calls.append({"system": system, "user": user, "model": model})
        payload = self.payloads.pop(0) if self.payloads else _judge_json("pass")
        return {
            "text": payload,
            "output_tokens": self.tokens,
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


def chart():
    return {
        "lagna": {"sign": "Aries", "degree": 10.0},
        "planets": {"Sun": {"sign": "Aries", "degree": 10.5, "house": 1, "dignity": "neutral"}},
    }


ITEM = {"id": "g-01", "prompt": "How is my career?"}
LEDGER = {"clauses": [{"text": "cite the 10th lord", "mechanical": True}], "required_grounds": ["10th lord"]}


class TestJudge(unittest.TestCase):
    def test_judge_prompt_is_anonymized(self):
        from eval_runner import judge_response

        client = FakeJudgeClient([_judge_json("pass")])
        response = "Answer (with arm): the 10th lord is strong."
        judge_response(
            client, ITEM, LEDGER, chart(), response, judge_model="meta/muse-spark-1.3-contributor"
        )
        joined = client.calls[0]["system"] + client.calls[0]["user"]
        for banned in ("bare", "without", "with-arm", "with_arm", "arm"):
            self.assertNotIn(banned, joined.lower())

    def test_judge_parse_failure_retries_then_marks_error(self):
        from eval_runner import judge_response

        client = FakeJudgeClient(["not json at all", "still not json"])
        result = judge_response(
            client, ITEM, LEDGER, chart(), "the 10th lord is strong.",
            judge_model="meta/muse-spark-1.3-contributor",
        )
        self.assertTrue(result["judge_error"])
        self.assertEqual(len(client.calls), 2)

    def test_judge_fail_returns_pass_false(self):
        from eval_runner import judge_response

        client = FakeJudgeClient([_judge_json("fail")])
        result = judge_response(
            client, ITEM, LEDGER, chart(), "answer", judge_model="m"
        )
        self.assertFalse(result["pass"])
        self.assertFalse(result["judge_error"])


class TestAnonymize(unittest.TestCase):
    def test_anonymize_strips_arm_labels(self):
        from eval_runner import anonymize

        text = "Answer (with arm): The 10th lord is Saturn."
        out = anonymize(text)
        self.assertNotIn("with arm", out.lower())
        self.assertIn("10th lord", out)


class TestReport(unittest.TestCase):
    def test_report_requires_intervals(self):
        from eval_runner import write_report

        results = {
            "items": [],
            "arms": {"with": {"proportion": 0.8}},  # no interval -> must raise
            "se": 0.098,
            "gate": 0.098,
        }
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(AssertionError):
                write_report(results, tmp)

    def test_se_printed_before_scoring_in_report(self):
        from eval_runner import write_report

        results = {
            "items": [],
            "arms": {
                "with": {"passes": 15, "n": 20, "proportion": 0.75, "interval": [0.53, 0.89]},
                "without": {"passes": 10, "n": 20, "proportion": 0.5, "interval": [0.30, 0.70]},
            },
            "se": 0.098058,
            "gate": "delta > 0.098058",
            "delta": {"value": 0.25, "interval": [0.0, 0.5]},
        }
        with tempfile.TemporaryDirectory() as tmp:
            write_report(results, tmp)
            report = open(os.path.join(tmp, "report.md"), encoding="utf-8").read()
        self.assertIn("SE", report)
        self.assertIn("0.098", report)
        self.assertIn("[0.53, 0.89]", report)
        self.assertNotIn("beats", report.lower())
        self.assertNotIn("wins", report.lower())

    def test_results_json_schema(self):
        from eval_runner import write_report

        results = {
            "items": [{"id": "g-01", "arms": {}}],
            "arms": {
                "bare": {"passes": 1, "n": 1, "proportion": 1.0, "interval": [0.2, 1.0]},
            },
            "se": 0.5,
            "gate": "delta > 0.5",
            "delta": {"value": 0.0, "interval": [0.0, 0.0]},
        }
        with tempfile.TemporaryDirectory() as tmp:
            write_report(results, tmp)
            payload = json.load(open(os.path.join(tmp, "results.json"), encoding="utf-8"))
        self.assertIn("items", payload)
        self.assertIn("arms", payload)
        self.assertIn("se", payload)
        self.assertIn("gate", payload)


class TestRunOrchestration(unittest.TestCase):
    def test_judge_error_excluded_from_both_arms(self):
        from eval_runner import tally

        items = [
            {"id": "g-01", "arms": {
                "with": {"judge_error": True, "pass": True},
                "without": {"judge_error": True, "pass": False},
            }},
            {"id": "g-02", "arms": {
                "with": {"judge_error": False, "pass": True},
                "without": {"judge_error": False, "pass": False},
            }},
        ]
        out = tally(items, arms=["with", "without"])
        self.assertEqual(out["with"]["n"], 1)
        self.assertEqual(out["with"]["passes"], 1)
        self.assertEqual(out["excluded"], ["g-01"])

    def test_arm_disqualified_for_run_on_budget_overrun(self):
        from eval_runner import tally

        items = [
            {"id": "g-01", "arms": {"with": {"disqualified": True}, "without": {"pass": True}}},
        ]
        out = tally(items, arms=["with", "without"])
        self.assertTrue(out["with"]["disqualified"])
        self.assertNotIn("proportion", out["with"])


class TestPartialPersistence(unittest.TestCase):
    def test_partial_written_atomically_after_each_item(self):
        from eval_runner import _write_partial

        items = [{"id": "g-01", "arms": {"with": {"pass": True}}}]
        with tempfile.TemporaryDirectory() as tmp:
            _write_partial(tmp, items, total=26, done=1)
            path = os.path.join(tmp, "partial.json")
            payload = json.load(open(path, encoding="utf-8"))
            self.assertEqual(payload["done"], 1)
            self.assertEqual(payload["total"], 26)
            self.assertEqual(payload["items"], items)
            self.assertFalse(os.path.exists(path + ".tmp"))

class TestModelResolution(unittest.TestCase):
    def test_overrides_win_over_transport_defaults(self):
        from eval_runner import _resolve_models

        self.assertEqual(
            _resolve_models("opencode-go"),
            ("deepseek-v4.1-flash", "muse-spark-1.3-contributor"),
        )
        self.assertEqual(
            _resolve_models("opencode-go", "glm-5.3-flash", "deepseek-v4.1-flash"),
            ("glm-5.3-flash", "deepseek-v4.1-flash"),
        )

class TestVerdictReport(unittest.TestCase):
    def _results(self, delta_value):
        return {
            "mode": "verdict",
            "items": [],
            "arms": {
                "without": {"passes": 3, "n": 26, "proportion": 0.115, "interval": [0.04, 0.29]},
                "with": {"passes": 3, "n": 26, "proportion": 0.115, "interval": [0.04, 0.29]},
            },
            "se": 0.098058,
            "gate": "delta > 0.098058",
            "delta": {"value": delta_value, "interval": [-0.25, 0.25]},
        }

    def test_verdict_report_not_cleared(self):
        from eval_runner import write_report

        with tempfile.TemporaryDirectory() as tmp:
            write_report(self._results(0.0), tmp)
            text = open(os.path.join(tmp, "report.md"), encoding="utf-8").read()
            payload = json.load(open(os.path.join(tmp, "results.json"), encoding="utf-8"))
        self.assertIn("Gate read: **NOT CLEARED**", text)
        self.assertNotIn("no verdict is taken", text.lower())
        self.assertFalse(payload["gate_cleared"])

    def test_verdict_report_cleared(self):
        from eval_runner import write_report

        with tempfile.TemporaryDirectory() as tmp:
            write_report(self._results(0.15), tmp)
            text = open(os.path.join(tmp, "report.md"), encoding="utf-8").read()
        self.assertIn("Gate read: **CLEARED**", text)
        self.assertNotIn("NOT CLEARED", text)



class TestAnonymizePreservesGrounds(unittest.TestCase):
    def test_ground_parenthetical_preserved(self):
        from eval_runner import anonymize

        text = "Saturn (with Saturn exalted) supports steady work."
        self.assertIn("(with Saturn exalted)", anonymize(text))


class TestLockedGate(unittest.TestCase):
    def test_verdict_refuses_subset(self):
        from eval_runner import _assert_verdict_ready

        with self.assertRaises(ValueError):
            _assert_verdict_ready([{"id": "g-01"}])

    def test_verdict_accepts_full_corpus(self):
        from eval_runner import _assert_verdict_ready

        _assert_verdict_ready([{"id": f"x-{i}"} for i in range(26)])


class TestPairedDelta(unittest.TestCase):
    def _items(self, pairs):
        return [
            {"id": f"i{i}", "arms": {"with": {"pass": w}, "without": {"pass": o}}}
            for i, (w, o) in enumerate(pairs)
        ]

    def test_perfect_separation_interval_positive(self):
        from eval_runner import _paired_delta_interval

        low, high = _paired_delta_interval(
            self._items([(True, False)] * 10), ["with", "without"]
        )
        self.assertGreater(low, 0.0)

    def test_identical_arms_include_zero(self):
        from eval_runner import _paired_delta_interval

        low, high = _paired_delta_interval(
            self._items([(True, True), (False, False)] * 5), ["with", "without"]
        )
        self.assertLessEqual(low, 0.0)
        self.assertGreaterEqual(high, 0.0)


class TestInvalidVerdictReport(unittest.TestCase):
    def test_exclusions_mark_verdict_invalid(self):
        from eval_runner import write_report

        results = {
            "mode": "verdict",
            "valid": False,
            "excluded": ["g-01"],
            "items": [],
            "arms": {
                "with": {"passes": 3, "n": 25, "proportion": 0.12, "interval": [0.04, 0.3]},
                "without": {"passes": 3, "n": 25, "proportion": 0.12, "interval": [0.04, 0.3]},
            },
            "se": 0.098058,
            "gate": "delta > 0.098058",
            "delta": {"value": 0.0, "interval": [-0.25, 0.25]},
        }
        with tempfile.TemporaryDirectory() as tmp:
            write_report(results, tmp)
            text = open(os.path.join(tmp, "report.md"), encoding="utf-8").read()
        self.assertIn("INVALID", text)
        self.assertNotIn("Gate read: **CLEARED**", text)


class TestManifest(unittest.TestCase):
    def test_manifest_written(self):
        from eval_runner import _write_manifest

        results = {
            "mode": "pilot",
            "models": {"transport": "opencode-go", "arm": "glm-5.3-flash", "judge": "deepseek-v4.1-flash"},
            "budget": 12000,
            "engines": {"dashaflow_version": "1.5.1"},
        }
        with tempfile.TemporaryDirectory() as tmp:
            _write_manifest(tmp, results, ["g-01", "s-01"])
            payload = json.load(open(os.path.join(tmp, "manifest.json"), encoding="utf-8"))
        self.assertEqual(payload["item_ids"], ["g-01", "s-01"])
        self.assertIn("repo_commit", payload)
        self.assertIn("prompt_hashes", payload)


class TestTransitContext(unittest.TestCase):
    def test_transit_attached_when_date_present(self):
        from unittest.mock import patch

        import eval_runner

        item = {
            "birth": {"dob": "1984-01-19", "time": "08:30", "lat": 8.5, "lon": 76.9, "tz": "Asia/Kolkata"},
            "transit_date": "2026-11-09",
        }
        with patch("dashaflow.cast_chart", return_value={"planets": {}}), \
             patch("dashaflow.cast_transit", return_value={"sade_sati": {"active": True}}) as transit:
            chart = eval_runner.precompute_chart(item)
        self.assertEqual(chart["transit"], {"sade_sati": {"active": True}})
        transit.assert_called_once()

    def test_no_transit_without_date(self):
        from unittest.mock import patch

        import eval_runner

        item = {"birth": {"dob": "1984-01-19", "time": "08:30", "lat": 8.5, "lon": 76.9, "tz": "Asia/Kolkata"}}
        with patch("dashaflow.cast_chart", return_value={"planets": {}}):
            chart = eval_runner.precompute_chart(item)
        self.assertNotIn("transit", chart)


if __name__ == "__main__":
    unittest.main()
