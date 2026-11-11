"""Tests for tools/stamp_commit.py — release build commit stamping."""

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import stamp_commit  # noqa: E402


class TestStampCommit(unittest.TestCase):
    def _write(self, tmp, commit="unknown"):
        path = Path(tmp) / "rishi_ai_mcp.py"
        path.write_text(
            f'__version__ = "1.2.3"\n__commit__ = "{commit}"\n', encoding="utf-8"
        )
        return path

    def test_stamps_commit(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(tmp)
            self.assertEqual(
                stamp_commit.main(["--file", str(path), "--commit", "deadbeef"]), 0
            )
            self.assertIn('__commit__ = "deadbeef"', path.read_text(encoding="utf-8"))

    def test_rejects_invalid_commit(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(tmp)
            self.assertEqual(
                stamp_commit.main(["--file", str(path), "--commit", "not-a-sha"]), 1
            )
            self.assertIn('__commit__ = "unknown"', path.read_text(encoding="utf-8"))

    def test_requires_one_assignment(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "rishi_ai_mcp.py"
            path.write_text('__version__ = "1.2.3"\n', encoding="utf-8")
            self.assertEqual(
                stamp_commit.main(["--file", str(path), "--commit", "deadbeef"]), 1
            )
