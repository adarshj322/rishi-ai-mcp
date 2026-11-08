"""
Reject yes-man / prophecy language in README.md.
Mirrors tests/test_minimap.py's persona guard for the repo front page.
"""

import unittest


class TestReadme(unittest.TestCase):
    def test_readme_has_no_yes_man_language(self):
        text = open("README.md", encoding="utf-8").read().lower()
        for phrase in ["world's greatest", "yantra", "guaranteed", "predictions will"]:
            self.assertNotIn(phrase, text, f"banned phrase present: {phrase}")


if __name__ == "__main__":
    unittest.main()
