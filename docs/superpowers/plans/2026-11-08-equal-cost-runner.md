# Equal-Cost Bar Runner Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and run the measurement that decides whether the plugin's verification machinery ships: the three-arm equal-cost comparison over the 26 JyotishQA seed cases, with hybrid deterministic+judge scoring and an Evidence Log row committed to `evals/README.md`.

**Architecture:** One orchestration entry (`tools/eval_runner.py`) with a small scoring library (`tools/eval_scoring.py`). Arm prompts are files under `evals/prompts/`; the `with` arm's verifier and critic reuse `agents/chart-verifier.md` and `agents/doctrine-critic.md` verbatim as their system prompts. Charts are precomputed once per item and embedded in every arm's prompt. All model calls go through OpenRouter via the `openai` SDK at explicitly pinned model ids, temperatures, and seeds.

**Tech Stack:** Python 3.10+, `openai` SDK against OpenRouter (`https://openrouter.ai/api/v1`), `dashaflow` 1.5.1 for chart precompute, `unittest` + `pytest`, ruff (`E,F,W,I,UP,B`; explicit `zip(strict=)`).

**Spec:** `docs/superpowers/specs/2026-11-08-equal-cost-bar-runner-design.md`

## Global Constraints

- Models pinned by the owner: arms `deepseek/deepseek-v4.1-flash`, judge `meta/muse-spark-1.3-contributor`. Any change re-opens the measurement (`evals/README.md` §10).
- `B` = output tokens per item per arm; default `3000`. Shares: `bare` 1×B; `without` 3 × B/3; `with` draft B/3 + verifier B/6 + critic B/6 + revision B/3. Input tokens recorded, never budgeted.
- Any arm exceeding B on ANY item ⇒ that arm is disqualified for the entire run; the run is reported as disqualified, not re-scored (`evals/README.md` §3).
- Deterministic stage does only two things: fabrication detection against the chart whitelist, and mechanical required-ground presence. Everything semantic is the judge's job.
- Judge inputs are anonymized (no arm label, no run ordering), reference-guided (chart JSON + clause list), temperature 0, and every verdict carries a quoted evidence span.
- Mandatory clauses are pre-authored in `evals/cases/ledger.json` BEFORE the first run; the judge may not invent clauses.
- Pilot = noise floor only. SE is computed and printed BEFORE scoring; the gate value is locked in that same run. No verdict is taken from the pilot (`evals/README.md` §4.2(d)).
- Report discipline (`evals/README.md` §4.3): intervals everywhere, no trophy language, no external comparison, no point estimate without its interval, latency recorded, token usage per arm recorded.
- The Evidence Log row is appended to `evals/README.md` §6 in the same commit as the results, labeled `pilot — noise floor only`.
- The only change to `evals/README.md` outside the Evidence Log is the §1 owner-rewrite amendment adding the diagnostic `bare` arm; §4, §4.1, §4.2 and §7 are untouched.
- No predictive-accuracy language anywhere: not in reports, prompts, commits, or docs. The seed set measures output correctness on chart-grounded tasks, nothing else.
- API key from `OPENROUTER_API_KEY`; never logged, never committed.
- Artifacts under `evals/results/<YYYY-MM-DD-pilot>/`: `report.md`, `results.json`, `charts.json`, `manifest.json`.

## Review Focus

1. **`B` accounting counts the wrong field** — output tokens from the API response's `usage.completion_tokens`, summed across all calls in the arm. If input tokens were counted, the with-arm's doctrine+chart preamble would disqualify it before generating anything. Test: Task 2 `test_budget_uses_completion_tokens_only`.
2. **Arm leakage into judge input** — any occurrence of `bare`/`without`/`with` as an arm label, or ordering artifacts ("first answer"), breaks anonymity. Test: Task 5 `test_judge_prompt_is_anonymized`.
3. **Fabrication checker whitelist too loose** — accepts any degree string that appears anywhere in the chart JSON, including for the wrong planet. Expected behavior: a degree attached to planet A that belongs only to planet B is flagged. Test: Task 1 `test_cross_planet_degree_is_flagged`.
4. **Judge JSON parse failure** — model wraps output in prose or fences. Expected: one strict retry, then item marked `judge-error` and excluded from BOTH arms with the exclusion counted in the report, never silently dropped. Test: Task 5 `test_judge_error_excluded_from_both_arms`.
5. **Over-budget mid-run** — an arm blowing B on item 17 leaves earlier results in place. Expected: whole arm marked disqualified in `results.json` and report header; its proportion is not printed. Test: Task 4 `test_arm_disqualified_for_run_on_budget_overrun`.

