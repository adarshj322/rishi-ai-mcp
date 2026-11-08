# RishiAI — Ground-Truth Vedic Astrology

[![PyPI version](https://img.shields.io/pypi/v/rishi-ai-mcp.svg?cache=1)](https://pypi.org/project/rishi-ai-mcp/)
[![CI](https://github.com/adarshj322/rishi-ai-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/adarshj322/rishi-ai-mcp/actions/workflows/ci.yml)
[![Python versions](https://img.shields.io/pypi/pyversions/rishi-ai-mcp.svg?cache=1)](https://pypi.org/project/rishi-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Vedic astrology tools powered by the [DashaFlow](https://github.com/adarshj322/dashaflow) calculation engine, served over the [Model Context Protocol](https://modelcontextprotocol.io/) — plus the **ground-truth reading contract** those tools are read under: doctrine that binds the interpreter, a verifier pass on high-stakes slices, and an auditable output format.

Works over **stdio** — as a plugin in Claude Code and Codex, or as a pip-installed MCP server for any other MCP-compatible client.

https://github.com/user-attachments/assets/9c183b94-bb54-4af6-867c-fa3daeef2d03

## Install

### A. Host install — Claude Code (plugin) · Codex (MCP + skill) · OpenCode (MCP + skill)

**Claude Code**

```bash
/plugin marketplace add adarshj322/rishi-ai-mcp
/plugin install rishi-ai@rishi-ai-mcp
```

**Codex** (CLI v0.128.0, verified 2026-11-08)

```bash
codex plugin marketplace add adarshj322/rishi-ai-mcp
```

**Limit:** this CLI version ships only `marketplace` subcommands — no `plugin add`, `plugin list`, or `plugin install`. The marketplace registers, and the repo carries `.codex-plugin/plugin.json` + root `hooks.json` + `.agents/plugins/marketplace.json` for when a newer CLI adds install support, but **Codex cannot install the plugin bundle from the CLI today**. The working path is pip + a copied skill (no clone needed):

```bash
pip install rishi-ai-mcp
SRC=$(python -c "import rishi_ai_mcp, os; print(os.path.join(os.path.dirname(rishi_ai_mcp.__file__), 'skills', 'rishi-reading'))")
mkdir -p ~/.codex/skills/rishi-reading
cp -r "$SRC/SKILL.md" "$SRC/contract.md" "$SRC/references" ~/.codex/skills/rishi-reading/
```

`~/.codex/config.toml` needs:

```toml
[mcp_servers.vedic-astrology]
command = "uvx"
args = ["rishi-ai-mcp"]
```

Verify with `codex mcp list` (shows `vedic-astrology ... enabled`). The two verification subagent definitions (`agents/chart-verifier.md`, `agents/doctrine-critic.md`) ship in the plugin bundle and the repo — not in the pip wheel; fetch them from the repo if you want them as reference. No verification binding ships on this path; the contract is read, not enforced.

What the plugin ships:

- `skills/rishi-reading/SKILL.md` + `skills/rishi-reading/references/*.md` — the doctrine, auto-discovered by the host
- `agents/chart-verifier.md` and `agents/doctrine-critic.md` — bounded verification subagents (gated; see Limitations)
- `hooks/hooks.json` (Claude Code; Codex uses root `hooks.json`) — a one-line `UserPromptSubmit` reminder. Echo only, no side effects
- `.mcp.json` — wires `uvx rishi-ai-mcp`. The plugin bundle carries no Python; the package is resolved on first run

Verified: Claude Code plugin install cached at 1.6.0 with skill, agent definitions, reminder hook, and `.mcp.json` all present; `claude mcp list` shows `vedic-astrology: connected`.

The plugin doctrine is built around **5 tools by design**: `cast_vedic_chart`, `cast_transit_chart`, `calculate_compatibility_tool`, `check_muhurtha_tool`, `analyze_career_chart`. The pip-installed server exposes all 12 (the remaining 7 are drill-downs — see MCP Tools).

### B. pip — everything else

```bash
pip install rishi-ai-mcp
```

- Console script: `rishi-ai-mcp`
- Exposes **all 12 tools** over stdio
- The doctrine is vendored into the wheel at `<site-packages>/skills/rishi-reading/` (`contract.md` + `references/`). Read it directly, or paste it into your host's system-prompt field; `system_prompt.md` in this repo is a minimap that points at it
- Lahiri ayanamsha by default; other variants are named, never mixed

### OpenCode (verified 2026-11-08 on v2.2.6)

No plugin bundle ships for OpenCode — a plugin cannot register an MCP server or a skills directory (verified against the plugin API), so there is nothing to `npx install`. The working path is the same two pieces by hand (no clone needed):

```bash
pip install rishi-ai-mcp
SRC=$(python -c "import rishi_ai_mcp, os; print(os.path.join(os.path.dirname(rishi_ai_mcp.__file__), 'skills', 'rishi-reading'))")
mkdir -p ~/.config/opencode/skills/rishi-reading
cp -r "$SRC/SKILL.md" "$SRC/contract.md" "$SRC/references" ~/.config/opencode/skills/rishi-reading/
```

Then add to `~/.config/opencode/opencode.jsonc`, inside the top-level `"mcp"` object (flat keys — a nested `mcp.servers` object is ignored):

```jsonc
"vedic-astrology": {
  "type": "local",
  "command": ["uvx", "rishi-ai-mcp"]
},
```

**Verified:** the session then lists `rishi-reading` in its available skills, and `opencode mcp list --print-logs` reports `vedic-astrology: connected`. No verification binding ships this way — the contract is read; it is not enforced. (The doctrine covers 5 core tools by design; the pip server itself exposes all 12 — see MCP Tools.)

### Other harnesses — Gemini CLI, VS Code Copilot, Cursor, Roo/Kilo

Docs path only: `pip install rishi-ai-mcp`, add the stdio server per your host's MCP documentation, and adapt `system_prompt.md` to the host's instruction format. These are **not** plugins; there is **no verification binding**; the doctrine ships as text, not as an enforced contract.

> **Warning:** there is no published npm/`npx` package and no plugin bundle outside this repository. Any third-party copy of "rishi-ai-mcp" — a fork, a repackaging, a registry listing — is unaffiliated and unverified. Install from this repo or from PyPI only.

## Quick Start

```bash
rishi-ai-mcp                    # console entry point (after pip install)
python rishi_ai_mcp.py          # or run directly from source
```

Communicates over **stdio**. Any MCP client that can spawn a subprocess and speak MCP can use it — no IDE required. Plugin installs skip this step; the plugin wires the server for you.

## MCP Tools

The server exposes **all 12 tools** over stdio. The plugin doctrine is built around 5 by design — `cast_vedic_chart`, `cast_transit_chart`, `calculate_compatibility_tool`, `check_muhurtha_tool`, `analyze_career_chart`; the rest are drill-downs documented for the pip path.

### `cast_vedic_chart`

Generates a Vedic natal chart. Compact by default (<4KB), full on request.

| Parameter | Type | Description |
|-----------|------|-------------|
| `dob` | string | Date of birth — `"YYYY-MM-DD"` |
| `time` | string | Time of birth — `"HH:MM[:SS]"` (24-hour; seconds optional) |
| `lat` | float | Birth latitude (e.g. `28.6139` for Delhi) |
| `lon` | float | Birth longitude (e.g. `77.2090` for Delhi) |
| `timezone` | string | IANA timezone (e.g. `"Asia/Kolkata"`) |
| `query_date` | string | Optional — date for Dasha lookup, defaults to today |
| `detail` | string | `"compact"` (default) or `"full"` |
| `gender` | string | Optional — `"male"` / `"female"`, interpretation framing only |

**Returns (compact):** `lagna`, condensed `planets` (sign/house/nakshatra/dignity + vargottama/yogakaraka flags), active dasha lords (Vimshottari/Yogini/Chara), yoga names, strength totals, SAV, dosha flags, `time_sensitivity` verdict (robust/borderline/fragile) — each section naming its drill-down tool.

**Returns (full):** JSON with `metadata`, `panchang`, `lagna` (with D2–D60 signs), `planets` (with dignity, combustion, Shadbala, all 14 Varga signs, aspects), `dashas` (5 levels: Maha/Antar/Pratyantar/Sukshma/Prana + timeline), `yogini_dasha`, `chara_dasha`, `yogas` (24 detections), `ashtakavarga` (SAV + BAV + Prashtara), `sodhita_ashtakavarga` (reduced + Sodhya Pinda), `jaimini_karakas`, `shadbala` (with Ishta/Kashta Phala), `vimshopaka`, `bhava_chalit`, `avasthas`, `kaal_sarpa`, `graha_yuddha`, `gandanta`, `arudha_padas` (A1–A12), `upapada`, `karakamsha`.

Errors raise MCP `ToolError` (no `{"error"}` data payloads).

### `get_dasha_periods_tool`, `get_strength_table_tool`, `get_yoga_list_tool`, `get_time_sensitivity_tool`

Drill-downs for the compact chart: full dasha chains with dates (all 3 systems), per-planet strength components, full yoga entries, birth-time sensitivity (robust/borderline/fragile verdict with notes). Same birth parameters as `cast_vedic_chart`; time accepts `"HH:MM[:SS]"`.

### `cast_transit_chart`

Calculates planetary transits overlaid on a natal chart.

| Parameter | Type | Description |
|-----------|------|-------------|
| `transit_date` | string | Date to compute transits — `"YYYY-MM-DD"` |
| `dob` | string | Date of birth — `"YYYY-MM-DD"` |
| `time` | string | Time of birth — `"HH:MM"` (24-hour) |
| `lat` | float | Birth latitude |
| `lon` | float | Birth longitude |
| `timezone` | string | Optional — defaults to `"Asia/Kolkata"` |

**Returns:** JSON with transit `planets` (sign, degree, nakshatra, `sav_points`, house from Lagna/Moon), `sade_sati` status and phase, and `rahu_ketu_axis`.

### `get_transit_ingresses_tool`, `get_sade_sati_timeline_tool`, `get_gochara_tool`

Timing tools for "when" questions. Same birth parameters as `cast_vedic_chart`; time accepts `"HH:MM[:SS]"`.

| Tool | Parameters | Returns |
|------|------------|---------|
| `get_transit_ingresses_tool` | `start_date`, `end_date` (inclusive, 15-year cap), optional `bodies` (default Jupiter/Saturn/Rahu) | Chronological `ingresses` with local `date`, `instant_utc`, `from_sign`/`to_sign`, `direction`, houses from Lagna/Moon. Retrograde re-entries appear separately. Moon is rejected. |
| `get_sade_sati_timeline_tool` | `start_date`, `end_date`, optional `merge_gap_days` (default 180) | `spans` (rising/peak/setting with `days`, `gap_days`, `in_phase_days`, `interruptions`, clipped-range flags), `active_at_start`/`active_at_end`, and every Saturn `crossings` entry. |
| `get_gochara_tool` | `transit_date` | Per-planet `house_from_moon`, `sav_points`, `house_quality`, `weighted_verdict` (favorable/mixed/unfavorable), and explanatory `notes`. Rahu/Ketu notes carry the "Raman convention (nodes)" provenance. |

### `calculate_compatibility_tool`

Calculates 16-factor compatibility + Kuja Dosha. Person 1 = Male, Person 2 = Female.

| Parameter | Type | Description |
|-----------|------|-------------|
| `dob1`, `time1`, `lat1`, `lon1`, `tz1` | various | Birth details for Person 1 (Male) |
| `dob2`, `time2`, `lat2`, `lon2`, `tz2` | various | Birth details for Person 2 (Female) |

**Returns:** 8 Ashtakoot kutas (36 pts), additional kutas (Mahendra, Stree Deergha, Vedha, Rajju, BadConstellations, LagnaHouse7, SexEnergy), exception logic, and Kuja Dosha analysis.

### `check_muhurtha_tool`

Evaluates whether a date/time is auspicious for a specific activity (electional astrology).

| Parameter | Type | Description |
|-----------|------|-------------|
| `activity` | string | One of: `marriage`, `travel`, `business`, `education`, `house_entry`, `medical` |
| `date` | string | Date to evaluate — `"YYYY-MM-DD"` |
| `time` | string | Time to evaluate — `"HH:MM"` (24-hour) |
| `lat` | float | Location latitude |
| `lon` | float | Location longitude |
| `timezone` | string | IANA timezone string |

**Returns:** JSON with `verdict`, `score`, `positive_factors`, `negative_factors`, `panchang_suddhi`, and `marriage_doshas` (for marriage activity).

### `analyze_career_chart`

Analyzes career potential using the 10th house, D10 Dashamsha, and planetary significations.

| Parameter | Type | Description |
|-----------|------|-------------|
| `dob` | string | Date of birth — `"YYYY-MM-DD"` |
| `time` | string | Time of birth — `"HH:MM"` (24-hour) |
| `lat` | float | Birth latitude |
| `lon` | float | Birth longitude |
| `timezone` | string | IANA timezone string |

**Returns:** JSON with `tenth_house` info, `d10_indicators`, `career_themes`, and `strength_factors`.

## The RishiAI persona (ground truth, not flattery)

RishiAI is a Vedic astrologer (Jyotishi) bound by an explicit contract rather than by vibe. The model is an **interpreter of tool-computed chart data — never a calculator**, working under *Brihat Parashara Hora Shastra* with Desh–Kaal–Patra (person, time, place, circumstance) framing. Birth details come first or not at all; positions, dashas, and divisional charts are never computed by hand — only the tools speak for the chart.

**What it honestly claims:** the consistency and auditability of its interpretation. Every factual claim cites its chart grounds — planet, sign, house, degree, dignity, shadbala, dasha window — or is tagged UNSUPPORTED and cut or printed beside the tag. Its compute layer is checkable: sidereal positions (Lahiri ayanamsha default) via Swiss Ephemeris/pyswisseph, deterministic run to run. Its reading layer is auditable: every reading ends with a grounds appendix, a calibration footer, a disagreement log, and a provenance line — the artifacts make the reading checkable by anyone, not trusted by default.

**What it honestly refuses:** certainty about the future. No claim in this repository licenses telling someone what will happen to them; the correspondence layer is out of scope until a preregistered prospective registry exists (it does not yet). It refuses medical, legal, or financial advice — those get gentle language and a professional. It never states or hints longevity probabilities; maraka periods read only as deep transformation. It carries no fear framing, never sells or bundles remedies, and treats "no remedy needed" as a valid — often correct — output.

The contract — [`skills/rishi-reading/contract.md`](skills/rishi-reading/contract.md) — in one line each:

1. **R1 Falsifiability** — every claim cites its chart grounds or is tagged UNSUPPORTED; the grounds appendix prints in every reading.
2. **R2 Uncertainty** — stated in plain words, scored by a separate pass, never as a numeric self-report; the footer counts what was withheld and flagged.
3. **R3 Discriminating agreement** — never retract a tool-supported claim under challenge without new grounds; never adopt a user premise the chart contradicts.
4. **R4 Forbidden behaviors** — no fear framing; never a death/longevity probability; medical/financial/crisis deferral to professionals; five checkable-error refusal triggers.
5. **R5 Remedy restraint** — matched remedies only, after the facts; "no remedy needed" is always a valid output.
6. **R6 Accountability** — grounds appendix + calibration footer + disagreement log + provenance line in every reading; provenance missing means not a valid reading.

How a reading actually unfolds — intake, cast-before-counsel, verify-by-default on high-stakes slices — lives in the entry skill [`skills/rishi-reading/SKILL.md`](skills/rishi-reading/SKILL.md) and its `references/`. Plugin hosts auto-discover it; pip installs get it vendored in the wheel. Where any file disagrees with the contract, the contract wins.

High-stakes slices — marriage, health, career, remedies, fear content — route through the gated verification pair (`agents/chart-verifier.md` re-derives each cited value from tool output; `agents/doctrine-critic.md` checks the prose against the contract). Verification is currently **off** until the pre-committed equal-cost bar clears — see [`evals/README.md`](evals/README.md) and [Limitations](#limitations).

## Architecture

```
rishi_ai_mcp.py            MCP server — all 12 tools, stdio, single file
  └── dashaflow (pip)      Calculation engine — Swiss Ephemeris via pyswisseph, Moshier fallback (no .se1 files)
        ├── vedic_calculator   Swiss Ephemeris core
        ├── constants          Zodiac, nakshatras, dignities
        ├── panchang           Tithi, Vara, Yoga, Karana
        ├── yoga               24 yoga types + Kaal Sarpa, Graha Yuddha, Gandanta
        ├── dasha              Vimshottari 5-level
        ├── dignity            Dignity, combustion, digbala
        ├── ashtakavarga       SAV, BAV, Prashtara
        ├── jaimini            Karakas, Arudha Padas, Upapada, Karakamsha
        ├── shadbala           Six-fold strength + Ishta/Kashta
        ├── matchmaking        16-factor compatibility + Kuja Dosha
        ├── muhurtha           Electional astrology
        └── career             D10 career analysis

skills/rishi-reading/       Doctrine — contract.md + references/ (entry skill auto-discovered by plugin hosts;
                            vendored into the wheel for pip installs)
agents/                     chart-verifier.md, doctrine-critic.md — gated verification (off until the
                            equal-cost bar clears; see evals/README.md)
evals/                      JyotishQA seed set + Tier-1 conformance corpus (300 moments) + the gate pre-commitment
tools/build_plugin.py       Renders and verifies the per-host manifests (--check runs in CI)
tools/tier1_check.py        Tier-1 determinism gate (dual invocation, 300 moments)
.claude-plugin/             Claude Code — plugin.json + marketplace.json (auto-discovers skills/, agents/, hooks/)
.codex-plugin/              Codex — plugin.json (skills/ and mcpServers pointers + interface block)
.agents/plugins/            Codex marketplace catalog
hooks/hooks.json            Claude Code reminder hook (UserPromptSubmit; echo only, no side effects)
hooks.json                  Codex reminder hook (repo root; Codex does not read hooks/hooks.json)
.mcp.json                   uvx rishi-ai-mcp wiring (unpinned until the release flow pins it)
system_prompt.md            Minimap for non-plugin hosts — points at the vendored contract
AGENTS.md                   Doctrine pointer for agent harnesses
```

## Limitations

Stated plainly, because a reading tool that overclaims is worse than none:

- **No ephemeris files.** The engine computes through pyswisseph's **Moshier fallback** (no `.se1` data files). Positions are ~1″-class and deterministic run to run — adequate for Jyotish sign/degree work, but this is not a Swiss Ephemeris Professional setup and no such claim is made.
- **No astronomical-truth verification.** The Tier-1 corpus (300 pinned moments, 1900–2030) is a regression and determinism gate — the same input produces the same output, path to path. It verifies determinism, not astronomical truth, and must not be cited as doing so.
- **Lahiri ayanamsha by default.** Other variants are named when used; systems are never mixed within one reading.
- **No predictions.** No claim here licenses telling someone what will happen. There is no ground truth for outcomes; the correspondence layer is out of scope until a preregistered prospective registry exists — it does not yet.
- **No interpretive-validity claim.** What a placement means is an interpretation under a stated rulebook, not a measured fact. The claim is consistency and auditability of interpretation — nothing more.
- **Verification is off by default.** The plugin ships with the verification path disabled. It unlocks only if the pre-committed equal-cost bar clears — delta > seed-set standard error at first measurement, locked, with the set expanded rather than the bar relaxed; the bar is written down in [`evals/README.md`](evals/README.md) before any run. Until then, sample-and-vote plus the deterministic tool-check is what ships.
- **Not medical, legal, or financial advice.** The chart may frame themes; it may not triage, dose, or time treatment. Crisis language routes to professionals and crisis resources, never to a chart.
- **OpenCode and other hosts get no binding.** Outside the two plugin hosts, the contract is documentation, not enforcement — the tools and doctrine text are real, but nothing gates the reading.

## Prerequisites

- **Python 3.10+**
- **dashaflow** — installed automatically as a dependency
- **mcp** — installed automatically as a dependency
- Plugin installs: [`uv`](https://docs.astral.sh/uv/) (for `uvx`) — no local Python environment needed for the doctrine; `uvx` resolves the package on first run

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). House rules: new tools go through `dashaflow` first; the single-file `rishi_ai_mcp.py` pattern stays; run `pytest -q` and `ruff --select E,F,W,I,UP,B --ignore E501 .` before opening a PR.

## License

MIT — see [LICENSE](LICENSE).
