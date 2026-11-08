"""Tests for the with-arm (verifier -> critic -> revision) and bare arm.

FakeClient records call order and max_tokens so budget shares and stage
sequencing are pinned without any network.
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
            }
        )
        text = self.texts.pop(0) if self.texts else "ok"
        return {
            "text": text,
            "output_tokens": self.tokens_per_call,
            "input_tokens": 500,
            "latency_s": 0.01,
        }


ITEM = {"id": "g-01", "prompt": "How is my career?"}
LEDGER = {"clauses": [], "required_grounds": ["10th lord"]}


class TestWithArm(unittest.TestCase):
    def test_with_four_stages_in_order(self):
        from eval_arms import run_with

        client = FakeClient(
            [
                "DRAFT: The 10th lord is Saturn.",
                "VERIFIER: approve",
                "CRITIC: conformant",
                "REVISED: The 10th lord is Saturn.",
            ]
        )
        result = run_with(
            client, ITEM, chart_with({"Sun": 10.5}), LEDGER, budget=3000,
            doctrine_prompt="DOCTRINE",
        )
        self.assertEqual(len(client.calls), 4)
        self.assertEqual([c["max_tokens"] for c in client.calls], [1000, 500, 500, 1000])
        self.assertEqual(result["text"], "REVISED: The 10th lord is Saturn.")
        self.assertFalse(result["disqualified"])
        # draft uses doctrine; verifier/critic use the agent definitions
        self.assertEqual(client.calls[0]["system"], "DOCTRINE")
        self.assertIn("chart-verifier", client.calls[1]["system"].lower())
        self.assertIn("doctrine-critic", client.calls[2]["system"].lower())

    def test_with_revision_gets_only_denials(self):
        from eval_arms import run_with

        client = FakeClient(
            [
                "DRAFT: The 10th lord is Jupiter.",
                "CLAIM-1: deny — chart shows Saturn\nCLAIM-2: approve",
                "CLAIM-1: nonconformant — wrong lord cited",
                "REVISED: The 10th lord is Saturn.",
            ]
        )
        run_with(
            client, ITEM, chart_with({"Sun": 10.5}), LEDGER, budget=3000,
            doctrine_prompt="DOCTRINE",
        )
        revision_prompt = client.calls[3]["user"]
        self.assertIn("deny", revision_prompt)
        self.assertIn("wrong lord", revision_prompt)
        self.assertNotIn("CLAIM-2: approve", revision_prompt)

    def test_with_budget_overrun_raises(self):
        from eval_arms import BudgetExceeded, run_with

        client = FakeClient(["a", "b", "c", "d"], tokens_per_call=1000)  # 4000 > 3000
        with self.assertRaises(BudgetExceeded):
            run_with(
                client, ITEM, chart_with({"Sun": 10.5}), LEDGER, budget=3000,
                doctrine_prompt="DOCTRINE",
            )


class TestBareArm(unittest.TestCase):
    def test_bare_single_call_uses_whole_budget(self):
        from eval_arms import run_bare

        client = FakeClient(["BARE: career looks steady."])
        result = run_bare(client, ITEM, chart_with({"Sun": 10.5}), budget=3000)
        self.assertEqual(len(client.calls), 1)
        self.assertEqual(client.calls[0]["max_tokens"], 3000)
        self.assertEqual(client.calls[0]["temperature"], 0)
        self.assertEqual(result["text"], "BARE: career looks steady.")
        self.assertIn("Vedic astrologer", client.calls[0]["system"])


if __name__ == "__main__":
    unittest.main()