---

### Task 1: Deterministic scoring library (fabrication + requirements + intervals)

**Files:**
- Create: `tools/eval_scoring.py`
- Create: `tests/test_eval_scoring.py`

**Interfaces:**
- Consumes: nothing (stdlib only).
- Produces:
  - `compute_se(n: int) -> float` — `0.5 / sqrt(n)` (rule 1).
  - `wilson_interval(k: int, n: int, z: float = 1.96) -> tuple[float, float]`.
  - `extract_numeric_claims(text: str) -> list[str]` — degree patterns (`\d+(?:\.\d+)?°`), sign names, date patterns (`\b\d{4}-\d{2}-\d{2}\b`, `\b(?:Jan|Feb|...)\w* \d{4}\b`).
  - `find_fabrications(text: str, chart: dict) -> list[str]` — returns claims not derivable from the chart JSON; planet-scoped degree check: a degree adjacent to a planet name must equal that planet's degree within 0.5°, not merely appear anywhere.
  - `deterministic_verdict(text: str, ledger_entry: dict, chart: dict) -> dict` — `{"pass": bool, "failures": [str], "checked": [str]}`; fails on fabrication or on a missing mechanical clause (substring match of the expected ground string in the ledger entry).

- [ ] **Step 1: Write failing tests** in `tests/test_eval_scoring.py` (unittest):
  - `test_compute_se_rule1`: `compute_se(26)` ≈ 0.098058…
  - `test_wilson_bounds`: k=20,n=26 → interval contains 20/26 and both bounds in [0,1]; k=0 and k=n edge cases valid.
  - `test_fabrication_flags_unknown_degree`: chart has Sun 10.5°; text says "Sun at 23°" → flagged.
  - `test_cross_planet_degree_is_flagged`: chart Sun 10.5°, Moon 23°; text says "Sun at 23°" → flagged (degree exists but for the wrong planet).
  - `test_known_degree_passes`: text repeats the exact Sun degree → not flagged.
  - `test_deterministic_verdict_missing_required_ground`: ledger entry requires substring `"10th lord"`; text lacks it → fail with that entry in `failures`.
- [ ] **Step 2: Run** `python -m pytest tests/test_eval_scoring.py -v` → FAIL (module missing).
- [ ] **Step 3: Implement** `tools/eval_scoring.py` with the signatures above. Regex-based extraction; chart whitelist built by walking the chart JSON recursively for numbers/strings. Planet-adjacency window: 40 characters around the planet name.
- [ ] **Step 4: Run tests** → PASS. Run `ruff check --select E,F,W,I,UP,B tools/eval_scoring.py tests/test_eval_scoring.py` → clean.
- [ ] **Step 5: Commit** `git add tools/eval_scoring.py tests/test_eval_scoring.py && git commit -m "feat(evals): deterministic scoring primitives (fabrication, SE, Wilson)"`

---

### Task 2: Corpus ledger normalization + prompts

**Files:**
- Create: `evals/cases/ledger.json`
- Create: `evals/prompts/bare_system.md`, `evals/prompts/doctrine_system.md`, `evals/prompts/judge.md`
- Create: `tests/test_eval_ledger.py`

**Interfaces:**
- Produces: `ledger.json` — `{"items": {id: {"tag": "chart-grounded"|"interpretation-only", "clauses": [{"text": str, "mechanical": bool}], "required_grounds": [str]}}}` for all 26 ids.
- Produces prompt files consumed by Task 3/4/5 by path.

- [ ] **Step 1: Write failing test** `tests/test_eval_ledger.py`:
  - `test_every_case_has_ledger_entry`: ids from the three JSONL files == ledger ids, count 26.
  - `test_tags_valid_and_g_are_chart_grounded`: g-* → `chart-grounded`; s-*/r-* → `interpretation-only`.
  - `test_every_item_has_clauses_and_required_grounds`: both non-empty; every clause text ends with the same wording as the rubric's "must …" sentence it came from (spot-check 3 items verbatim).
