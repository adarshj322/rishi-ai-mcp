# RishiAI Ground Truth Plugin (v0+v1) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn rishi-ai-mcp from a pip MCP server into an installable ground-truth plugin (Claude Code + Codex git marketplaces, documented OpenCode docs path) that ships doctrine + contract + gated verification, and passes a pre-committed equal-cost gate.

**Architecture:** One repo, three distributable surfaces generated from one source (`skills/rishi-reading/**` + `agents/`): Claude plugin files (`.claude-plugin/`, root `.mcp.json`, `hooks/hooks.json`), Codex plugin files (`.codex-plugin/plugin.json`, repo-root `hooks.json`, `.agents/plugins/marketplace.json`), and the pip wheel (`rishi_ai_mcp.py` + `skills/rishi-reading/**`). A `tools/build_plugin.py` reads `__version__` from `rishi_ai_mcp.py` and emits/checks every host manifest. Verification ships gated by a pre-committed bar in `evals/README.md`.

**Tech Stack:** Python ≥ 3.10, mcp (FastMCP), dashaflow 1.5+ (path: dashaflow→pyswisseph→Moshier fallback), hatchling, pytest, ruff (`E,F,W,I,UP,B`; new `zip()` needs `strict=`). Shell for hook bodies. GitHub Actions CI.

**Spec:** `docs/superpowers/specs/2026-11-08-rishi-ground-truth-plugin-design.md`

## Global Constraints

- Owner-ratified 2026-11-08 decisions: **1b** OpenCode = documented git-clone path, no npm package; **2a** Tier-1 = single-lineage dual-path + determinism gate, shared-lineage caveat, NOT astronomical truth ("~1 arcsecond Moshier is fine"); **3** hooks = reminder-only, no code hook bodies v1, no file writes outside project; **4c** equal-cost bar = formal written delegation in `evals/README.md`, pre-committed before first run; **5b(+a)** wheel ships `skills/rishi-reading/**` + one-paragraph minimap inline in `system_prompt.md`.
- Report binding: verification ships only if it clears the pre-committed bar; failing is a valid outcome with verification off.
- Plugin MCP surface frozen at 5 tools: `cast_vedic_chart`, `cast_transit_chart`, `calculate_compatibility_tool`, `check_muhurtha_tool`, `analyze_career_chart`. Other 7 tools stay pip-only, documented as such.
- Moshier fallback; no `.se1` buy, no Swiss Ephemeris license, no network at runtime.
- Version lockstep everywhere: `__version__` == tag == PyPI == both plugins' `plugin.json` (asserted in CI).
- `AGENTS.md` highest-priority rules preserved (never fabricate chart data; tool binding). `CLAUDE.md` pointer-only, doctrine never duplicated.
- Single-file `rishi_ai_mcp.py` for the pip MCP server (no re-architecture).
- ruff `E,F,W,I,UP,B`; any new `zip()` carries `strict=`; Python 3.10–3.13 matrix.
- Deletion scope: 16 directories under `.agents/skills/` mined then removed (not 15). No scripts/executable hook bodies in plugin.
- Idle footprint target: skill body + 5 tool schemas ≤ ~3k tokens (CI estimator, word-count × 1.4 worst-case bound).
- Reference skills doctrine must not claim predictive accuracy; only consistency/auditability.
- Commit subjects: Conventional Commits, one deliverable per commit.
- Not on critical path (optional same-session, only if trivial): MCP Registry submission. Do not attempt.

## Review Focus

Five inputs the spec does not spell out; each is pinned by the task named.

