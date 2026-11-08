"""
Tests for tools/build_plugin.py — the manifest generator + check.

Every scenario runs against a tempdir copy of the packaging inputs;
the repo's real manifests (and rishi_ai_mcp.py) are never mutated.
"""

import contextlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "build_plugin.py"

sys.path.insert(0, str(ROOT / "tools"))
import build_plugin  # noqa: E402


def copy_packaging_inputs(dest: Path) -> None:
    shutil.copy(ROOT / "rishi_ai_mcp.py", dest / "rishi_ai_mcp.py")
    (dest / "packaging" / "hooks").mkdir(parents=True)
    shutil.copy(ROOT / "packaging" / "hooks" / "reminder.txt",
                dest / "packaging" / "hooks" / "reminder.txt")


class TestGetVersion(unittest.TestCase):
    def test_reads_version(self):
        version = build_plugin.get_version()
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")

    def test_missing_version_source(self):
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "rishi_ai_mcp.py"
            src.write_text("X = 1\n", encoding="utf-8")
            with self.assertRaises(build_plugin.VersionSourceMissing):
                build_plugin.get_version(src)

    def test_non_string_version_source(self):
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "rishi_ai_mcp.py"
            src.write_text("__version__ = 150\n", encoding="utf-8")
            with self.assertRaises(build_plugin.VersionSourceMissing):
                build_plugin.get_version(src)


class TestRender(unittest.TestCase):
    def test_all_templates_parse_as_json(self):
        for name, template in build_plugin.TEMPLATES.items():
            with self.subTest(name=name):
                out = build_plugin.render(name, "9.9.9", template)
                data = json.loads(out)
                self.assertIsInstance(data, dict)
                self.assertTrue(out.endswith("\n"))
                if name in build_plugin.VERSIONED_TEMPLATES:
                    self.assertEqual(data["version"], "9.9.9")
        self.assertEqual(set(build_plugin.TEMPLATES), set(build_plugin.ALLOWED_KEYS))

    def test_check_scenarios(self):
        # render is deterministic; hooks carry the reminder from reminder.txt
        for name, template in build_plugin.TEMPLATES.items():
            self.assertEqual(build_plugin.render(name, "1.2.3", template),
                             build_plugin.render(name, "1.2.3", template))
        reminder = (ROOT / "packaging" / "hooks" / "reminder.txt").read_text(encoding="utf-8").rstrip("\n")
        for name in ("hooks/hooks.json", "hooks.json"):
            hooks = json.loads(build_plugin.render(name, "1.2.3", build_plugin.TEMPLATES[name]))
            command = hooks["hooks"]["UserPromptSubmit"][0]["hooks"][0]["command"]
            self.assertEqual(command, "echo '" + reminder.replace("'", "'\\''") + "'")

    def test_render_refuses_unknown_key(self):
        template = dict(build_plugin.TEMPLATES[".mcp.json"])
        template["frobnicate"] = True
        with self.assertRaises(build_plugin.UnknownTemplateKey) as cm:
            build_plugin.render(".mcp.json", "1.2.3", template)
        self.assertIn("frobnicate", str(cm.exception))


class TestCheckMode(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.tmp_path = Path(self.tmp.name)
        copy_packaging_inputs(self.tmp_path)

    def run_tool(self, *args):
        return subprocess.run([sys.executable, str(TOOL), *args],
                              cwd=self.tmp.name, capture_output=True, text=True,
                              check=False)

    def emit_files(self):
        proc = self.run_tool()  # no flag = emit
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_check_ok(self):
        self.emit_files()
        proc = self.run_tool("--check")
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_check_mismatch(self):
        self.emit_files()
        target = self.tmp_path / ".mcp.json"
        target.write_text(target.read_text(encoding="utf-8") + " ", encoding="utf-8")
        proc = self.run_tool("--check")
        self.assertEqual(proc.returncode, 3)
        self.assertIn(".mcp.json", proc.stdout + proc.stderr)

    def test_check_unknown_template_key(self):
        original = build_plugin.TEMPLATES
        poisoned = {name: dict(t) for name, t in original.items()}
        poisoned[".mcp.json"]["frobnicate"] = True
        build_plugin.TEMPLATES = poisoned
        self.addCleanup(setattr, build_plugin, "TEMPLATES", original)
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit) as cm:
            build_plugin.main(["--check"])
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("frobnicate", stderr.getvalue())

    def test_check_missing_version_source(self):
        (self.tmp_path / "rishi_ai_mcp.py").write_text("X = 1\n", encoding="utf-8")
        proc = self.run_tool("--check")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("version-source-missing", proc.stdout + proc.stderr)


if __name__ == "__main__":
    unittest.main()
