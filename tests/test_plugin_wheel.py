"""
Wheel packaging test: the pip wheel must ship the skills/ doctrine files
(rishi-reading SKILL.md / contract.md / references) so pip-installed
users get the real files, not just a pointer.
"""

import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build_available() -> bool:
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "build", "--version"],
            capture_output=True, text=True, timeout=60, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return proc.returncode == 0


class TestPluginWheel(unittest.TestCase):
    def test_skills_in_wheel(self):
        if not build_available():
            raise unittest.SkipTest("python -m build is not available")

        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                [sys.executable, "-m", "build", "--wheel", "--outdir", tmp, str(ROOT)],
                capture_output=True, text=True, timeout=600, check=False,
            )
            self.assertEqual(proc.returncode, 0,
                             f"python -m build failed:\n{proc.stdout}\n{proc.stderr}")

            wheels = list(Path(tmp).glob("rishi_ai_mcp-*.whl"))
            self.assertEqual(len(wheels), 1, f"expected one wheel in {tmp}, got {wheels}")
            wheel = wheels[0]

            with zipfile.ZipFile(wheel) as zf:
                names = zf.namelist()
            listing = "\n".join(sorted(names))

            try:
                self.assertIn("rishi_ai_mcp.py", names)
                for member in (
                    "skills/rishi-reading/SKILL.md",
                    "skills/rishi-reading/contract.md",
                    "skills/rishi-reading/references/bphs-rulebook.md",
                ):
                    self.assertIn(member, names)
                for member in names:
                    self.assertFalse(
                        member.startswith("agents/skills/") or member.startswith(".agents/"),
                        f"wheel must not vendor .agents/ content: {member}",
                    )
            except AssertionError:
                print(f"wheel listing for {wheel.name}:\n{listing}")
                raise


if __name__ == "__main__":
    unittest.main()
