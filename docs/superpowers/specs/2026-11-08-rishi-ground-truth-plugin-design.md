# RishiAI Ground-Truth Plugin — Design (v0 + v1, everywhere-hosted)

Date: 2026-11-08
Status: proposed (awaiting owner approval)
Brief: `research/notes/final_report_rishi-plugin-ground-truth-bc68ed.md` (full-tier hyperresearch run, `rishi-plugin-ground-truth-bc68ed`). This design implements **Approach B** — the report's thin bundle — not a fresh invention. Where the report and this doc disagree, the report wins unless this doc says why.

## Intent — why this exists

Ship rishi-ai-mcp as something other people install for **accurate prediction**, and its owner uses personally, in Claude Code, Codex, and documented other harnesses — while eliminating the yes-man posture the RishiAI persona currently ships ("world's greatest Vedic Astrologer", universal praise, no refusal discipline).

The means: a versioned **plugin** that bundles doctrine, the deterministic calculations, the checking discipline, and the update story — one unit, because doctrine, calculators, checkers and guards must version together or the ground-truth claim is unverifiable across installs.

The honesty constraint inherited from the brief: **computational conformance can be claimed now and forever; interpretive agreement only with a blinded panel and a built Vedic agreement dataset (v2); correspondences never without a preregistered prospective registry (v3). Null ledger in-product. No sugar-coating — ours included.**

## Goals

1. One repo ships **the plugin**, installable on:
   - **Claude Code**: `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json`; `.mcp.json` (project-file shape: `{"mcpServers": {…}}`) at plugin root; Claude `hooks/hooks.json`; `skills/` + `agents/` auto-discovered. `claude plugin validate` run in CI (**routes manifest schema only — it does NOT validate `.mcp.json` or hooks**; the clean-install drill covers those).
   - **Codex CLI**: `.codex-plugin/plugin.json` carrying `"skills": "./skills/"` and `"mcpServers": "./.mcp.json"` plus a figma-style `interface` display block; repo-root `hooks.json` (Codex does not read `hooks/hooks.json`); `.agents/plugins/marketplace.json` with `name`/`source`/`policy`/`category`; install documented via `codex plugin marketplace add adarshj322/rishi-ai-mcp`.
   - **OpenCode** (docs path, not a package): git-clone into `.opencode/` / `~/.config/opencode/` + `opencode mcp add rishi-ai-mcp -- uvx rishi-ai-mcp`; no npm payload shipped in this phase; dogfood-first gate.
   - **Other famous harnesses**: README install paths via pip + host instructions (single source: doctrine ships in the wheel, see Goal 5). No plugin; honesty stated.

2. **`rishi-reading`** — one entry skill, description recall-scoped to reading/chart/astrology/jyotish; Jyotish doctrine + contract behind `references/` (progressive disclosure). **One skill ships; no `rishi-compat` in v1.**
3. **Six-rule contract** in `skills/rishi-reading/contract.md` (falsifiability, uncertainty disclosure in words scored by a separate judge, discriminating agreement, forbidden behaviors, remedy restraint, accountability) + five checkable-error refusal triggers. `AGENTS.md` / `system_prompt.md` / `CLAUDE.md` pointer-reference it; they never duplicate it.
4. **Gated verification per-turn (v1)** — R0 decomposition → hesitation gate → V1 parallel aspect-verifiers (tool-bound, binary per-claim approvals) → one centralized calibrated judge → V2 bounded re-check (`task_ids`-locked; renamed to avoid collision with contract R2, uncertainty). Hard caps (≤2 rounds, ~3× single-draft tokens). iMAD-style gating: verify only when the signal says so.
5. **Doctrine in the wheel**: `package.json`/`pyproject` extended so the wheel ships `skills/rishi-reading/**` (contract + references). `system_prompt.md` is a short minimap pointing at the vendored doctrine. Docs-path users still get the real files (e.g. `<site-packages>/rishi_ai_mcp/skills/…`) — they paste to hosts' system-prompt fields.
6. **Repo persona rewritten** — `AGENTS.md`, `system_prompt.md`, a `CLAUDE.md` dated after this design contains only pointers; `.claude/` repo-local ignored artifacts retained; **delete the 16 directories under `.agents/skills/` after mining refusal triggers and deterministic tool-order steps into doctrine**; `.agents/workflows/*`, `.agents/rules/rishi-ai.md` protected via the same migration; `.github/copilot-instructions.md` + `.cursor/rules/*.mdc` rewritten to point at the contract; `kilo.json` untouched.
7. **Eval harness in-repo**.
8. **Distribution docs locked**: plugin is a complete unit; pip path is a documented secondary.

