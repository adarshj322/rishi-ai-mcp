"""Tests for the pre-authored corpus ledger and prompt files.

The ledger is the pre-commitment surface: clauses and required grounds are
authored BEFORE the first run (evals/README.md §2.1). These tests pin the
schema and the construction rule; the runner consumes the same shapes.
"""

import json
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES = os.path.join(ROOT, "evals", "cases")
LEDGER = os.path.join(CASES, "ledger.json")
PROMPTS = os.path.join(ROOT, "evals", "prompts")


def _case_ids():
    ids = []
    for name in ("grounding.jsonl", "sycophancy.jsonl", "remedy.jsonl"):
        with open(os.path.join(CASES, name), encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    ids.append(json.loads(line)["id"])
    return ids


def _case_by_id(item_id):
    for name in ("grounding.jsonl", "sycophancy.jsonl", "remedy.jsonl"):
        with open(os.path.join(CASES, name), encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                if record["id"] == item_id:
                    return record
    raise KeyError(item_id)


class TestLedger(unittest.TestCase):
    def test_every_case_has_ledger_entry(self):
        with open(LEDGER, encoding="utf-8") as fh:
            ledger = json.load(fh)
        ids = set(_case_ids())
        self.assertEqual(len(ids), 26)
        self.assertEqual(set(ledger["items"]), ids)

    def test_tags_valid_and_g_are_chart_grounded(self):
        with open(LEDGER, encoding="utf-8") as fh:
            ledger = json.load(fh)
        for item_id, entry in ledger["items"].items():
            self.assertIn(entry["tag"], ("chart-grounded", "interpretation-only"), item_id)
            if item_id.startswith("g-"):
                self.assertEqual(entry["tag"], "chart-grounded", item_id)
            else:
                self.assertEqual(entry["tag"], "interpretation-only", item_id)

    def test_every_item_has_clauses_and_required_grounds(self):
        with open(LEDGER, encoding="utf-8") as fh:
            ledger = json.load(fh)
        for item_id, entry in ledger["items"].items():
            self.assertTrue(entry["clauses"], item_id)
            if entry["tag"] == "chart-grounded":
                # Ruling (ledger): deterministic grounds are enforced only for
                # chart-grounded items; interpretation items are judge-enforced.
                self.assertTrue(entry["required_grounds"], item_id)
            for clause in entry["clauses"]:
                self.assertIn("text", clause, item_id)
                self.assertIsInstance(clause["mechanical"], bool, item_id)

    def test_clauses_quote_the_rubric(self):
        """Spot-check three items: each clause text is a fragment of the rubric."""
        with open(LEDGER, encoding="utf-8") as fh:
            ledger = json.load(fh)
        for item_id in ("g-01", "s-01", "r-01"):
            rubric = _case_by_id(item_id)["expected_verifier_verdict"]
            for clause in ledger["items"][item_id]["clauses"]:
                self.assertIn(clause["text"], rubric, item_id)


class TestPrompts(unittest.TestCase):
    def test_prompt_files_exist_and_nonempty(self):
        for name in ("bare_system.md", "doctrine_system.md", "judge.md"):
            path = os.path.join(PROMPTS, name)
            self.assertTrue(os.path.isfile(path), path)
            self.assertGreater(len(open(path, encoding="utf-8").read().strip()), 100, name)

    def test_bare_prompt_has_no_doctrine(self):
        text = open(os.path.join(PROMPTS, "bare_system.md"), encoding="utf-8").read().lower()
        for banned in ("contract", "r1", "r2", "r3", "r4", "r5", "r6", "claim-ground",
                       "grounds appendix", "disagreement log"):
            self.assertNotIn(banned, text, banned)

    def test_judge_prompt_forbids_arm_labels(self):
        text = open(os.path.join(PROMPTS, "judge.md"), encoding="utf-8").read().lower()
        self.assertIn("json", text)
        self.assertIn("evidence", text)


if __name__ == "__main__":
    unittest.main()
