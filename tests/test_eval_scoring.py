"""Tests for tools/eval_scoring.py — deterministic scoring primitives.

Every test here pins a behavior the equal-cost runner depends on. No
network, no model calls, no chart engine: synthetic chart dicts only.
"""

import math
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))


def chart_with(planets, lagna_degree=10.0):
    """Minimal chart shape matching dashaflow's planets block."""
    return {
        "lagna": {"sign": "Aries", "degree": lagna_degree, "nakshatra": "Ashwini"},
        "planets": {
            name: {
                "sign": "Aries",
                "degree": deg,
                "house": 1,
                "dignity": "neutral",
            }
            for name, deg in planets.items()
        },
        "dashas": {
            "maha": {"lord": "Jupiter", "start": "2020-01-01", "end": "2036-12-31"},
            "antar": {"lord": "Saturn", "start": "2026-01-01", "end": "2028-06-30"},
        },
        "ashtakavarga": {"sarvashtakavarga": {"Aries": 28}},
    }


class TestComputeSE(unittest.TestCase):
    def test_compute_se_rule1(self):
        from eval_scoring import compute_se

        self.assertAlmostEqual(compute_se(26), 0.5 / math.sqrt(26), places=12)
        self.assertAlmostEqual(compute_se(26), 0.098058, places=5)

    def test_compute_se_rejects_nonpositive(self):
        from eval_scoring import compute_se

        with self.assertRaises(ValueError):
            compute_se(0)


class TestWilsonInterval(unittest.TestCase):
    def test_wilson_bounds(self):
        from eval_scoring import wilson_interval

        low, high = wilson_interval(20, 26)
        self.assertLess(low, 20 / 26)
        self.assertGreater(high, 20 / 26)
        self.assertGreaterEqual(low, 0.0)
        self.assertLessEqual(high, 1.0)

    def test_wilson_edge_cases(self):
        from eval_scoring import wilson_interval

        for k, n in ((0, 10), (10, 10), (0, 1), (1, 1)):
            low, high = wilson_interval(k, n)
            self.assertGreaterEqual(low, 0.0, (k, n))
            self.assertLessEqual(high, 1.0, (k, n))
            self.assertLessEqual(low, high, (k, n))

    def test_wilson_rejects_invalid_counts(self):
        from eval_scoring import wilson_interval

        with self.assertRaises(ValueError):
            wilson_interval(5, 0)
        with self.assertRaises(ValueError):
            wilson_interval(11, 10)


class TestFabrication(unittest.TestCase):
    def test_fabrication_flags_unknown_degree(self):
        from eval_scoring import find_fabrications

        chart = chart_with({"Sun": 10.5, "Moon": 100.0})
        self.assertTrue(find_fabrications("Your Sun sits at 23° in Aries.", chart))
        self.assertEqual(find_fabrications("Your Sun sits at 23° in Aries.", chart), ["23°"])

    def test_cross_planet_degree_is_flagged(self):
        from eval_scoring import find_fabrications

        chart = chart_with({"Sun": 10.5, "Moon": 23.0})
        # 23° belongs to the Moon, not the Sun -> fabrication for the Sun claim.
        self.assertEqual(find_fabrications("Sun at 23° in Aries", chart), ["23°"])

    def test_known_degree_passes(self):
        from eval_scoring import find_fabrications

        chart = chart_with({"Sun": 10.5, "Moon": 23.0})
        self.assertEqual(find_fabrications("Sun at 10.5° in Aries.", chart), [])
        # minute form of the same value
        self.assertEqual(find_fabrications("Sun at 10°30' in Aries.", chart), [])

    def test_unknown_date_is_flagged_and_known_date_passes(self):
        from eval_scoring import find_fabrications

        chart = chart_with({"Sun": 10.5})
        self.assertEqual(find_fabrications("The period runs 2026-01-01 to 2028-06-30.", chart), [])
        # inside the chart's 2020-2036 maha range: allowed as a window reference
        self.assertEqual(find_fabrications("It lifts in March 2031.", chart), [])
        self.assertEqual(find_fabrications("It began in January 2020.", chart), [])
        # outside every chart range: fabricated
        self.assertEqual(find_fabrications("Marriage will happen in 2041-05-04.", chart), ["2041-05-04"])
        self.assertEqual(find_fabrications("It returns in March 2041.", chart), ["March 2041"])

    def test_derived_separation_degree_is_not_fabrication(self):
        from eval_scoring import find_fabrications

        chart = chart_with({"Sun": 10.5, "Moon": 100.0})
        self.assertEqual(
            find_fabrications("The Moon is 3.3° from the Capricorn cusp.", chart), []
        )
        self.assertEqual(
            find_fabrications("Saturn is within 1° of the Sun.", chart), []
        )


    def test_transit_degree_is_accepted(self):
        from eval_scoring import find_fabrications

        chart = chart_with({"Saturn": 10.5})
        chart["transit"] = {"planets": {"Saturn": {"degree": 25.0}}}
        self.assertEqual(find_fabrications("Transit Saturn at 25° in Pisces.", chart), [])
    def test_absolute_unknown_degree_still_flagged(self):
        from eval_scoring import find_fabrications

        chart = chart_with({"Sun": 10.5})
        self.assertEqual(find_fabrications("Sun at 29° in Aries.", chart), ["29°"])


