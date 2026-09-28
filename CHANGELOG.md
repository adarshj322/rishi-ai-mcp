# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Compact chart payloads: `cast_vedic_chart` defaults to a <4KB summary (`detail="full"` restores the complete chart).
- Three drill-down tools: `get_dasha_periods_tool`, `get_strength_table_tool`, `get_yoga_list_tool`.
- Optional `gender` parameter on `cast_vedic_chart` for interpretation framing (no calculation changes).

### Changed
- Errors now raise MCP `ToolError` instead of returning `{"error"}` data payloads.
- Tool descriptions rewritten with true output keys, full dignity enum, and drill-down pointers; README and `system_prompt.md` synced.
- Requires `dashaflow>=1.2.0`.

## [1.1.0] - 2026-04-08

### Changed
- Updated all MCP tools to return Python dictionaries directly instead of JSON strings.
- Simplified `cast_transit_chart` signature to accept raw birth details instead of requiring a serialized natal chart JSON.
- Updated agent skills, workflows, and tools documentation to reflect new parameter structures and clarify birth parameter usage.
- Removed redundant `json.loads` calls in the test suite to accommodate dictionary-based tool outputs.

## [1.0.0] - 2026-04-07

### Added
- Initial release of the RishiAI MCP Server.
- Five core MCP tools exposed via FastMCP:
  - `cast_vedic_chart`
  - `cast_transit_chart`
  - `calculate_compatibility_tool`
  - `check_muhurtha_tool`
  - `analyze_career_chart`
- Dynamic version extraction from `rishi_ai_mcp.py` via `hatchling`.
- Automated testing and PyPI publishing via GitHub Actions.
- IDE configurations for VS Code Copilot, Cursor, and Antigravity.
- Persona and skills instructions for agents.

[1.1.0]: https://github.com/adarshj322/rishi-ai-mcp/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/adarshj322/rishi-ai-mcp/releases/tag/v1.0.0
