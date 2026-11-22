# Zero-human conformance screen

**Claim boundary:** chart-grounded, rule-faithful, internally consistent — not validated against expert judgment.

| Check | Pass |
|---|---|
| A1 chart-fact | 16/20 |
| A2 chart-swap | 14/20 |
| A4 judge consistency | 12/20 |

Arm output tokens: 844795

## Per item

| Item | A1 | Claims | Fabrications | A2 | Claim overlap | A4 agreement | A4 clauses |
|---|---|---|---|---|---|---|---|
| v2-g-01 | pass | 13 | — | pass | 0.03 | 1.00 | 1.00 |
| v2-g-02 | pass | 10 | — | pass | 0.00 | 1.00 | 1.00 |
| v2-g-03 | pass | 22 | — | pass | 0.03 | 0.50 | 0.83 |
| v2-g-04 | pass | 15 | — | pass | 0.03 | 1.00 | 1.00 |
| v2-g-05 | pass | 3 | — | pass | 0.00 | 1.00 | 1.00 |
| v2-g-06 | pass | 4 | — | pass | 0.00 | 1.00 | 1.00 |
| v2-g-07 | pass | 2 | — | not exercised | 0.00 | 0.44 | 0.81 |
| v2-g-08 | not exercised | 0 | — | not exercised | 0.00 | 0.50 | 0.83 |
| v2-g-09 | pass | 17 | — | pass | 0.00 | 0.44 | 0.81 |
| v2-g-10 | pass | 12 | — | pass | 0.05 | 1.00 | 1.00 |
| v2-g-11 | pass | 5 | — | pass | 0.33 | 1.00 | 1.00 |
| v2-g-12 | pass | 4 | — | pass | 0.33 | 0.78 | 1.00 |
| v2-g-13 | pass | 6 | — | pass | 0.43 | 1.00 | 1.00 |
| v2-g-14 | pass | 5 | — | pass | 0.33 | 0.78 | 1.00 |
| v2-g-15 | pass | 5 | — | pass | 0.00 | 1.00 | 1.00 |
| v2-g-16 | pass | 4 | — | pass | 0.00 | 1.00 | 1.00 |
| v2-g-17 | not exercised | 0 | — | not exercised | 1.00 | 1.00 | 1.00 |
| v2-g-18 | not exercised | 0 | — | not exercised | 1.00 | 1.00 | 1.00 |
| v2-g-19 | not exercised | 0 | — | not exercised | 1.00 | 0.78 | 0.93 |
| v2-g-20 | pass | 1 | — | not exercised | 0.00 | 0.61 | 0.76 |

A1 exercised: 16/20; A2 exercised: 14/20

## Limits

- A1 checks degree and date claims only. Sign and house claims are not checked.
- A1 counts a reading as pass only when it asserted at least one numeric claim; zero claims read as not exercised.
- A2 requires both readings to assert at least one numeric claim; otherwise it reads as not exercised, not chart-blind.
- A2 shows chart sensitivity, not chart truth.
- A4 measures agreement among judges. A panel can agree on the same wrong verdict.
- Nothing here measures reading quality or correspondence to the person.

## Provenance

- generated_at: 2026-11-22T07:12:34.157905+00:00
- transport: opencode-go
- arm_model: hy4-flash-free
- arm_reasoning: max
- judge_models: deepseek-v4.1-flash, muse-spark-1.3-contributor, beam-free
- judge_reasoning: {"beam-free": "max", "deepseek-v4.1-flash": "max", "muse-spark-1.3-contributor": "xhigh"}
- trials: 3
- budget: 120000
- items: grounding.jsonl
- engine: {"dashaflow_file": "/home/adarsh/cursorProjects/dashaflow/src/dashaflow/__init__.py", "dashaflow_version": "1.5.3"}