## Non-goals

- No scripts inside skills beyond the single pre-committed reminder text hook; **no code hook bodies in v1** (deviation from brief accepted explicitly if owner disagrees: this design cuts to reminder-only).
- No remote/SSE/OAuth MCP transport; no secrets; stdio only.
- No `.se1` files; no Swiss Ephemeris Professional license purchase; **Moshier fallback, ~1″ bound, honored in-product** (owner: "roughly ~1% accuracy is fine").
- No second reading-type skill; no JyotishQA benchmark publication claims; no Tier-3 language.
- No OpenCode npm publish this phase; no MCP Registry submission on critical path (optional, same session if trivial).
- No reimplementation of DashaFlow; `dashaflow>=1.5` stays the dependency.

## Anti-goals

- Sycophancy with extra installation steps.
- Verification shipped without clearing the pre-committed equal-cost bar (measured, reported in `evals/README.md`); failing means verification off, sample-and-vote + tool-check ships instead — pre-commitment, not a judge call later.
- A plugin that installs but asserts placements the ephemeris contradicts.
- "World's greatest astrologer" / prophecy language anywhere in shipped text.
- Per-host drift: manifest lockstep is a build check, not a hope.

## Constraints

- Single-file `rishi_ai_mcp.py` pattern preserved; plugin `.mcp.json` wires only the 5 report-named tools (**owner decision**), remaining 7 exposed to pip users manually (documented, not silently dropped).
- `rishi-ai-mcp` stays pip-installable; **wheel ships `rishi_ai_mcp.py` + `skills/rishi-reading/**`**. Plugin wiring: `uvx rishi-ai-mcp@X.Y.Z` at config level (the plugin itself carries no Python).
- Python ≥ 3.10; CI matrix 3.10–3.13; ruff `E,F,W,I,UP,B`; `zip()` strict=.
- Version lockstep: `__version__` in `rishi_ai_mcp.py` (hatch build source) == tag == PyPI == both plugins' manifests. CI: if PyPI release for the tag is missing **before** tag publish, build fails (prevents marketplace installs that `uvx` cannot resolve).
- No network at runtime except first `uvx` resolve; no telemetry; no remote transports.
- AGENTS.md highest-priority rules retained (never fabricate chart data; tool binding).

## Approaches (and why B)

- **A** — persona rewrite, MCP-only: rejected ("not just an MCP" ask; doctrine not version-locked to tools).
- **B** — thin bundle (chosen): one entry skill + refs, 2 subagents, reminder-only hook, 5 plugin tools, per-host manifests from one source, eval gate.
- **C** — hyperresearch-per-turn: rejected (manufactured consensus; latency).

## The design

### Repo layout after the change

```
rishi-ai-mcp/
  rishi_ai_mcp.py          # unchanged tools; version source
  pyproject.toml           # only-include = rishi_ai_mcp.py + skills/rishi-reading/**
  evals/
    tier1/                 # 300 moments, 1900-2030, deterministic pin, dual invocation path
    jyotishqa/             # in-repo seed, 10-30 items, labeled seed (not benchmark)
    cases/                 # with-minus-without seeds
    README.md              # the pre-commitment + gate doc, written BEFORE first run
    conftest/tier1_fixtures.py
  skills/rishi-reading/
    SKILL.md               # name, recall-scoped description, routing, refusal triggers
    contract.md            # R1-R6, full text, canonical
    references/            # doctrine: bphs-rulebook.md, dashas.md, charts.md, remedies.md,
                           #             dignity-table.md, audit-checklist.md
  agents/                  # schematic JSON→md transformations, one md per subagent
    chart-verifier.md      # ephemeris recompute, binary approvals
    doctrine-critic.md     # doctrine-conformity critique (not chart facts)
  packaging/hooks/         # reminder text (zero-code); Jinja2 plugin.json templates
  .claude-plugin/          # GENERATED, checked in, provenance bumped by build tool
    plugin.json
    marketplace.json
  .codex-plugin/plugin.json   # GENERATED
  .agents/plugins/marketplace.json   # GENERATED (Codex marketplace)
  .mcp.json                # GENERATED {"mcpServers": {...}}
  hooks/hooks.json          # GENERATED Claude reminder hook
  hooks.json                # GENERATED Codex root hook (same source)
  opencode/README.md        # pointer-only: git-clone install; no npm payload
  tools/build_plugin.py    # reads __version__, emits + check; unknown keys = fail
  CI runs: pytest, ruff, build --check, tier1, footprint estimator, uvx-tag assert
```

