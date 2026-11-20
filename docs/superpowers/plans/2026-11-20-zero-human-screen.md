# Zero-Human Conformance Screen — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a zero-human screen that runs A1 deterministic chart-fact checks, A2 chart-swap, A4 multi-model judge consistency, and the A3/A5 public-resource harnesses, with A7 documented, under a binding claim boundary: conformance and reliability, not expert-validated reading quality.

**Architecture:** Reuse the v2 case/ledger format and the existing `eval_arms` + `eval_scoring` primitives. A new `tools/zero_human_screen.py` generates a shipped reading and a decoy-chart reading per item, runs A1/A2 deterministically, and runs A4 by repeating a judge across three models. A3 (public exam) and A5 (AI Delphi) are separate thin harnesses; A7 is an inventory document.

**Tech Stack:** Python 3.10+, pytest/unittest, existing `openai` client, `dashaflow`, no new dependencies.

**Spec:** `research/notes/final_report_vedic-ai-validation-2cc3db.md` §4, §6, §7C.

## Global Constraints

- No human recruitment, no human labels, no expert spend.
- The report must contain this exact sentence: “chart-grounded, rule-faithful, internally consistent — not validated against expert judgment.”
- Reuse `evals/v2/cases/` and its ledger; do not create a new corpus or new model floor.
- No new dependencies. Tests never call the network; use fake clients.
- A1/A2 are deterministic; A4 measures agreement/consistency only, never validity.
- The screen is a diagnostic, not a release gate that replaces the v2 claim gate.

## Review Focus

- **A2 false pass:** a chart-blind model can produce identical real/decoy readings; the test must show that identical texts fail A2.
- **A4 misuse:** agreement is not validity; the report must label it “consistency,” never “quality” or “validated.”
- **A1 blind spot:** `find_fabrications` checks degrees and dates, not sign/house claims; the report must state the limit.
- **A3 key drift:** public exam keys can be wrong or mis-transcribed; the harness must report per-item errors, not silently trust the key.
- **A5 dissent limit:** with no human panel, dissent fidelity is unmeasurable; report panel disagreement only.

---

### Task 1: Claim boundary and A7 public-resource inventory

**Files:**
- Create: `evals/zero-human/README.md`
- Create: `evals/zero-human/public_resources.md`
- Test: `tests/test_zero_human_docs.py`

**Interfaces:**
- Produces: the binding claim boundary and the A7 inventory later tasks cite.

- [ ] **Step 1: Write the failing test**

```python
def test_zero_human_boundary_and_inventory():
    root = pathlib.Path(__file__).resolve().parents[1]
    readme = (root / "evals" / "zero-human" / "README.md").read_text()
    assert "chart-grounded, rule-faithful, internally consistent — not validated against expert judgment" in readme
    assert "A1" in readme and "A2" in readme and "A4" in readme
    resources = (root / "evals" / "zero-human" / "public_resources.md").read_text()
    for name in ("OurNakshatra", "Jyotish-LLM", "BaziQA", "CUET-PG", "BPHS"):
        assert name in resources
    assert "not validated" in readme
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_zero_human_docs.py -v`
Expected: FAIL with `FileNotFoundError` (the docs do not exist).

- [ ] **Step 3: Write the docs**

`README.md`: the claim boundary, the A1/A2/A4 definitions, the A3/A5/A7 inventory pointers, the “what this does not validate” section, and the command example:

```
python tools/zero_human_screen.py --cases evals/v2/cases --limit 5 --out /tmp/zero-human
```

`public_resources.md`: one row per resource — OurNakshatra (602 pairs, CC-BY-4.0), Jyotish-LLM (1M synthetic rows, Apache-2.0), BaziQA (555 items/117 charts, public repo), CUET-PG Jyotish (5 papers, 4 NTA keys), BPHS/AstroCentral (rule corpus), JPL Horizons/Swiss Ephemeris (computation), AstroTalk/AstroYogi (cost benchmarks). State what each licenses and cannot.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_zero_human_docs.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add evals/zero-human/README.md evals/zero-human/public_resources.md tests/test_zero_human_docs.py
git commit -m "docs(evals): zero-human claim boundary and public-resource inventory"
```

---

### Task 2: A1/A2 deterministic screen

**Files:**
- Create: `tools/zero_human_screen.py`
- Test: `tests/test_zero_human_screen.py`

**Interfaces:**
- Consumes: `eval_scoring.find_fabrications`, `eval_scoring.extract_numeric_claims`, `eval_arms.run_without`, `eval_runner.precompute_chart`, `eval_runner.load_ledger`, `eval_runner.load_prompt`.
- Produces:
  - `shift_birth(birth: dict, hours: int = 12) -> dict`
  - `chart_text_divergence(real_text: str, decoy_text: str, real_chart: dict) -> dict` with keys `real_fabrications`, `decoy_fabrications`, `claim_overlap`, `pass`.
  - `screen_item(item: dict, entry: dict, client, doctrine_prompt: str, arm_model: str, budget: int, reasoning) -> dict` with keys `a1`, `a2`, `real_text`, `decoy_text`, `tokens`.

- [ ] **Step 1: Write the failing tests**

```python
def test_a1_flags_fabricated_degree():
    chart = {"planets": {"Sun": {"degree": 10.0}}}
    result = chart_text_divergence("The Sun is at 99.99°.", "The Sun is at 10.0°.", chart)
    assert result["real_fabrications"] == ["99.99°"]

