"""
Reject yes-man / prophecy language in README.md.
Mirrors tests/test_minimap.py's persona guard for the repo front page.
Also pins the verified per-host install contract: pip-sourced doctrine,
no repo-clone copy steps, no phantom plugin-install commands.
"""

import re
import unittest


def _section(text, heading):
    """Return the README subsection starting at a '### ' heading or '**Heading**'
    line (exclusive of the next heading of equal-or-higher level)."""
    m = re.search(r"^(?:### " + re.escape(heading) + r"|\*\*" + re.escape(heading) + r"\*\*).*?$",
                  text, re.M)
    if not m:
        raise AssertionError(f"README section not found: {heading!r} (headings must not drift silently)")
    rest = text[m.end():]
    nxt = re.search(r"^#{2,3} ", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


class TestReadme(unittest.TestCase):
    def test_readme_has_no_yes_man_language(self):
        text = open("README.md", encoding="utf-8").read().lower()
        for phrase in ["world's greatest", "yantra", "guaranteed", "predictions will"]:
            self.assertNotIn(phrase, text, f"banned phrase present: {phrase}")

    def test_codex_install_is_pip_sourced(self):
        text = open("README.md", encoding="utf-8").read()
        codex = _section(text, "Codex")
        self.assertIn("pip install rishi-ai-mcp", codex)
        self.assertIn("os.path.dirname(rishi_ai_mcp.__file__)", codex)
        self.assertIn("~/.codex/skills/rishi-reading", codex)
        for block in re.findall(r"```(?:bash|sh|console)\n(.*?)```", codex, re.S):
            self.assertNotIn("git clone", block,
                             "install blocks must not require cloning the repo")
            self.assertNotIn("cp -r skills/", block,
                             "doctrine must come from the installed wheel, not a repo checkout")

    def test_codex_has_no_plugin_install_command(self):
        text = open("README.md", encoding="utf-8").read()
        codex = _section(text, "Codex")
        self.assertNotRegex(codex, r"codex plugin install\b",
                            "v0.128.0 has no plugin install subcommand; README must not invent one")

    def test_opencode_install_is_pip_sourced(self):
        text = open("README.md", encoding="utf-8").read()
        oc = _section(text, "OpenCode")
        self.assertIn("pip install rishi-ai-mcp", oc)
        self.assertIn("os.path.dirname(rishi_ai_mcp.__file__)", oc)
        self.assertIn("~/.config/opencode/skills/rishi-reading", oc)
        for block in re.findall(r"```(?:bash|sh|console)\n(.*?)```", oc, re.S):
            self.assertNotIn("git clone", block,
                             "install blocks must not require cloning the repo")
            self.assertNotIn("cp -r skills/", block,
                             "doctrine must come from the installed wheel, not a repo checkout")

    def test_opencode_mcp_snippet_is_flat(self):
        text = open("README.md", encoding="utf-8").read()
        oc = _section(text, "OpenCode")
        self.assertIn('"vedic-astrology"', oc)
        for block in re.findall(r"```(?:jsonc?|json|toml)\n(.*?)```", oc, re.S):
            self.assertNotIn("mcp.servers", block,
                             "config snippets must use flat keys; nested mcp.servers is ignored")


if __name__ == "__main__":
    unittest.main()
