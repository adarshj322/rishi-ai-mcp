# Zero-human conformance screen

**Claim boundary:** chart-grounded, rule-faithful, internally consistent — not validated against expert judgment.

| Check | Pass |
|---|---|
| A1 chart-fact | 16/20 |
| A2 chart-swap | 15/20 |
| A4 judge consistency | not run |

Arm output tokens: 861676

## Per item

| Item | A1 | Claims | Contradictions | A2 | Claim overlap | A4 agreement | A4 clauses |
|---|---|---|---|---|---|---|---|
| v2-g-01 | fail | 11 | D9 Mars in Libra (chart: Scorpio) | fail | 0.04 | not run | not run |
| v2-g-02 | pass | 13 | — | fail | 0.16 | not run | not run |
| v2-g-03 | pass | 18 | — | pass | 0.00 | not run | not run |
| v2-g-04 | pass | 8 | — | pass | 0.00 | not run | not run |
| v2-g-05 | pass | 7 | — | pass | 0.07 | not run | not run |
| v2-g-06 | pass | 9 | — | pass | 0.07 | not run | not run |
| v2-g-07 | fail | 6 | D2 Lagna in Pisces (chart: Leo) | pass | 0.00 | not run | not run |
| v2-g-08 | pass | 4 | — | fail | 0.00 | not run | not run |
| v2-g-09 | pass | 17 | — | pass | 0.07 | not run | not run |
| v2-g-10 | pass | 12 | — | pass | 0.14 | not run | not run |
| v2-g-11 | pass | 7 | — | pass | 0.08 | not run | not run |
| v2-g-12 | pass | 8 | — | pass | 0.07 | not run | not run |
| v2-g-13 | pass | 7 | — | pass | 0.00 | not run | not run |
| v2-g-14 | pass | 7 | — | pass | 0.11 | not run | not run |
| v2-g-15 | pass | 12 | — | pass | 0.00 | not run | not run |
| v2-g-16 | pass | 9 | — | pass | 0.05 | not run | not run |
| v2-g-17 | pass | 1 | — | pass | 0.00 | not run | not run |
| v2-g-18 | pass | 1 | — | pass | 0.00 | not run | not run |
| v2-g-19 | fail | 2 | Saturn in Aquarius (chart: Scorpio), D9 Saturn in Aquarius (chart: Leo) | not exercised | 0.00 | not run | not run |
| v2-g-20 | not exercised | 0 | — | not exercised | 1.00 | not run | not run |

A1 exercised: 19/20; A2 exercised: 18/20

## Limits

- A1 checks degrees, dates, signs and houses. Aspects, yogas and dignities are not checked.
- A1 scopes D10/D9 and transit claims when labelled; relative houses ("from Moon") and ambiguous trailing-varga claims are skipped.
- A1 counts a reading as pass only when it asserted at least one checkable claim; zero claims read as not exercised.
- A2 requires both readings to assert at least one numeric, sign or house claim; otherwise it reads as not exercised, not chart-blind.
- A2 shifts birth time by 12 hours and date by 15 days so sign claims diverge.
- A2 shows chart sensitivity, not chart truth.
- A4 measures agreement among judges. A panel can agree on the same wrong verdict.
- Nothing here measures reading quality or correspondence to the person.

## Provenance

- generated_at: 2026-11-22T10:20:37.154853+00:00
- transport: opencode-go
- arm_model: hy4-flash-free
- arm_reasoning: max
- judge_models: 
- judge_reasoning: {}
- trials: 3
- budget: 120000
- items: grounding.jsonl
- engine: {"dashaflow_file": "/home/adarsh/cursorProjects/dashaflow/src/dashaflow/__init__.py", "dashaflow_version": "1.5.3"}