1. **`pyproject.toml` build with `only-include` = `rishi_ai_mcp.py` + `skills/`** — hatch/build must not silently drop `skills/rishi-reading/**` (non-package data); expected behavior: wheel contains both, `pip install` exposes `skills/rishi-reading/contract.md`. Test: Task 23 has a wheel-content assertion test in `tests/test_plugin_wheel.py::test_skills_in_wheel`.
2. **Verification subagents with untrusted chart data** — a hostile/impossible chart (e.g., future date, nonexistent moon sign) must not loop the two subagents forever; expected: one round + one critic pass, then stop or refuse. Test: Task 11 has a subagent-contract doc test asserting the stop rule text.
3. **`build_plugin.py` when repo clone lacks `git` or py-version drifted** — expected: non-zero exit with one-line diagnosis, CI red, no silently site-rolled manifests. Test: Task 9 Step 1 has `tests/test_build_plugin.py::test_version_mismatch_fails` (mismatch → exit 3; missing `__version__` → exit 2; unknown key → exit 1).
4. **CI footprint estimator edge** — world-count×1.4 on emoji/UTF-8 byte-heavy doctrine; expected: fail at >3k worst-case bound, not warn. Test: Task 20 as specified.
5. **Doctrine references read at 30k tokens** — overflows by progressive-disclosure must not happen on small SKILL.md (load only refs listed in SKILL.md §references); expected: footprint estimator reads SKILL.md + declared refs only. Test: Task 19 footprint test + Task 10 SKILL.md refs manifest assertion.

---

### Task 1: Branch + spec snapshot

**Files:** none (git)

- [ ] **Step 1: Create work branch from main**
Run: `git switch -c feature/ground-truth-plugin`
Expected: branch created, clean tree.
- [ ] **Step 2: Commit the design spec reference state**
Run: `git log --oneline -1 docs/superpowers/specs/2026-11-08-rishi-ground-truth-plugin-design.md`
Expected: `45d33e8` visible. No changes.

---

### Task 2: Doctrine mining stub doc (record what the 16 dirs hold before deleting)

**Files:**
- Create: `evals/doctrine-mining-notes.md`

- [ ] **Step 1:** For each of 16 directories in `.agents/skills/`, capture one falsifiable refusal trigger, one deterministic tool-order step, and any unique grounding rule worth keeping. Write one line each into `evals/doctrine-mining-notes.md` as a table.
- [ ] **Step 2: Commit** `git add evals/doctrine-mining-notes.md && git commit -m "docs: doctrine mining notes (legacy skills)"`

---

### Task 3: `skills/rishi-reading/contract.md` — canonical R1–R6

**Files:** Create `skills/rishi-reading/contract.md`

- [ ] **Step 1: Write the contract from the design** — R1 Falsifiability (grounds or UNSUPPORTED tag), R2 Uncertainty (words, separate-judge scored, footer withheld counts), R3 Discriminating agreement (Type-1/2, selection-time agreement penalty, overcorrection meter), R4 Forbidden behaviors (no fear framing, no death/predict-longevity, professional deferral for medical/financial/crisis), R5 Remedy restraint (matched remedies only, "no remedy needed" is valid), R6 Accountability (named provenance engine/version/commit/Lahiri-default/disagreement log). 350–500 lines of prose. No hedging language like "consider" or "try to".
- [ ] **Step 2:** Verify by reading top-to-bottom; every rule has mechanism evidence motivation and falsifier. No citations to unreliable sources — can cite the report by title (`research/notes/final_report_rishi-plugin-ground-truth-bc68ed.md`) and the three papers (claim-checking, isotonic calibration) once, clearly marked "for context, not for per-turn use".
- [ ] **Step 3: Commit** `git add skills/rishi-reading/contract.md && git commit -m "docs: canonical R1-R6 contract"`

---

### Task 4: `references/` doctrine files

**Files:** Create `skills/rishi-reading/references/{bphs-rulebook.md,dashas.md,dignity-table.md,chart-walk-order.md,remedies.md,refusal-triggers.md,audit-checklist.md}`

- [ ] **Step 1:** Port the per-topic doctrine out of `.agents/skills/*` — one file per topic, ≤2,500 words each. Include: Desh-Kaal-Patra framing; locked fast-rule set (no LLM calculator rule, Lahiri default, D9/D10 vargas read not computed, Maraka → "deep transformation", lagna/lord logic); five refusal triggers verbatim from R4's list.
- [ ] **Step 2:** Add `references/README.md` listing every reference file with one-line purpose + when-to-load. (This is the progressive-disclosure manifest; CI footprint reads this file.)
- [ ] **Step 3: Commit** `git add skills/rishi-reading/references && git commit -m "docs: doctrine reference set"`

---