class TestDeterministicVerdict(unittest.TestCase):

    def test_lagna_degree_is_not_fabrication(self):
        from eval_scoring import find_fabrications

        chart = chart_with({"Sun": 10.5, "Moon": 3.87}, lagna_degree=28.8)
        text = "Moon Pisces 3.87° h10; Lagna Gemini 28.8°."
        self.assertEqual(find_fabrications(text, chart), [])

    def test_degree_binds_to_nearest_planet_not_any_nearby(self):
        from eval_scoring import find_fabrications

        # "dead state, 25.9°" belongs to Jupiter (25.93); "Sun" appears later in
        # "combust by the Sun" and must not hijack the association.
        chart = chart_with({"Jupiter": 25.93, "Sun": 24.14})
        text = "Jupiter is in Cancer at its condition: Mrita avastha (dead state, 25.9°), combust by the Sun at 24.14° Cancer."
        self.assertEqual(find_fabrications(text, chart), [])

    def test_deterministic_verdict_missing_required_ground(self):
        from eval_scoring import deterministic_verdict

        entry = {
            "clauses": [{"text": "cite the 10th lord", "mechanical": True}],
            "required_grounds": ["10th lord"],
        }
        chart = chart_with({"Sun": 10.5})
        verdict = deterministic_verdict("Your career looks bright this year.", entry, chart)
        self.assertFalse(verdict["pass"])
        self.assertTrue(any("10th lord" in f for f in verdict["failures"]))

    def test_deterministic_verdict_passes_with_grounds_and_no_fabrication(self):
        from eval_scoring import deterministic_verdict

        entry = {
            "clauses": [{"text": "cite the 10th lord", "mechanical": True}],
            "required_grounds": ["10th lord"],
        }
        chart = chart_with({"Sun": 10.5})
        text = "The 10th lord Saturn sits in Aries; Sun at 10.5° in Aries."
        verdict = deterministic_verdict(text, entry, chart)
        self.assertTrue(verdict["pass"], verdict["failures"])

    def test_deterministic_verdict_fails_on_fabrication_even_with_grounds(self):
        from eval_scoring import deterministic_verdict

        entry = {"clauses": [], "required_grounds": ["10th lord"]}
        chart = chart_with({"Sun": 10.5})
        verdict = deterministic_verdict("The 10th lord is strong, Sun at 29° in Aries.", entry, chart)
        self.assertFalse(verdict["pass"])


class TestGroundAliases(unittest.TestCase):
    def test_required_ground_prose_aliases(self):
        from eval_scoring import deterministic_verdict

        chart = chart_with({"Sun": 10.5})
        cases = [
            ("sav_points", "SAV bindus for the sign are 28."),
            ("arudha_padas", "The arudha padas A1 and A10 are cited."),
            ("D9", "the navamsha (D9) shows the same lord."),
            ("10th lord", "the tenth lord Saturn sits there."),
            ("6th", "the sixth house is afflicted."),
            ("graha_yuddha", "graha yuddha between Mars and Saturn."),
            ("gandanta", "the gandanta list is empty."),
            ("bhava_chalit", "the bhava chalit shifts it."),
            ("maha", "the mahadasha runs to 2035."),
            ("antar", "the antardasha is Sun."),
        ]
        for ground, text in cases:
            entry = {"clauses": [], "required_grounds": [ground]}
            verdict = deterministic_verdict(text, entry, chart)
            self.assertTrue(verdict["pass"], (ground, verdict["failures"]))

    def test_missing_ground_still_fails(self):
        from eval_scoring import deterministic_verdict

        entry = {"clauses": [], "required_grounds": ["sav_points"]}
        verdict = deterministic_verdict("Career looks steady.", entry, chart_with({"Sun": 10.5}))
        self.assertFalse(verdict["pass"])


if __name__ == "__main__":
    unittest.main()
