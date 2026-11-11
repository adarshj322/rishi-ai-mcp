#!/usr/bin/env python3
"""
Generate (default) or verify (--check) the per-host plugin manifests.

All seven artifacts are rendered in-memory from TEMPLATES with the
__version__ read from rishi_ai_mcp.py, so they can never drift from
each other or from __version__.

  python tools/build_plugin.py           emit the seven manifests (cwd-relative)
  python tools/build_plugin.py --check   compare committed files, write nothing

Exit codes: 0 ok, 3 mismatch, 1 unknown template key, 2 version source missing.

The hook reminder line is read from packaging/hooks/reminder.txt at render
time (cached), not at import, so --help/import never need it.
"""

import argparse
import ast
import copy
import hashlib
import json
import shutil
import sys
from pathlib import Path

VERSIONED_TEMPLATES = ("plugin/.claude-plugin/plugin.json", "plugin/.codex-plugin/plugin.json")

ALLOWED_KEYS = {
    ".claude-plugin/marketplace.json": {"name", "owner", "plugins"},
    ".agents/plugins/marketplace.json": {"name", "plugins"},
    ".mcp.json": {"mcpServers"},
    "hooks/hooks.json": {"hooks"},
    "hooks.json": {"hooks"},
    "plugin/.claude-plugin/plugin.json": {
        "name", "version", "description", "author", "homepage", "repository",
        "license", "keywords",
    },
    "plugin/.codex-plugin/plugin.json": {
        "name", "version", "description", "author", "homepage", "repository",
        "license", "keywords", "skills", "mcpServers", "interface",
    },
    "plugin/.mcp.json": {"mcpServers"},
    "plugin/hooks/hooks.json": {"hooks"},
    "plugin/hooks.json": {"hooks"},
}


class VersionSourceMissing(Exception):
    """rishi_ai_mcp.py is absent/unparseable or has no simple string __version__."""


class UnknownTemplateKey(Exception):
    """A template carries a top-level key the manifest schema does not know."""


_reminder_cache: str | None = None


def _load_reminder() -> str:
    global _reminder_cache
    if _reminder_cache is None:
        path = Path("packaging/hooks/reminder.txt")
        try:
            _reminder_cache = path.read_text(encoding="utf-8").rstrip("\n")
        except OSError as exc:
            raise RuntimeError(
                f"packaging/hooks/reminder.txt is required "
                f"(single source of truth for the hook line): {exc}"
            ) from exc
    return _reminder_cache

_DISPLAY_NAME = "RishiAI — Ground-Truth Vedic Astrology"
_CLAUDE_PLUGIN_BASE = {
    "name": "rishi-ai",
    "description": "Ground-truth Vedic astrology: doctrine + contract + deterministic tools, in your harness.",
    "author": {"name": "Adarsh J"},
    "homepage": "https://github.com/adarshj322/rishi-ai-mcp",
    "repository": "https://github.com/adarshj322/rishi-ai-mcp",
    "license": "MIT",
    "keywords": ["vedic-astrology", "jyotish", "astrology", "ground-truth", "mcp", "plugin"],
}


def _hooks_template() -> dict:
    reminder = _load_reminder()
    command = "echo " + "'" + reminder.replace("'", "'\\''") + "'"
    return {
        "hooks": {
            "UserPromptSubmit": [
                {"hooks": [{"type": "command", "command": command}]}
            ]
        }
    }


HOOK_TEMPLATES = ("hooks/hooks.json", "hooks.json", "plugin/hooks/hooks.json", "plugin/hooks.json")
MCP_TEMPLATES = (".mcp.json", "plugin/.mcp.json")

# Fixed content; render() injects __version__ into VERSIONED_TEMPLATES.
# Hooks entries are built at render time (see render()) so that importing
# this module never reads packaging/hooks/reminder.txt.
TEMPLATES = {
    ".claude-plugin/marketplace.json": {
        "name": "rishi-ai-mcp",
        "owner": {"name": "Adarsh J"},
        "plugins": [
            {
                "name": "rishi-ai",
                "source": "./plugin",
                "description": "Ground-truth Vedic astrology plugin",
            }
        ],
    },
    "plugin/.claude-plugin/plugin.json": {
        **_CLAUDE_PLUGIN_BASE,
    },
    "plugin/.codex-plugin/plugin.json": {
        **_CLAUDE_PLUGIN_BASE,
        "skills": "./skills/",
        "mcpServers": "./.mcp.json",
        "interface": {"displayName": _DISPLAY_NAME, "category": "Productivity"},
    },
    "plugin/.mcp.json": {
        "mcpServers": {
            "vedic-astrology": {"command": "uvx", "args": ["rishi-ai-mcp"]}
        }
    },
    "plugin/hooks/hooks.json": {},
    "plugin/hooks.json": {},
    ".agents/plugins/marketplace.json": {
        "name": "rishi-ai-mcp",
        "plugins": [
            {
                "name": "rishi-ai",
                "source": {"source": "local", "path": "plugin"},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": "Productivity",
            }
        ],
    },
    # unpinned during development; the release flow pins the version
    ".mcp.json": {
        "mcpServers": {
            "vedic-astrology": {"command": "uvx", "args": ["rishi-ai-mcp"]}
        }
    },
    "hooks/hooks.json": {},  # built at render time via _hooks_template()
    "hooks.json": {},
}


