"""Schema and construction checks for the ratified v2 corpus."""

import json
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES = os.path.join(ROOT, "evals", "v2", "cases")
sys.path.insert(0, os.path.join(ROOT, "tools"))


def _rows(name):
    with open(os.path.join(CASES, f"{name}.jsonl"), encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


class TestV2Corpus(unittest.TestCase):
    def setUp(self):
        self.records = {name: _rows(name) for name in ("grounding", "sycophancy", "remedy")}
        with open(os.path.join(CASES, "ledger.json"), encoding="utf-8") as fh:
            self.ledger = json.load(fh)["items"]

    def test_forty_unique_items(self):
        ids = [r["id"] for rows in self.records.values() for r in rows]
        self.assertEqual(len(ids), 40)
        self.assertEqual(len(set(ids)), 40)
        self.assertEqual(set(ids), set(self.ledger))

    def test_tags_and_counts(self):
        self.assertEqual(sum(len(v) for v in self.records.values()), 40)
        self.assertEqual(len(self.records["grounding"]), 20)
        self.assertEqual(len(self.records["sycophancy"]), 10)
        self.assertEqual(len(self.records["remedy"]), 10)
        for item_id, entry in self.ledger.items():
            if item_id.startswith("v2-g-"):
                self.assertEqual(entry["tag"], "chart-grounded")
                self.assertTrue(entry["required_grounds"])
            else:
                self.assertEqual(entry["tag"], "interpretation-only")
                self.assertFalse(entry["required_grounds"])
            self.assertGreaterEqual(len(entry["clauses"]), 1)
            self.assertLessEqual(len(entry["clauses"]), 3)
            self.assertTrue(entry.get("rationale"))

    def test_birth_data_is_anonymous(self):
        for rows in self.records.values():
            for record in rows:
                self.assertEqual(set(record["birth"]), {"dob", "time", "lat", "lon", "tz"})
                self.assertEqual(record["birth"]["tz"], "UTC")
                self.assertNotIn("name", record["birth"])
                self.assertNotIn("name", record)

    def test_all_charts_cast(self):
        import dashaflow

        for rows in self.records.values():
            for record in rows:
                birth = record["birth"]
                chart = dashaflow.cast_chart(
                    birth["dob"], birth["time"], birth["lat"], birth["lon"], birth["tz"]
                )
                self.assertIn("planets", chart)
                self.assertIn("lagna", chart)

    def test_required_grounds_are_known_aliases(self):
        from eval_scoring import _ground_variants

        for entry in self.ledger.values():
            for ground in entry["required_grounds"]:
                self.assertTrue(_ground_variants(ground), ground)


if __name__ == "__main__":
    unittest.main()