- [ ] **Step 2: Run** → FAIL (ledger missing).
- [ ] **Step 3: Author `ledger.json`** by decomposing each `expected_verifier_verdict` into its "must …" clauses (one clause per mandatory sentence), marking mechanical only those naming an exact chart string (dasha pair, sign name, SAV number). Author the three prompt files: `bare_system.md` (one paragraph, tools-only, no doctrine), `doctrine_system.md` (contract summary + SKILL.md flow + CLAIM–GROUND–STANCE requirement), `judge.md` (clause-by-clause JSON output contract, evidence required per verdict, no arm labels).
- [ ] **Step 4: Run tests** → PASS.
- [ ] **Step 5: Commit** `git add evals/cases/ledger.json evals/prompts tests/test_eval_ledger.py && git commit -m "feat(evals): corpus ledger clauses + arm/judge prompts"`

---

### Task 3: Model client + `without` arm (sample-and-vote)

**Files:**
- Create: `tools/eval_arms.py`
- Create: `tests/test_eval_arms.py`

**Interfaces:**
- Produces:
  - `class ChatClient: def complete(self, system: str, user: str, model: str, temperature: float, max_tokens: int, seed: int = 7) -> dict` — returns `{"text": str, "output_tokens": int, "input_tokens": int, "latency_s": float}`; reads `OPENROUTER_API_KEY`; uses `openai.OpenAI(base_url="https://openrouter.ai/api/v1")`.
  - `run_without(client, item, chart, ledger_entry, budget, doctrine_prompt) -> dict` — 3 completions at temperature 0.7 with `max_tokens=budget//3`; filters by `deterministic_verdict`; selects survivor with fewest failures (ties → first); returns `{"text", "output_tokens", "disqualified": bool, "samples": int}`.
  - `class BudgetExceeded(Exception)`.

- [ ] **Step 1: Write failing tests** with a `FakeClient` (no network): `test_without_samples_three_and_selects_best`, `test_without_disqualified_when_total_exceeds_budget`, `test_without_discards_fabricating_sample` (fake returns one sample with fabricated degree — not selected), `test_arms_call_doctrine_prompt` (asserts the doctrine prompt text was passed).
- [ ] **Step 2: Run** → FAIL.
- [ ] **Step 3: Implement** `tools/eval_arms.py`. Selection: compute `deterministic_verdict` per sample; sort by `len(failures)`; first wins ties; if all fail, still return best with its failures (the judge scores it; disqualification is budget-only).
- [ ] **Step 4: Run tests** → PASS; ruff clean.
- [ ] **Step 5: Commit** `git add tools/eval_arms.py tests/test_eval_arms.py && git commit -m "feat(evals): OpenRouter client + without-arm sample-and-vote"`

---

### Task 4: `with` arm (verifier → critic → revision) + `bare` arm

**Files:**
- Modify: `tools/eval_arms.py`
- Modify: `tests/test_eval_arms.py`

**Interfaces:**
- Consumes: `ChatClient`, `deterministic_verdict`, `agents/chart-verifier.md`, `agents/doctrine-critic.md`.
- Produces:
  - `run_bare(client, item, chart, budget) -> dict` — one completion, bare system prompt, `max_tokens=budget`.
  - `run_with(client, item, chart, ledger_entry, budget, doctrine_prompt) -> dict` — draft (B/3, temp 0) → verifier (B/6) → critic (B/6) → revision (B/3); verifier/critic system prompts read from `agents/*.md` at call time; revision prompt includes only the deny/nonconformant lines and forbids adding claims; returns text + token sum + stage traces.
  - `run_arm(name, ...)` dispatch.

- [ ] **Step 1: Write failing tests**: `test_with_four_stages_in_order` (fake client records call order and max_tokens), `test_with_revision_gets_only_denials`, `test_bare_single_call_uses_whole_budget`, `test_arm_disqualified_for_run_on_budget_overrun` (sum of B/3+B/6+B/6+B/3 must be ≤ B; force +1 and assert `BudgetExceeded`).
- [ ] **Step 2: Run** → FAIL.
- [ ] **Step 3: Implement**. Stage prompts are literal templates in `tools/eval_arms.py`; verifier/critic content read from the agent files (fail loudly if missing).
- [ ] **Step 4: Run tests** → PASS; ruff clean.
- [ ] **Step 5: Commit** `git add tools/eval_arms.py tests/test_eval_arms.py && git commit -m "feat(evals): with-arm verifier/critic pipeline + bare arm"`

---

### Task 5: Judge + orchestration + report

