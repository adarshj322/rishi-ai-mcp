#!/usr/bin/env python3
"""Stamp the build commit into rishi_ai_mcp.py before a release build."""

import argparse
import re
import subprocess
import sys
from pathlib import Path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", default="rishi_ai_mcp.py")
    parser.add_argument("--commit", default="", help="override git rev-parse HEAD")
    args = parser.parse_args(argv)

    commit = args.commit
    if not commit:
        try:
            commit = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], text=True
            ).strip()
        except (OSError, subprocess.CalledProcessError) as exc:
            print(f"stamp-commit: cannot read git HEAD: {exc}", file=sys.stderr)
            return 1
    if not re.fullmatch(r"[0-9a-f]{7,40}", commit):
        print(f"stamp-commit: invalid commit {commit!r}", file=sys.stderr)
        return 1

    path = Path(args.file)
    text = path.read_text(encoding="utf-8")
    updated, count = re.subn(
        r'^__commit__ = ".*"$', f'__commit__ = "{commit}"', text, flags=re.M
    )
    if count != 1:
        print("stamp-commit: expected exactly one __commit__ assignment",
              file=sys.stderr)
        return 1
    path.write_text(updated, encoding="utf-8")
    print(f"stamped {path} @ {commit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