### Task 5: `SKILL.md` — the one entry skill

**Files:** Create `skills/rishi-reading/SKILL.md`

- [ ] **Step 1: Frontmatter**
`name: rishi-reading` ; `description:` recall-scoped to reading/chart/jyotish/dasha/transit/muhurtha/spouse/career/timing — not exhaustive. Keep under ~100 tokens.
- [ ] **Step 2: Body** — (1) refusal triggers (5) as hard short-circuits; (2) tool protocol: `cast_vedic_chart` first, `cast_transit_chart` if timing involved; contract pointer (load `contract.md` on read); (3) CLAIM–GROUND–STANCE claim format with worked micro-example; (4) gate cue: genuine low-stakes informational reading ships with grounds appendix + footer; marriage/health/career/remedy ⇒ verifier runs; verify-by-default slices; (5) every reading ends with the mandatory three artifacts: grounds appendix, calibration footer (withheld counts), disagreement log (user premises rejected with reasons or `none`); (6) no output contains forbidden behaviors; (7) tool failure ⇒ say so, ask user to verify birth details.
- [ ] **Step 3: Manifest test** — Write `tests/test_skill_manifest.py::test_references_manifest_lists_every_reference_file`: parse SKILL.md's `references:` list (or README refs file), assert every `references/*.md` appears and no extra appears. Fail initially (file not linked), implement, pass.
- [ ] **Step 4: Commit**

---

### Task 6: `chart-verifier` subagent

**Files:** Create `agents/chart-verifier.md`

- [ ] **Step 1:** Markdown-equivalent subagent definition (JSON-call-translatable to Claude and Codex `.md` agents): inputs = emitted claims + computed chart (tool outputs passed as args); job = ephemeris recompute, dignity/yoga legality, dasha consistency; output = per-claim binary verdict {approve|deny, reason, chart-field pointer}; cannot generate interpretation; must never recompute from scratch, only compare.
- [ ] **Step 2:** Stop rule: one verifier round per turn max; any deny blocks the corresponding factual claim (not the interpretive one); no third pass; "unsure" counts as deny for facts.
- [ ] **Step 3: Commit**

---

### Task 7: `doctrine-critic` subagent

**Files:** Create `agents/doctrine-critic.md`

- [ ] **Step 1:** Inputs = emitted connectivity claims + chart grounds; job = BPHS-conformity review (rule firing vs grounds), no chart recalculation; output = per-claim conformance verdict + rule citation + one-line rationale; failure mode = reward-hacking critique (generates platitudes instead of checks) must be explicitly banned in output contract.
- [ ] **Step 2:** Stop rule mirrors verifier (one pass per turn).
- [ ] **Step 3: Commit**

---

### Task 8: Reminder hook source

**Files:** Create `packaging/hooks/reminder.txt` (single line)

- [ ] **Step 1:** Exact content: `No chart, no reading. Cast cast_vedic_chart first; interpret only what tool math produced.` (no code, no side effects).
- [ ] **Step 2: Commit**

---

### Task 9: `tools/build_plugin.py` — manifest generator + check (TDD)

**Files:** Create `tests/test_build_plugin.py`, `tools/build_plugin.py`

- [ ] **Step 1: Write failing test** in `tests/test_build_plugin.py` asserting: on `--check`, exit 0 when committed files match templates rendered with `__version__`; exit 3 with a message naming each mismatching file when any does; exit 2 with `version-source-missing` when `rishi_ai_mcp.__version__` is absent; exit 1 on unknown template key.
Run: `pytest tests/test_build_plugin.py -v` → expected FAIL (module missing).
- [ ] **Step 2: Implement** `tools/build_plugin.py`:
  - `get_version()`: `ast`-parse `rishi_ai_mcp.py`, return `__version__` or raise `VersionSourceMissing`.
  - Templates in-memory: `{plugin.json: kebab-name, version, description, author=Adarsh, homepage, repository(https://github.com/adarshj322/rishi-ai-mcp), license MIT, keywords, interface displayName "RishiAI — Ground-Truth Vedic Astrology"}`; `marketplace.json (Claude)`: `{"name":"rishi-ai-mcp","owner":{"name":"Adarsh J"},"plugins":[{"name":"rishi-ai","source":"./","description": "…"}]}`; `marketplace.json (Codex)`: `{"name":"rishi-ai-mcp","plugins":[{"name":"rishi-ai","source":{"source":"local","path":"."},"policy":{"installation":"AVAILABLE","authentication":"ON_INSTALL"},"category":"Productivity"}]}`; `.mcp.json`: `{"mcpServers":{"vedic-astrology":{"command":"uvx","args":["rishi-ai-mcp@__version__"]}}}`; Claude `hooks/hooks.json` + Codex root `hooks.json`: same event/matcher/text body, `{"hooks":{"UserPromptSubmit":[{"hooks":[{"type":"command","command":"<print reminder from packaging/hooks/reminder.txt>"}]}]}}` — NOTE: reminder-only, no file write; use `echo` built-in only.