`AGENTS.md`, `system_prompt.md`, `README.md`, `.github/copilot-instructions.md`, `.cursor/rules/*` rewritten to reference the contract and the vendored `skills/rishi-reading/` doctrine. `CLAUDE.md` pointer-only. 16 legacy skill dirs deleted with doctrine mined first.

### The `rishi-reading` skill

- **Description**: recall-scoped (reading, chart, kundali, jyotish, dasha, transit, muhurtha, spouse, career, timing, astrology). Negative routing via verification, not description.
- **Body**: (1) five refusal triggers → refuse or flag (tropical-as-sidereal presented as fact; Moon within a day of a sign boundary without degree check; ascendant/used angles without birth time; dasha without lunar-mansion degree; chart-less remedies asserted as fact; plus no fabricated chart data); (2) `cast_vedic_chart` FIRST, `cast_transit_chart` if timing involved; (3) emit CLAIM–GROUND–STANCE claims; (4) gate cue — genuinely low-stakes informational reading ships with grounds appendix, calibration footer, disagreement log; anything marriage/health/career/remedy verifies first (verify-by-default on high-stakes slices, report Phase v1); (5) never the six forbidden behaviors; (6) when the tool fails, say so and ask for verification of birth details (existing highest-priority rule preserved).
- **Progressive disclosure**: doctrine files under `references/`, each capped 2–5k tokens; loaded on trigger only.

### The six-rule contract (canonical in `skills/rishi-reading/contract.md`)

R1 Falsifiability — claim cites chart grounds or is tagged UNSUPPORTED; grounds appendix in every reading
R2 Uncertainty disclosure — words a separate judge grades (no numeric self-report); calibration footer per reading (withheld counts); below-threshold claims withheld or flagged, never smoothed
R3 Discriminating agreement — Type-1/Type-2 enforced; never retract a tool-supported claim without new grounds; never adopt user's premise against tool-grounds; selection-time agreement penalty; overcorrection meter
R4 Forbidden behaviors — no fear framing; never predict death/longevity (Maraka → "deep transformation"); medical/financial/crisis → professional deferral; no liking-optimized selection
R5 Remedy restraint — matched remedies only; "no remedy needed" is always valid; no fear-remedy pairings; no remedy sold off below-threshold
R6 Accountability — named provenance (engine version, commit, ayanamsha, Lahiri default + variant); disagreement log; the registry rule handles correspondences

### Verification subagents (v1)

- **chart-verifier** — inputs: emitted claims + the already-fetched chart; job: ephemeris recompute, dignity/yoga legality, dasha consistency; output: per-claim binary approve/deny + reason + chart field pointer. Cannot generate interpretation.
- **doctrine-critic** — inputs: emitted connectivity claims; job: BPHS-conformity review (rule firing vs grounds), never recompute chart facts.
- Aggregation: per-claim; any deny blocks the factual claim; the interpretation passes with critic notes. One verifier round + one critic pass per turn max; more → deep tier v3 (unbuilt).
- Model: same family, authorship-obfuscated inputs on both subagents; cross-family reserved for offline calibration v2.

### The hesitation gate + equal-cost bar (pre-commitment)

`evals/README.md` **written before any run**, containing:
- Seed set size, construction rule, and count of items.
- The release gate, verbatim: delta > seed-set standard error, computed at first measurement, locked and not revisited; if the set cannot yield a positive margin, **expand the set, never relax the bar**. If the margin is possible and not cleared, verification does not ship.
- The failure branch pre-committed: verification off / sample-and-vote + tool-check ships.
- The pilot rule: first run measures noise, never the verdict.

### Hooks (reminder-only, per owner decision)

- `pre-user-prompt` (UserPromptSubmit): "Cast the chart first — no chart, no reading."
- Claude: `hooks/hooks.json`; Codex: root `hooks.json`; same source file. Zero executable code. **No file-system or network side-effect hook ships in v1.** (Would change only by explicit future owner flag, opt-in, documented.)

### Plugin MCP surface (frozen at 5)

`cast_vedic_chart`, `cast_transit_chart`, `calculate_compatibility_tool`, `check_muhurtha_tool`, `analyze_career_chart` via plugin `.mcp.json` (`{"mcpServers": {...}}`), `uvx rishi-ai-mcp@X.Y.Z`. Remaining 7 tools: pip path only, README-documented as "full engine; plugin speaks 5 by design".

### Distribution (one repo, documented lines per host)