def test_a2_fails_identical_texts():
    chart = {"planets": {"Sun": {"degree": 10.0}}}
    text = "The Sun is at 10.0°."
    result = chart_text_divergence(text, text, chart)
    assert result["claim_overlap"] == 1.0
    assert result["pass"] is False

def test_a2_passes_when_decoy_diverges():
    chart = {"planets": {"Sun": {"degree": 10.0}}}
    result = chart_text_divergence(
        "The Sun is at 10.0°.", "The Sun is at 22.0° and the Moon is at 5.0°.", chart
    )
    assert result["pass"] is True

def test_shift_birth_changes_time():
    assert shift_birth({"dob": "2000-01-01", "time": "04:20", "lat": 0, "lon": 0, "tz": "UTC"})["time"] == "16:20"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_zero_human_screen.py -v`
Expected: FAIL with `ImportError` / `NameError` (`zero_human_screen` missing).

- [ ] **Step 3: Implement the minimal functions**

`shift_birth` parses `time` with `datetime.time.fromisoformat`, adds `hours` modulo 24, returns a copy with the new `"HH:MM"`. `chart_text_divergence` calls `find_fabrications` on both texts against `real_chart`, computes `extract_numeric_claims` Jaccard, and returns `pass = len(decoy_fab) > len(real_fab) or claim_overlap < 0.5`. `screen_item` casts the real chart via `precompute_chart(item)`, casts the decoy chart from `shift_birth(item["birth"])`, runs `run_without` twice with the same doctrine prompt/ledger, and returns the A1/A2 result.

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_zero_human_screen.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/zero_human_screen.py tests/test_zero_human_screen.py
git commit -m "feat(evals): zero-human A1/A2 chart-fact and chart-swap screen"
```

---

### Task 3: A4 multi-model judge consistency

**Files:**
- Modify: `tools/zero_human_screen.py`
- Modify: `tests/test_zero_human_screen.py`

**Interfaces:**
- Consumes: `eval_runner.judge_response`.
- Produces: `judge_consistency(judge_client, item, entry, chart, text, judge_models: list[str], trials: int) -> dict` with keys `per_model`, `pairwise_agreement`, `judge_errors`, `pass`.

- [ ] **Step 1: Write the failing tests**

```python
def test_judge_consistency_perfect():
    client = FakeJudgeClient([_judge_json("pass")] * 12)
    result = judge_consistency(client, {"id": "x", "prompt": "q"}, LEDGER, CHART, "answer", ["m1", "m2"], 3)
    assert result["pairwise_agreement"] == 1.0
    assert result["judge_errors"] == 0
    assert result["pass"] is True

def test_judge_consistency_flags_split():
    client = FakeJudgeClient([_judge_json("pass"), _judge_json("fail")] * 6)
    result = judge_consistency(client, {"id": "x", "prompt": "q"}, LEDGER, CHART, "answer", ["m1", "m2"], 3)
    assert result["pairwise_agreement"] < 0.8
    assert result["pass"] is False
```

Use the existing `FakeJudgeClient` / `_judge_json` / `LEDGER` / `CHART` fixtures from `tests/test_eval_runner.py` (import or copy the minimal helper).

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_zero_human_screen.py -v`
Expected: FAIL with `NameError: judge_consistency`.

- [ ] **Step 3: Implement `judge_consistency`**

For each `model` in `judge_models`, call `judge_response` `trials` times; collect `(model, i, pass, clauses)`. Count `judge_errors`. Pairwise agreement is the fraction of all same-item verdict pairs with identical `pass`; clause agreement is the fraction of clause pairs with identical verdicts. `pass = pairwise_agreement >= 0.8 and judge_errors == 0`. Never label it quality.

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_zero_human_screen.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/zero_human_screen.py tests/test_zero_human_screen.py
git commit -m "feat(evals): zero-human A4 judge-consistency panel"
```

---

### Task 4: CLI and report

**Files:**
- Modify: `tools/zero_human_screen.py`
- Modify: `tests/test_zero_human_screen.py`

**Interfaces:**
- Produces: `write_report(results: dict, outdir: str) -> None`, `main(argv=None) -> int`.
- CLI flags: `--cases`, `--items`, `--limit`, `--out`, `--transport`, `--arm-model`, `--judge-models`, `--trials`, `--budget`, `--arm-reasoning`.

- [ ] **Step 1: Write the failing report test**

```python
def test_report_keeps_boundary_and_never_says_validated(tmp_path):
    write_report({"items": [], "summary": {"a1": [0, 0], "a2": [0, 0], "a4": [0, 0]}}, str(tmp_path))
    text = (tmp_path / "report.md").read_text()
    assert "not validated against expert judgment" in text
    assert "validated" not in text.lower().replace("not validated", "")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_zero_human_screen.py::test_report_keeps_boundary_and_never_says_validated -v`
