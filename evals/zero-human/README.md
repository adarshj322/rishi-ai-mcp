# Zero-human conformance screen

**Claim boundary:** chart-grounded, rule-faithful, internally consistent — not validated against expert judgment.

This screen exists for the case where no human expert budget is available. It runs on generated
readings and public resources only. It is a diagnostic, not a substitute for the v2/v2r claim gate.

## What it runs

- **A1 — deterministic chart-fact checks.** Extract chart-fact claims from each reading and
  recompute them against the engine. A contradiction fails the reading. The current checker covers
  degrees and dates, not sign or house claims; that limit is reported, not hidden.
- **A2 — chart-swap.** Generate a reading from the real chart and one from a time-shifted decoy
  chart. If the two readings make the same chart claims, the pipeline is not reading the chart.
  A2 fails on identical texts.
- **A4 — multi-model judge consistency.** Repeat a clause-level judge across three model families
  and K trials. Report agreement and judge errors. This is **consistency**, not quality, and never
  a validity claim.
- **A3 — public exam harness.** Score a model on keyed public questions (BaziQA, CUET-PG). This is
  a competence screen, not a reading-quality measure. See `tools/public_exam_screen.py`.
- **A5 — AI Delphi rubric pre-pass.** Persona panels propose rubric items and report disagreement.
  Without a human panel, dissent fidelity is unmeasurable; report panel disagreement only. See
  `tools/ai_delphi.py`.
- **A7 — public-resource inventory.** What each free corpus licenses and cannot. See
  `public_resources.md`.

## What it does not claim

No reading quality, no correspondence to the person, no predictive truth, no parity with a
jyotishi. A4 measures agreement among judges; a panel can agree on the same wrong thing. The
screen's honest sentence is the claim boundary above.

## Run

```bash
python tools/zero_human_screen.py --cases evals/v2/cases --limit 5 --out /tmp/zero-human
```

Model IDs are exact. `--arm-reasoning` sets the arm effort (`none`, `default`, `max`, ...).
`--judge-models` accepts `model` or `model:effort` entries, e.g.
`deepseek-v4.1-flash:max,muse-spark-1.3-contributor:xhigh`.

Add `--resume` to continue an interrupted run. The screen writes `<out>/partial.json`
after every item and removes it on success. A partial from a different model,
effort, budget or corpus is refused rather than mixed in.

The report is written to `<out>/report.md`; the machine-readable results to `<out>/results.json`.

## Results

| date | commit | items | A1 pass | A2 pass | A4 agreement | notes |
|---|---|---|---|---|---|---|
| `__PENDING__` | `__PENDING__` | `__PENDING__` | `__PENDING__` | `__PENDING__` | `__PENDING__` | `__PENDING__` |
