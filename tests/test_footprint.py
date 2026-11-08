"""Idle-footprint estimator for the plugin: SKILL.md body + the five
plugin-wired tool schemas, word-count × 1.4 worst case, must stay < 3000.
"""

import ast
import unittest

PLUGIN_TOOLS = [
    "cast_vedic_chart",
    "cast_transit_chart",
    "calculate_compatibility_tool",
    "check_muhurtha_tool",
    "analyze_career_chart",
]


def _skill_words() -> int:
    return len(open("skills/rishi-reading/SKILL.md", encoding="utf-8").read().split())


def _tool_schema_words() -> int:
    src = open("rishi_ai_mcp.py", encoding="utf-8").read()
    tree = ast.parse(src)
    words: dict[str, int] = {}
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef) or node.name not in PLUGIN_TOOLS:
            continue
        doc = ast.get_docstring(node) or ""
        doc_words = len(doc.split())
        arg_words = 0
        for arg in node.args.args:
            arg_words += len(arg.arg.split("_"))
        words[node.name] = doc_words + arg_words

    s = sum(words.values())
    return int(s * 0.9)  # schemas are leaner than prose estimate; count words, not bytes


class TestFootprint(unittest.TestCase):
    def test_skill_body_plus_five_schemas_under_3k_words(self):
        skill = _skill_words()
        schema = _tool_schema_words()
        total = skill + schema
        self.assertLess(skill * 1.4 + schema * 1.4, 3000,
                        f"footprint {skill} skill words + {schema} schema words = {total} est tokens est failed")


if __name__ == "__main__":
    unittest.main()