def get_version(path: Path = Path("rishi_ai_mcp.py")) -> str:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except OSError as exc:
        raise VersionSourceMissing(f"cannot read {path}: {exc}") from exc
    except SyntaxError as exc:
        raise VersionSourceMissing(f"cannot parse {path}: {exc}") from exc
    for node in tree.body:  # top-level statements only
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(t, ast.Name) and t.id == "__version__" for t in node.targets):
            continue
        value = node.value
        if isinstance(value, ast.Constant) and isinstance(value.value, str):
            return value.value
        raise VersionSourceMissing(f"__version__ in {path} is not a simple string constant")
    raise VersionSourceMissing(f"no top-level __version__ assignment in {path}")


def render(name: str, version: str, template: dict) -> str:
    allowed = ALLOWED_KEYS.get(name)
    if allowed is None:
        raise UnknownTemplateKey(f"{name}: unknown template")
    if name in HOOK_TEMPLATES:
        template = _hooks_template()
    for key in template:
        if key not in allowed:
            raise UnknownTemplateKey(f"{name}: unknown key {key!r}")
    out = copy.deepcopy(template)
    if name in VERSIONED_TEMPLATES:
        out = {"name": out.pop("name"), "version": version, **out}
    if name in MCP_TEMPLATES:
        out["mcpServers"]["vedic-astrology"]["args"] = [f"rishi-ai-mcp=={version}"]
    return json.dumps(out, indent=2, ensure_ascii=False) + "\n"


def render_all(version: str) -> dict:
    return {name: render(name, version, template) for name, template in TEMPLATES.items()}


PLUGIN_ROOT = Path("plugin")


def _tree_digest(path: Path) -> dict:
    digest = {}
    if not path.is_dir():
        return digest
    for file in sorted(path.rglob("*")):
        if file.is_file():
            digest[str(file.relative_to(path))] = hashlib.sha256(file.read_bytes()).hexdigest()
    return digest


def sync_plugin_tree() -> None:
    """Mirror the shipped skills into the plugin bundle; manifests are rendered."""
    source = Path("skills")
    target = PLUGIN_ROOT / "skills"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)


def plugin_tree_errors() -> list:
    errors = []
    for forbidden in ("agents", "evals"):
        if (PLUGIN_ROOT / forbidden).exists():
            errors.append(f"plugin tree contains forbidden path: plugin/{forbidden}")
    if _tree_digest(Path("skills")) != _tree_digest(PLUGIN_ROOT / "skills"):
        errors.append("plugin tree drift: plugin/skills does not match skills/")
    return errors


def check() -> int:
    try:
        version = get_version()
    except VersionSourceMissing as exc:
        print(f"version-source-missing: {exc}", file=sys.stderr)
        return 2
    try:
        rendered = render_all(version)
    except UnknownTemplateKey as exc:
        print(f"unknown-template-key: {exc}", file=sys.stderr)
        return 1
    mismatch = [name for name, content in rendered.items()
                if not Path(name).is_file() or Path(name).read_text(encoding="utf-8") != content]
    for name in mismatch:
        print(f"manifest drift: {name}")
    for error in plugin_tree_errors():
        print(error)
        mismatch.append(error)
    return 3 if mismatch else 0


def emit() -> int:
    try:
        version = get_version()
    except VersionSourceMissing as exc:
        print(f"version-source-missing: {exc}", file=sys.stderr)
        return 2
    try:
        rendered = render_all(version)
    except UnknownTemplateKey as exc:
        print(f"unknown-template-key: {exc}", file=sys.stderr)
        return 1
    for name, content in rendered.items():
        path = Path(name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    sync_plugin_tree()
    return 0


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        description="Emit the per-host plugin manifests (default), or verify them.",
    )
    parser.add_argument("--check", action="store_true",
                        help="compare committed manifests against the templates; write nothing")
    args = parser.parse_args(argv)
    try:
        code = check() if args.check else emit()
    except RuntimeError as exc:  # packaging/hooks/reminder.txt missing
        print(exc, file=sys.stderr)
        sys.exit(1)
    sys.exit(code)


if __name__ == "__main__":
    main()
