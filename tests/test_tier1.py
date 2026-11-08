"""
Tier-1 corpus validation + determinism gate tests.

Binding caveat (evals/README §2.2, stamped verbatim there):
    "Shared lineage (dashaflow → pyswisseph → Moshier fallback): this is a
     regression/determinism gate, NOT astronomical-truth verification."

`test_corpus_pinned_deterministically` runs tools/tier1_check.py, which casts
each moment in a FRESH subprocess twice and requires byte-identical chart JSON
plus <=1e-6 relative positional agreement. Full 300 moments run only under
TIER1_FULL=1; otherwise a deterministic evenly-spaced 8-moment sample runs.
No repository corpus files are written by these tests.
"""

import json
import os
import re
import subprocess
import sys
import unittest
from collections import Counter
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MOMENTS = REPO / "evals" / "tier1" / "moments.json"
CHECK = REPO / "tools" / "tier1_check.py"
UTC_FMT = "%Y-%m-%d %H:%M:%S"
LOWER = datetime(1900, 1, 1, 0, 0, 0)
UPPER = datetime(2030, 12, 31, 23, 59, 59)
BANGALORE = (12.9716, 77.5946)
SAMPLE_SIZE = 8


def load_corpus():
    with MOMENTS.open(encoding="utf-8") as fh:
        return json.load(fh)


class MomentsFileValidity(unittest.TestCase):
    def test_moments_file_valid(self):
        entries = load_corpus()

        self.assertIsInstance(entries, list)
        self.assertEqual(len(entries), 300, "corpus must hold exactly 300 moments")

        required = {"utc", "source", "rationale", "place", "lat", "lon", "timezone"}
        parsed = []
        for i, entry in enumerate(entries):
            with self.subTest(index=i, utc=entry.get("utc")):
                self.assertTrue(required <= set(entry), f"missing fields: {required - set(entry)}")
                self.assertIn(entry["source"], ("generated", "manual"))
                self.assertTrue(entry["rationale"].strip(), "rationale must be non-empty")
                self.assertTrue(entry["place"].strip(), "place must be non-empty")
                self.assertEqual(entry["timezone"], "Asia/Kolkata",
                                 "single pinned timezone keeps the fixture deterministic")
                self.assertTrue(-90.0 <= entry["lat"] <= 90.0)
                self.assertTrue(-180.0 <= entry["lon"] <= 180.0)
                parsed.append(datetime.strptime(entry["utc"], UTC_FMT))

        self.assertEqual(min(parsed), LOWER, "corpus must reach 1900")
        self.assertGreaterEqual(max(parsed), datetime(2030, 1, 1), "corpus must reach 2030")
        for dt in parsed:
            self.assertTrue(LOWER <= dt <= UPPER, "moment outside 1900-01-01..2030-12-31 span")

        counts = Counter(e["source"] for e in entries)
        self.assertEqual(counts["generated"], 260)
        self.assertEqual(counts["manual"], 40)

        generated = [e for e in entries if e["source"] == "generated"]
        for e in generated:
            with self.subTest(generated=e["utc"]):
                dt = datetime.strptime(e["utc"], UTC_FMT)
                self.assertIn((dt.month, dt.day, dt.hour, dt.minute, dt.second),
                              {(1, 1, 0, 0, 0), (7, 1, 12, 0, 0)},
                              "generated entries must be Jan 1 00:00:00 or Jul 1 12:00:00")
                self.assertIn(dt.year, range(1900, 2030))
                self.assertEqual((e["lat"], e["lon"]), BANGALORE)
                self.assertEqual(e["rationale"], "year-start/year-midfield deterministic pin")

        manual = [e for e in entries if e["source"] == "manual"]
        manual_utcs = [e["utc"] for e in manual]
        self.assertEqual(len(set(manual_utcs)), 40, "manual entries must be distinct instants")

        # 6 manual landmark instants intentionally overlap generator output
        # (hand-tagged deliberately); corpus-wide uniqueness is NOT asserted.
        all_utcs = [e["utc"] for e in entries]
        self.assertEqual(len(all_utcs) - len(set(all_utcs)), 6)


@unittest.skipUnless(CHECK.exists(), "tools/tier1_check.py is missing")
class Tier1Determinism(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import dashaflow  # noqa: F401
        except Exception as exc:  # degrade explicitly, never silently pass
            raise unittest.SkipTest(
                f"dashaflow not importable — Tier-1 gate skipped (reason: {exc}); "
                "degradation to be recorded in evals/README.md by the maintainer") from exc

    def test_corpus_pinned_deterministically(self):
        full = os.environ.get("TIER1_FULL") == "1"
        cmd = [sys.executable, str(CHECK)] if full else [sys.executable, str(CHECK), "--sample", str(SAMPLE_SIZE)]
        expected = 300 if full else SAMPLE_SIZE
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=7200, check=False)
        self.assertEqual(
            proc.returncode, 0,
            f"tier1_check failed (exit {proc.returncode})\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}")
        m = re.search(r"(\d+) moments OK", proc.stdout)
        self.assertIsNotNone(m, f"missing summary line in output:\n{proc.stdout}")
        self.assertEqual(int(m.group(1)), expected)


if __name__ == "__main__":
    unittest.main()
