"""
Manifest test for the rishi-reading skill.

The skill's references block is the disclosure manifest CI checksums:
every doctrine file in skills/rishi-reading/references/ is listed,
no listed file is missing from disk, and the skill carries valid frontmatter.
README.md is the manifest index, not a doctrine reference — it must not be listed.
"""

import re
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1] / "skills" / "rishi-reading"
SKILL_MD = SKILL_DIR / "SKILL.md"
REFERENCES_DIR = SKILL_DIR / "references"


class TestSkillManifest(unittest.TestCase):
    def test_references_manifest_lists_every_reference_file(self):
        self.assertTrue(SKILL_MD.exists(), "skills/rishi-reading/SKILL.md is missing")
        text = SKILL_MD.read_text(encoding="utf-8")

        on_disk = sorted(p.name for p in REFERENCES_DIR.glob("*.md"))
        self.assertEqual(len(on_disk), 8,
                         f"expected exactly 8 reference files (7 doctrine + README.md), found {on_disk}")
        doctrine = [f for f in on_disk if f != "README.md"]
        self.assertEqual(len(doctrine), 7)

        listed = set(re.findall(r"references/[A-Za-z0-9._-]+\.md", text))
        for f in doctrine:
            self.assertIn(f"references/{f}", listed,
                          f"references/{f} exists on disk but is not listed in SKILL.md")
        self.assertNotIn("references/README.md", listed,
                         "README.md is the manifest index, not a doctrine reference; it must not be listed")
        for ref in listed:
            self.assertTrue((SKILL_DIR / ref).is_file(),
                            f"SKILL.md lists {ref} but it is missing from disk")

        m = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        self.assertIsNotNone(m, "SKILL.md must start with YAML frontmatter delimited by ---")
        fm = m.group(1)
        name_m = re.search(r"^name:\s*([^\s]+)\s*$", fm, re.M)
        self.assertIsNotNone(name_m, "frontmatter must carry name:")
        self.assertEqual(name_m.group(1), "rishi-reading")
        desc_m = re.search(r"^description:\s*(.+?)\s*$", fm, re.M)
        self.assertIsNotNone(desc_m, "frontmatter must carry description:")
        desc = desc_m.group(1).strip()
        self.assertTrue(desc, "description must be non-empty")
        self.assertLessEqual(len(desc), 130,
                             f"description must be <= 130 chars, got {len(desc)}")


if __name__ == "__main__":
    unittest.main()
