"""
Consistency test for the system_prompt.md minimap.
The vendored doctrine (wheel: skills/rishi-reading/) is authoritative;
this file is only a minimap, and it must name the six rules.
"""

import unittest


class TestSystemPromptMinimap(unittest.TestCase):
    def test_minimap_mentions_all_six_rules(self):
        text = open("system_prompt.md", encoding="utf-8").read()
        for rule in ["R1", "R2", "R3", "R4", "R5", "R6"]:
            self.assertIn(rule, text, f"missing rule tag {rule}")
        for literal in [
            "skills/rishi-reading/contract.md",
            "grounds appendix",
            "calibration footer",
            "disagreement log",
            "Lahiri",
        ]:
            self.assertIn(literal, text, f"missing literal: {literal}")

    def test_minimap_has_no_yes_man_language(self):
        text = open("system_prompt.md", encoding="utf-8").read()
        banned = [
            "world's greatest",
            "guaranteed",
            "destiny is sealed",
            "predestin",
        ]
        for phrase in banned:
            self.assertNotIn(phrase.lower(), text.lower(), f"banned phrase present: {phrase}")

    def test_minimap_length_is_compact(self):
        text = open("system_prompt.md", encoding="utf-8").read()
        self.assertLess(len(text.split()), 400, "minimap bloated beyond ~400 words")


if __name__ == "__main__":
    unittest.main()