**Files:**
- Create: `tools/eval_runner.py`
- Create: `tests/test_eval_runner.py`

**Interfaces:**
- Produces:
  - `judge_response(client, item, ledger_entry, chart, anonymized_text, judge_model) -> dict` — one call, temp 0, strict JSON; one retry on parse failure; returns `{"clauses": [...], "pass": bool, "judge_error": bool}`.
  - `anonymize(text: str) -> str` — strips arm labels and leading "Answer:"-style prefixes.
  - `run(items, arms, budget, outdir) -> dict` — precomputes charts via `dashaflow.cast_chart(dob,time,lat,lon,tz)`, runs arms sequentially, scores, disqualifies over-budget arms, returns results dict.
  - `write_report(results, outdir)` — `report.md` + `results.json`; prints SE before scoring; refuses to print any proportion without its Wilson interval (assert in code).
  - CLI: `python tools/eval_runner.py --mode pilot --arms bare,without,with --budget 3000 --out evals/results/<date>`.

- [ ] **Step 1: Write failing tests** with fake client: `test_judge_prompt_is_anonymized` (no `bare|without|with` tokens in the judge system+user text), `test_judge_error_excluded_from_both_arms`, `test_report_requires_intervals` (calling write_report with a proportion lacking an interval raises), `test_se_printed_before_scoring` (report header contains `SE` and the computed value), `test_results_json_schema` (arms/items/verdicts/tokens/latency present).
- [ ] **Step 2: Run** → FAIL.
- [ ] **Step 3: Implement**. Report header restates the §4.3 discipline lines. Excluded items listed explicitly. Disqualified arms printed as `DISQUALIFIED (budget)` with no proportion.
- [ ] **Step 4: Run tests** → PASS; full suite `python -m pytest -q`; ruff.
- [ ] **Step 5: Commit** `git add tools/eval_runner.py tests/test_eval_runner.py && git commit -m "feat(evals): runner orchestration, judge, interval-enforcing report"`

---

### Task 6: The pilot run + §1 amendment + Evidence Log row

**Files:**
- Modify: `evals/README.md` (§1 amendment text as specified; §6 Evidence Log row)
- Create: `evals/results/<YYYY-MM-DD-pilot>/` artifacts

- [ ] **Step 1:** Amend `evals/README.md` §1 with the owner-rewrite paragraph from the design (diagnostic `bare` arm; gate unchanged). Append the Evidence Log row template as a pre-commitment note (`__PENDING__` until the run fills it). Commit separately: `docs(evals): owner rewrite — diagnostic bare arm`.
- [ ] **Step 2:** Verify `OPENROUTER_API_KEY` present (do not print it). Run `python tools/eval_runner.py --mode pilot --arms bare,without,with --budget 3000 --out evals/results/$(date +%F)-pilot`.
- [ ] **Step 3:** Inspect `report.md`: SE line present and pre-scoring; every proportion has an interval; excluded/disqualified sections populated; no trophy language (`grep -Ei "beats|wins|state of the art"` clean).
- [ ] **Step 4:** Fill the Evidence Log row in `evals/README.md` §6 with the real values (SE rule, substituted values, locked gate, arm numbers with intervals, margin with interval, verdict column `pilot — no verdict`, notes = budgets consumed + model ids + excluded items). Append-only.
- [ ] **Step 5:** Commit artifacts + row: `git add evals && git commit -m "feat(evals): equal-cost pilot run + locked gate + Evidence Log row"`.
- [ ] **Step 6:** Report the outcome to the owner **without a ship decision** — the pilot cannot decide by pre-commitment; next measurement is a new, logged run under the locked gate.

## Self-Review

- Spec coverage: three arms (Tasks 3–4), hybrid scoring (1, 5), budget/disqualification (2, 4), anonymization (5), clauses pre-authored (2), SE-before-scoring + Evidence Log (6), §1 amendment (6), artifacts (5), report discipline (5). Design's "20% judge instability controls" — folded into Task 5's judge as an optional `--judge-controls 0.2` that repeats a sample with reordered evidence; test asserts the control set is recorded when enabled.
- Type consistency: `deterministic_verdict`, `ChatClient.complete`, `run_without`/`run_with`/`run_bare`, `judge_response`, `write_report` names stable across tasks.
- Review Focus each mapped to a named test.
- Proportion: ~6 tasks for ~700 lines of code — plan is shorter than the implementation, mostly signatures.
