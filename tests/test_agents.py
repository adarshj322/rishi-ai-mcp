"""
Integrity tests for the two subagent definition files shipped in Tasks 6-7:
agents/chart-verifier.md and agents/doctrine-critic.md.

Both files carry YAML frontmatter (name/description/tools:[Read]) and an H2 body
contract (Inputs, verdict tables, stop rules). The two agents deliberately use
different halt markers (DENY-ALL: / rival-premise-denied vs HALT: / opposed-premise);
these tests assert each file carries its own markers and never assert cross-file
marker equality.
"""

import re
import unittest
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - CI installs pyyaml; bare envs skip
    yaml = None

REPO_ROOT = Path(__file__).resolve().parents[1]
VERIFIER = REPO_ROOT / "agents" / "chart-verifier.md"
CRITIC = REPO_ROOT / "agents" / "doctrine-critic.md"
REFERENCES = REPO_ROOT / "skills" / "rishi-reading" / "references"


def read(path):
    return path.read_text(encoding="utf-8")


def frontmatter(text):
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if m is None:
        return None, None
    return m.group(1), m.end()


def check_zero_code_and_no_network(testcase, text):
    testcase.assertIsNone(re.search(r"https?://", text), "no network URLs allowed")
    testcase.assertIsNone(re.search(r"\bopen\(", text), "no file-writing open() calls allowed")
    for cmd in (r"\bpip\b", r"\bcurl\b", r"\bsh\b", r"\bpython\b"):
        testcase.assertIsNone(re.search(cmd, text),
                              f"no shell/python command tokens allowed (matched {cmd!r})")


class AgentFileTestCase(unittest.TestCase):
    path = None
    name = None

    def setUp(self):
        if self.path is None:
            raise unittest.SkipTest("base class — subclassed per agent")
        self.text = read(self.path) if self.path.is_file() else ""

    def test_exists_and_frontmatter(self):
        self.assertTrue(self.path.is_file(), f"{self.path} is missing")
        if yaml is None:
            raise unittest.SkipTest("pyyaml not installed — frontmatter parse skipped")
        text = self.text
        self.assertTrue(text.startswith("---\n"), "file must start with YAML frontmatter (---)")
        fm_raw, body_start = frontmatter(text)
        self.assertIsNotNone(fm_raw, "frontmatter block delimited by --- must be present")
        data = yaml.safe_load(fm_raw)
        self.assertIsInstance(data, dict, "frontmatter must parse as a YAML mapping")
        self.assertEqual(data.get("name"), self.name)
        self.assertTrue(str(data.get("description", "")).strip(),
                        "frontmatter description must be non-empty")
        self.assertEqual(list(data.get("tools", [])), ["Read"],
                         "frontmatter tools must be exactly [Read]")
        body = text[body_start:]
        self.assertRegex(body, r"(?m)^## ", "an H2 section must follow the frontmatter")


class TestChartVerifier(AgentFileTestCase):
    path = VERIFIER
    name = "chart-verifier"

    def test_binary_verdict_contract(self):
        text = self.text
        for token in ("claim", "verdict", "approve", "deny"):
            self.assertIn(token, text)
        self.assertTrue("chart field" in text or "grounds-pointer" in text,
                        "must reference a chart field or grounds-pointer")
        self.assertIn("factual claims verified", text)

    def test_deny_blocks_facts(self):
        text = self.text
        self.assertIn("deny", text)
        self.assertRegex(text, r"\bblocks\b",
                         "a deny must carry an explicit blocking relationship")
        self.assertIn("N/A", text, "interpretive claims must be marked N/A")

    def test_stop_rule_and_halt(self):
        text = self.text
        self.assertIn("unsure", text)
        self.assertIn("deny", text, "unsure must be treated as deny for factual claims")
        self.assertIn("DENY-ALL:", text)

    def test_zero_code_and_no_network(self):
        check_zero_code_and_no_network(self, self.text)


class TestDoctrineCritic(AgentFileTestCase):
    path = CRITIC
    name = "doctrine-critic"

    def test_no_chart_recompute(self):
        text = self.text
        self.assertIn("recompute", text)
        self.assertTrue(
            re.search(r"(?i)\bnever\b[^\n]*recompute|recompute[^\n]*\bnever\b", text)
            or "BPHS-conformity" in text,
            "must carry a clear prohibition on recomputing (never/not) or BPHS-conformity frame",
        )

    def test_verdict_contract(self):
        text = self.text
        self.assertIn("conformant", text)
        self.assertTrue("nonconformant" in text or "unsupported" in text)
        self.assertRegex(text, r"(?i)\bcheck(s|ing|ed)?\b",
                         "must carry a reference-resolution phrase (check/checking/checks)")

    def test_anti_reward_hacking(self):
        text = self.text
        self.assertIn("citation", text)
        self.assertIn("reward", text, "must carry the anti-reward-hacking concept")
        self.assertRegex(text, r"(?i)anti-reward-hacking",
                         "must label a section/concept as anti-reward-hacking")

    def test_stop_rule_and_halt(self):
        text = self.text
        self.assertIn("HALT:", text)
        self.assertRegex(text, r"(?i)one pass", "must carry a one-pass stop rule")

    def test_zero_code_and_no_network(self):
        check_zero_code_and_no_network(self, self.text)


class TestCrossConsistency(unittest.TestCase):
    def test_reference_files_exist(self):
        for name in ("bphs-rulebook.md", "dignity-table.md", "dashas.md", "chart-walk-order.md"):
            path = REFERENCES / name
            self.assertTrue(path.is_file(), f"{path} referenced by the agents is missing")

    def test_no_marker_equality(self):
        verifier = read(VERIFIER)
        critic = read(CRITIC)
        self.assertIn("DENY-ALL:", verifier)
        self.assertIn("HALT:", critic)
        self.assertIn("rival-premise-denied", verifier)
        self.assertIn("opposed-premise", critic)
        self.assertNotEqual("rival-premise-denied", "opposed-premise",
                            "marker literals are divergent by design")
        self.assertNotEqual("DENY-ALL:", "HALT:",
                            "halt literals are divergent by design")


if __name__ == "__main__":
    unittest.main()