Expected: FAIL with `NameError`.

- [ ] **Step 3: Implement the CLI and report**

`write_report` writes the exact boundary, the A1/A2/A4 counts, the per-item table, and the limits (A1 checks degrees/dates only; A4 is consistency, not quality). `main` parses args, loads items/ledger/doctrine, runs `screen_item` and `judge_consistency`, writes `results.json` + `report.md`, and prints the report path.

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_zero_human_screen.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/zero_human_screen.py tests/test_zero_human_screen.py
git commit -m "feat(evals): zero-human screen CLI and report"
```

---

### Task 5: A3 public exam harness

**Files:**
- Create: `tools/public_exam_screen.py`
- Create: `evals/zero-human/public_exam/README.md`
- Test: `tests/test_public_exam_screen.py`

**Interfaces:**
- Produces: `score_exam(client, questions: list[dict], model: str, budget: int) -> dict`; question shape `{"id": str, "question": str, "options": {"A": str, ...}, "answer": "A"}`; result keys `correct`, `n`, `accuracy`, `errors`.

- [ ] **Step 1: Write the failing test**

```python
def test_score_exam_marks_correct_and_wrong():
    questions = [
        {"id": "q1", "question": "2+2?", "options": {"A": "4", "B": "5"}, "answer": "A"},
        {"id": "q2", "question": "3+3?", "options": {"A": "5", "B": "6"}, "answer": "B"},
    ]
    class C:
        def complete(self, *a, **k):
            return {"text": "A", "output_tokens": 1, "input_tokens": 1, "latency_s": 0.0}
    result = score_exam(C(), questions, "m", 100)
    assert result["correct"] == 1 and result["n"] == 2 and result["accuracy"] == 0.5
```

- [ ] **Step 2: Run test to verify it fails** — `pytest tests/test_public_exam_screen.py -v` → FAIL.

- [ ] **Step 3: Implement `score_exam`** — prompt the model with the question/options, parse the first A–D letter, compare to `answer`; collect per-item errors. The README explains how to populate the JSONL from BaziQA and CUET-PG, and warns that CUET tests shastra recall, not reading quality.

- [ ] **Step 4: Run test to verify it passes** — PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/public_exam_screen.py evals/zero-human/public_exam/README.md tests/test_public_exam_screen.py
git commit -m "feat(evals): public exam competence screen"
```

---

### Task 6: A5 AI Delphi rubric pre-pass

**Files:**
- Create: `tools/ai_delphi.py`
- Test: `tests/test_ai_delphi.py`

**Interfaces:**
- Produces: `run_delphi(client, topic: str, personas: list[str], rounds: int, model: str, budget: int) -> dict`; result keys `items` (list of `{"text": str, "mentions": int}`) and `panel_disagreement` (1 − max share).

- [ ] **Step 1: Write the failing test**

```python
def test_delphi_counts_mentions():
    class C:
        def complete(self, system, user, **k):
            return {"text": "- chart-fact accuracy\n- rule fidelity", "output_tokens": 1, "input_tokens": 1, "latency_s": 0.0}
    result = run_delphi(C(), "rubric", ["p1", "p2"], 1, "m", 100)
    assert result["items"][0]["mentions"] == 2
    assert 0.0 <= result["panel_disagreement"] <= 1.0
```

- [ ] **Step 2: Run test to verify it fails** — FAIL.

- [ ] **Step 3: Implement `run_delphi`** — for each persona/round, prompt for 5 bullet items; parse `- ` lines; count normalized mentions; `panel_disagreement = 1 - max(mentions)/sum(mentions)`. The tool cannot measure human dissent fidelity; state that in the docstring.

- [ ] **Step 4: Run test to verify it passes** — PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/ai_delphi.py tests/test_ai_delphi.py
git commit -m "feat(evals): AI Delphi rubric pre-pass"
```

---

## Self-Review

- **Spec coverage:** A1 (Task 2), A2 (Task 2), A3 (Task 5), A4 (Task 3), A5 (Task 6), A7 (Task 1). The claim boundary is Task 1 and the report is Task 4.
- **Step scan:** each step is a test, a run, a minimal implementation, a run, a commit. No “handle edge cases” lines.
- **Type consistency:** `chart_text_divergence` keys are used by `screen_item` and the report; `judge_consistency` keys are used by the report; `score_exam` and `run_delphi` are standalone.
- **Review Focus:** A2 chart-blind fixture (Task 2), A4 label (Task 4 report test), A1 limit (Task 4 report), A3 per-item errors (Task 5), A5 dissent limit (Task 6 docstring).
- **Proportion:** six small tasks; no task writes more than a focused module and its tests.

## Execution Handoff

Plan saved. The user has already approved the protocol; before implementation, confirm this scope and choose **native** (recommended: six tightly coupled tasks, small codebase) or subagent-driven (fresh reviewer per task).