- [ ] **Step 3:** Run test → PASS. Add `pytest` to CI glob. Commit.

---

### Task 10: Generate manifests + hooks

**Files:** Create generated `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, `.mcp.json`, `hooks/hooks.json`, `hooks.json`

- [ ] **Step 1:** Extend Task 9's `tools/build_plugin.py` default mode (no flag) to emit templates rendered with `__version__`; keep `--check` compare-only. The `.mcp.json` emitted during development uses unpinned `uvx rishi-ai-mcp`; version pinning is a release-flow concern, not a committed artifact (Task 22/25). Run `python tools/build_plugin.py`; inspect diffs; verify `jq` parses all; `version` equal across all seven files and equals `rishi_ai_mcp.__version__`.
- [ ] **Step 2:** Verify `.codex-plugin/plugin.json` has `"skills": "./skills/"` and `"mcpServers": "./.mcp.json"`; `.claude-plugin/plugin.json` has none of those; both have `version`.
- [ ] **Step 3: Commit** (git add the seven files + templates, message `chore(plugin): generated per-host manifests`).

---

### Task 11: Subagent-injection test — subagent files are well-formed (TDD)

**Files:** Create `tests/test_agents.py`

- [ ] **Step 1: Write test** asserting: both files exist; each has YAML-less H2 contract with inputs/outputs/stop-rule; verifying chart-verifier deny→factual-block rule present; `doctrine-critic` has anti-reward-hacking line; no `python` executable blocks; no network endpoints. FAIL initially.
- [ ] **Step 2:** Implement — refine Task 6/7 files until PASS. Commit.

---

### Task 12: `evals/README.md` — the pre-commitment (written BEFORE any run)

**Files:** Create `evals/README.md`

- [ ] **Step 1:** Sections: (1) corpus description — JyotishQA seed set built by this project, 10–30 items, construction rule, no publication claim; (2) equal-cost bar: delta > seed-set standard error at first measurement, locked, not revisited; expand set not bar; (3) failure branch — verification off + sample-and-vote ships; (4) pilot rule — first run measures noise not verdict; (5) Tier-1 caveat stamped verbatim: "Shared lineage (dashaflow → pyswisseph → Moshier fallback): this is a regression/determinism gate, NOT astronomical-truth verification."; (6) shared inference floor; (7) metrics reported w/ CIs, never trophies.
- [ ] **Step 2: Commit** `docs: eval gate pre-commitment`. (Executed before Task 13: the doctrine doc must exist before any corpus-related commands run, keeping the pre-commitment honest by sequence, not just by timing.)

---

### Task 13: Tier-1 corpus + determinism gate (TDD)

**Files:** Create `evals/tier1/moments.json`, `tools/tier1_check.py`, `tests/test_tier1.py`

- [ ] **Step 1: Write test** `tests/test_tier1.py::test_corpus_pinned_deterministically`: load `moments.json`, for each moment call `dashaflow.cast_chart()` twice (same process) and compare `dashaflow.vedic_calculator.compute_chart`-style lower-level path if importable; assert ≤1e-6° positional delta (Moshier tolerance) and byte-identical JSON output across invocations. If the lower-level path cannot be imported on the pinned dashaflow, the test degrades to same-process determinism only and logs the degradation explicitly in `evals/README.md` (logged honestly, never silent).
Run → expected FAIL (no corpus).
- [ ] **Step 2:** Build corpus: 300 UTC instants across 1900-2030 pinned in-repo (hand-picked landmark instants: ephemeris edges — 01 Jan 1900, 2000-01-01 12:00, recent transits); deterministic fakerule for the rest → stored literal table with `manual=True` tag for hand-curated and `generated_from=…` tag otherwise.
- [ ] **Step 3:** Implement check; run; commit with corpus.

---

### Task 14: `evals/cases/` seed with-minus-without cases

**Files:** Create `evals/cases/{grounding.jsonl,sycophancy.jsonl,remedy.jsonl}`

- [ ] **Step 1:** 12 grounding cases (well-formed interpretation questions requiring chart-grounded answers), 8 sycophancy cases (user presses to agree with a wrong premise — expected refusal/redirect), 6 remedy cases (fear-coupled remedies must be refused). Each: `{prompt, birth, expected_verifier_verdict, with_delta_baseline}`.
- [ ] **Step 2: Commit.**

---

### Task 15: Calibration minimap in `system_prompt.md`

**Files:** Modify `system_prompt.md`

- [ ] **Step 1:** Replace everything after line 11 (role definition end marker) with a minimap: one paragraph of intent + the six rules in one line each + a pointer to vendored `skills/rishi-reading/` (exact installed path pattern `<site-packages>/rishi_ai_mcp/skills/rishi-reading/…`) + provenance footer requirement. Keep the first 11 lines byte-identical.
- [ ] **Step 2: Consistency test** — add `tests/test_minimap.py::test_minimap_mentions_all_six_rules` parsing `system_prompt.md` for the literal strings R1…R6 and the vendored path. FAIL initially → implement → PASS. Commit.

---

### Task 16: Wheel vendors `skills/`

**Files:** Modify `pyproject.toml`; extend `tools/build_plugin.py` with `--check-wheel`

- [ ] **Step 1:** Edit `[tool.hatch.build.targets.wheel] only-include = ["rishi_ai_mcp.py", "skills/"]`.
- [ ] **Step 2: Test** `tests/test_plugin_wheel.py::test_skills_in_wheel`: build wheel to tmp dir, unzip, assert `rishi_ai_mcp.py` + `skills/rishi-reading/contract.md` present; assert `. agents/skills/` gone. FAIL initially.
- [ ] **Step 3:** Implement/ensure hatch picks it; PASS. Commit.

---

### Task 17: Delete 16 legacy `.agents/skills/*` directories

**Files:** Delete `.agents/skills/` entirely (and `.agents/workflows/`, `.agents/rules/` after migration pointers are written); keep only `.agents/` if anything remains — otherwise empty dirs are also removed.

- [ ] **Step 1:** Mine complete (Task 2)? If not, re-mined now. Then `rm -r .agents/skills/`.
- [ ] **Step 2:** Update `AGENTS.md`, `README.md`, `system_prompt.md`, `.github/copilot-instructions.md`, `.cursor/rules/rishi-ai.mdc` to reference RishiAI ground-truth doctrine (top-level reference, not copied text).
- [ ] **Step 3: Commit** `refactor(persona): remove yes-man skills`.

---

### Task 18: Rewrite `AGENTS.md` to pointer-only

**Files:** Modify `AGENTS.md`

- [ ] **Step 1:** Replace entire file with: (1) scope line; (2) highest-priority-rule block verbatim-equivalent (never fabricate chart data; tool dependency) + Lahiri-default note; (3) pointer to `skills/rishi-reading/contract.md` + `references/`; (4) tool-binding note; (5) plugin vs pip surface note (5 wired / 7 pip-only).
- [ ] **Step 2: Consistency test** — extend minimap test; `tests/test_minimap.py::test_agents_md_pointer_only` (no `world's greatest`, no `greatest`, no motivational prose, contains literal `skills/rishi-reading/contract.md`). FAIL → edit → PASS. Commit.

---

### Task 19: Footprint estimator test (TDD)

**Files:** Create `tests/test_footprint.py`

- [ ] **Step 1: Write test**: read `SKILL.md` + the five plugin tool schemas (skip large chart d2 fields as proxy) via `json` + `dashaflow` introspection or hand-mapped list; Σ words × 1.4 < 3000.
Run → expected FAIL (estimator > target).
- [ ] **Step 2:** Tighten `SKILL.md` prose; re-run; PASS; commit.

---

### Task 20: CI matrix update

**Files:** Modify `.github/workflows/ci.yml`

- [ ] **Step 1:** Add steps after `pytest -q`: ruff (pinned `E,F,W,I,UP,B`, `zip()` rules), `python tools/build_plugin.py --check`, footprint test (pytest `tests/test_footprint.py`), tier-1 (`python tools/tier1_check.py`), PyPI-tag assert for release-only jobs (skip on PR).
- [ ] **Step 2: Commit** `ci: plugin gates`.

---

### Task 21: README rewrite — install & distribution sections

**Files:** Modify `README.md` (install 14–40, persona table, workflows list, architecture block, license)

- [ ] **Step 1:** Replace persona sections with: plugin install (Claude: `/plugin marketplace add adarshj322/rishi-ai-mcp` then `/plugin install rishi-ai@rishi-ai-mcp`); Codex (`codex plugin marketplace add …`, `/plugins`); OpenCode docs path (git clone, `opencode mcp add rishi-ai-mcp -- uvx rishi-ai-mcp`); pip docs path (vendored doctrine pointer); state "plugin speaks 5 tools by design; pip exposes 12"; remove "world's greatest"; add CHANGELOG entry "unreleased" describing change + honest limitations (no predictions claimed, no .se1, tier-1 caveat).
- [ ] **Step 2: Consistency test** — add `tests/test_docs.py::test_readme_has_no_yes_man_language` (reject `world's greatest`, `yantra`, `guaranteed`, `predictions will`). FAIL → fix → PASS. Commit.

---

### Task 22: CHANGELOG + version discipline

**Files:** Modify `CHANGELOG.md`

- [ ] **Step 1:** Append under `## [Unreleased]`: bullets — ground-truth plugin (Claude Code + Codex), contract, verification gated+off-until-bar, docs paths, wheel doctrine, legacy skills removed, tier-1 caveat, no accuracy inflated.
- [ ] **Step 2: Commit** `chore(release): changelog ground-truth plugin`.

---

### Task 23: Full suite + plugin smoke test

**Files:** Run existing `test_rishi_ai_mcp.py` + new tests (no new files)

- [ ] **Step 1:** `pytest -q` → expect pass on 3.10–3.13 (in CI). If any legacy test asserts removed behavior (none expected — tools unchanged), pin it or mark xfail with reason. Record counts in commit message.
- [ ] **Step 2:** Manual host smoke: `uvx rishi-ai-mcp --help` (expected: entrypoint OK); `claude plugin validate` on the repo's `.claude-plugin/` (expected: pass); `jq` sanity on all JSON manifests (expected: parse clean).
- [ ] **Step 3: Commit** merge-ready branch state.

---

### Task 24: Dogfood drill + recover the plan into the final report

**Files:** Modify `CHANGELOG.md`, `evals/README.md`

- [ ] **Step 1:** One reading each on Claude Code + Codex (trigger "read my chart: DOB DD/MM/YYYY, time, place"). Verify refusal trigger + grounds appendix; screenshot-free logging of outcomes appended to `evals/README.md` ("Verified by dogfood, date").
- [ ] **Step 2:** If any wiring fails (validate passes but MCP silent, Codex pointed at wrong path, etc.), log exactly what broke and fix it in-place.
- [ ] **Step 3: Commit** `docs: dogfood log`.

---

### Task 25: Open the PR (owner's release flow preserved)

**Files:** none

- [ ] **Step 1:** Push `feature/ground-truth-plugin`; open PR to `main` with summary linking design spec (`docs/superpowers/specs/2026-11-08-rishi-ground-truth-plugin-design.md`) + plan. Do NOT tag/release; that is owner's `pypi`-environment-gated step.
- [ ] **Step 2:** Await owner merge (their admin-merge flow); do not self-merge even if CI green.
