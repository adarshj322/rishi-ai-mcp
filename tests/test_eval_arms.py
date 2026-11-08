"""Tests for tools/eval_arms.py — model client and the without arm.

No network: a FakeClient stands in for the OpenRouter client and records
every call, so budget accounting and selection logic are tested directly.
"""

import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))


def chart_with(planets):
    return {
        "lagna": {"sign": "Aries", "degree": 10.0},
        "planets": {
            name: {"sign": "Aries", "degree": deg, "house": 1, "dignity": "neutral"}
            for name, deg in planets.items()
        },
        "dashas": {"maha": {"lord": "Jupiter"}, "antar": {"lord": "Saturn"}},
    }


class FakeClient:
    """Records calls; returns queued texts in order; reports output tokens."""

    def __init__(self, texts, tokens_per_call=100):
        self.texts = list(texts)
        self.tokens_per_call = tokens_per_call
        self.calls = []

    def complete(self, system, user, model, temperature, max_tokens, seed=7, reasoning=None):
        self.calls.append(
            {
                "system": system,
                "user": user,
                "model": model,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "seed": seed,
            }
        )
        text = self.texts.pop(0) if self.texts else "The 10th lord is strong."
        return {
            "text": text,
            "output_tokens": self.tokens_per_call,
            "input_tokens": 1000,
            "latency_s": 0.01,
        }


ITEM = {
    "id": "g-01",
    "prompt": "How is my career?",
    "birth": {"dob": "1975-03-10", "time": "05:40", "lat": 28.6, "lon": 77.2, "tz": "Asia/Kolkata"},
}

LEDGER = {
    "clauses": [{"text": "cite the 10th lord", "mechanical": True}],
    "required_grounds": ["10th lord"],
}


class TestWithoutArm(unittest.TestCase):
    def test_without_samples_three_and_selects_best(self):
        from eval_arms import run_without

        client = FakeClient(
            [
                "Your career is great.",                       # no ground
                "The 10th lord is Saturn; career is steady.",   # has ground
                "Career will shine brightly.",                  # no ground
            ]
        )
        result = run_without(
            client, ITEM, chart_with({"Sun": 10.5}), LEDGER, budget=3000,
            doctrine_prompt="DOCTRINE",
        )
        self.assertEqual(len(client.calls), 3)
        self.assertEqual(result["samples"], 3)
        self.assertIn("10th lord", result["text"])
        self.assertFalse(result["disqualified"])
        for call in client.calls:
            self.assertEqual(call["temperature"], 0.7)
            self.assertEqual(call["max_tokens"], 1000)
            self.assertEqual(call["system"], "DOCTRINE")

    def test_without_disqualified_when_total_exceeds_budget(self):
        from eval_arms import run_without

        client = FakeClient(["a", "b", "c"], tokens_per_call=1200)
        from eval_arms import BudgetExceeded

        with self.assertRaises(BudgetExceeded):
            run_without(
                client, ITEM, chart_with({"Sun": 10.5}), LEDGER, budget=3000,
                doctrine_prompt="DOCTRINE",
            )

    def test_without_discards_fabricating_sample(self):
        from eval_arms import run_without

        client = FakeClient(
            [
                "The 10th lord is strong. Sun at 29° in Aries.",  # fabricated degree + ground
                "The 10th lord is Saturn.",                        # clean
                "Career is bright.",
            ]
        )
        result = run_without(
            client, ITEM, chart_with({"Sun": 10.5}), LEDGER, budget=3000,
            doctrine_prompt="DOCTRINE",
        )
        self.assertEqual(result["text"].strip(), "The 10th lord is Saturn.")

    def test_arms_call_doctrine_prompt(self):
        from eval_arms import run_without

        client = FakeClient(["The 10th lord is Saturn."] * 3)
        run_without(
            client, ITEM, chart_with({"Sun": 10.5}), LEDGER, budget=3000,
            doctrine_prompt="DOCTRINE-CONTENT-XYZ",
        )
        self.assertEqual({c["system"] for c in client.calls}, {"DOCTRINE-CONTENT-XYZ"})


class TestChatClient(unittest.TestCase):
    def test_api_key_required(self):
        from eval_arms import ChatClient

        old = os.environ.pop("OPENROUTER_API_KEY", None)
        try:
            with self.assertRaises(RuntimeError):
                ChatClient()
        finally:
            if old is not None:
                os.environ["OPENROUTER_API_KEY"] = old

    def test_client_constructs_with_key(self):
        from eval_arms import ChatClient

        old = os.environ.get("OPENROUTER_API_KEY")
        os.environ["OPENROUTER_API_KEY"] = "test-key"
        try:
            client = ChatClient()
            self.assertIsNotNone(client)
        finally:
            if old is None:
                os.environ.pop("OPENROUTER_API_KEY", None)
            else:
                os.environ["OPENROUTER_API_KEY"] = old


if __name__ == "__main__":
    unittest.main()