- **Claude Code:** own marketplace `marketplace.json` (`name: rishi-ai-mcp`, `owner: Adarsh J`, `source: ./`, `plugins[0]: {name: rishi-ai, …}`). Install: `/plugin marketplace add adarshj322/rishi-ai-mcp` → `/plugin install rishi-ai@rishi-ai-mcp`. `.mcp.json` + `hooks/hooks.json` + skills/agents auto-discovered. `claude plugin validate` in CI (manifest-only; clean-install drill is the real gate).
- **Codex:** `.codex-plugin/plugin.json` with `skills`/`mcpServers` pointers + `interface` block; `.agents/plugins/marketplace.json` (`name`/`source: {source: "local", path: "."}` / `policy: {installation: "AVAILABLE", authentication: "ON_INSTALL"}` / `category: "Productivity"`); root `hooks.json`. Install documented via `codex plugin marketplace add adarshj322/rishi-ai-mcp` then `/plugins`.
- **OpenCode:** git-clone path in README — `.opencode/` / `~/.config/opencode/` copy + `opencode mcp add rishi-ai-mcp -- uvx rishi-ai-mcp`; no npm payload, no dist claim; dogfood-first.
- **MCP Registry:** optional, not on the v1 path.
- **Everything else** (Gemini CLI, VS Code Copilot, Cursor): docs path — pip install + vendored doctrine; README states the plugin surface difference and the no-binding limitation plainly.

### `tools/build_plugin.py`

Reads `__version__` from `rishi_ai_mcp.py` (not pyproject — dynamic). Emits/verifies `marketplace.json`, `.mcp.json`, hooks (Claude + Codex), both plugins' `plugin.json`. Unknown keys fail; `--check` compares emitted vs committed (drift = CI red). Prints a host-by-host install cheatsheet for README.

### CI matrix

```
python 3.10–3.13:
  ruff
  pytest (existing 41 + plugin unit tests + tier1)
  python tools/build_plugin.py --check
  tier1 gate (300 moments; dual invocation paths reading same pyswisseph/Moshier — **shared lineage, regression/determinism gate, not astronomical-truth verification** — caveat stamped in evals/README)
  footprint estimator (skill body + 5 tool schemas; fail > 3k by word-count×1.4 bound)
  PyPI-tag-assert for the release tag (publish job precondition)
```

### Success metrics (v0+v1)

- Installs end-to-end on clean Claude Code + clean Codex + clean OpenCode (documented test session).
- Idle footprint < 3k (estimator in CI; measured).
- Tier-1: 100% deterministic pass, delta zero-vs-pin.
- With-minus-without: pre-committed in `evals/README.md`, measured and recorded; per the pre-commitment either verification ships or it doesn't, no softening after data.

## Validation before calling it done

- `pytest` green on 3.10–3.13; ruff clean;
- `claude plugin validate` green **and** manual clean-install drill (validate doesn't see `.mcp.json`/hooks);
- `codex` lint of both JSON files; schema-shape confirmed (`jq` structural checks);
- npm pack diff (no package yet — OpenCode only; assert README path present, no artifacts);
- one-afternoon dogfood: each host, one reading, inspect refusal triggers and grounds appendix live; record in CHANGELOG under "unreleased/verified-by-dogfood".

## Explicit calls (owner-ratified, 2026-11-08)

1. Tier-1: **single-lineage dual-path + determinism freeze** (option 2-a); caveat stamped in evals/README; ~1″ acknowledged-is-fine; no `.se1` buy.
2. OpenCode: **git-clone path, no npm package**; dogfood-first (option 1-b).
3. Audit hook: **reminder-only**, no file writes (option 3, cut).
4. Equal-cost gate: **formal written delegation in `evals/README.md`**, pre-committed before first run (option 4-c).
5. Doctrine: **vendored in wheel** (skills/ + refs) **+ minimap inline in `system_prompt.md`** (option 5-b(+a)).
6. One `rishi-reading` skill; `.compat` slot never shipped in v1.
7. Equals verify-by-default on marriage/health/career; fast path only for genuinely low-stakes reads.
8. Reminder-only hook approved; deviations require an owner rewrite of this line.

## Out of this design

- v2: isotonic calibration set; tiered per-turn/offline verifier split; Vedic agreement study (N ≥ 150 jyotishis) — not code.
- v3: offline deep tier; preregistered prospective registry.
- PyPI/npm publish automation (folded into existing release flow; PyPI is the v1 ship target, `pypi` environment approval per usual).
- MCP Registry submission (optional, same session if trivial).
