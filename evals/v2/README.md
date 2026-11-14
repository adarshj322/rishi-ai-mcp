# v2 evaluation — shipped path vs bare MCP

**BINDING — locked before data. Owner: Adarsh J. Ratified: 2026-11-14.**

This file is the v2 pre-commitment. It is the only binding doctrine for the
v2 question. The v1 file (`evals/README.md`) remains the binding record of the
closed verification question: its bar did not clear and verification was cut.
Nothing here re-opens v1.

## 1. The question

At identical token budgets, does the **shipped path** — doctrine/contract plus
sample-and-vote plus the deterministic ground check — beat **bare MCP** — the
same tools and chart data with no doctrine and no sampling — on a
discrimination-focused JyotishQA set?

This is a product-value measurement. It is not a verification-ship gate.

## 2. The decisions (locked)

- **n = 40** items.
- **SE rule:** rule 1, `SE = 0.5 / sqrt(n) = 0.5 / sqrt(40) = 0.079057`.
- **Locked gate:** `delta (shipped − bare) > 0.079057`.
- **Floor:** arms `glm-5.3-flash` at provider-default reasoning; judge
  `deepseek-v4.1-flash` at provider-default reasoning with a 16,000-token cap;
  budget `B = 12,000` output tokens per item per arm; transport OpenCode Go.
  A base-model, decoding, budget, or engine change re-opens this as a new
  pilot before any verdict (v1 §10 applies by analogy).
- **Consequence — informational / claim gate.** The result decides **only**
  whether the plugin may claim measurable lift over bare MCP on this corpus:
  - Gate clears: the plugin may report that the shipped path demonstrated lift
    on this corpus, with intervals; no predictive-validity claim follows.
  - Gate does not clear: the plugin must say lift was **not demonstrated** on
    this corpus and may make no comparative claim. The doctrine layer is not
    automatically removed; it remains writing guidance. Any product change is a
    separate owner decision, not a result of this file.
- **No tuning:** no prompt, rubric, corpus, model, budget, or scoring change may
  be made between the pilot and the verdict. Re-runs are new rows; no
  run-until-favorable.

## 3. Arms and budget

- **`shipped`** — the doctrine/contract prompt; three independent samples at
  temperature 0.7 with distinct seeds; deterministic pick-best. Sample caps are
  `B/3` each.
- **`bare`** — no doctrine; one call at temperature 0; whole budget `B`.
- One shared inference floor: same base model, engine, decoding configuration,
  prompts outside the arm difference, and total budget. Both arms are
  anonymized before judging.

## 4. Corpus construction (before any arm output)

- **40 items**, authored and committed before the first run.
- **Discrimination first.** Each item targets one specific failure a bare
  answer plausibly makes: a missing required ground, a wrong dasha window, a
  fabricated degree, a sycophantic premise adoption, a remedy overreach, or a
  fear/death framing. Items where the doctrine text alone trivially guarantees
  a pass, or where both arms trivially pass, are excluded.
- **1–3 mandatory clauses per item**, not 4–6. Item-level all-or-nothing scoring
  stays; the conjunction is shorter so a competent answer can pass.
- **Tags:** `chart-grounded` (deterministic required grounds enforced) and
  `interpretation-only` (judge-enforced).
- **No reuse of v1 items** without re-tagging. The v1 corpus remains the record
  of the closed question.
- **Construction ledger:** every item carries id, prompt, birth data, expected
  verdict, required grounds, tag, and authoring rationale, committed before the
  first arm output.

## 5. Scoring

1. Deterministic check first: fabrication against the chart whitelist and
   mechanical required grounds.
2. Reference-guided judge second: cross-family, anonymized, one verdict per
   mandatory clause, no arm labels, `no evidence found` when a clause is unmet.
3. **Primary metric:** item pass (all mandatory clauses pass). **Secondary:**
   clause-level pass rate. The gate uses item pass only.
4. Every proportion carries a Wilson interval; the delta carries a paired
   bootstrap interval; no point estimate stands alone.

## 6. Instrument requirements before the first run

Correctness fixes, not leniency:
- Relational degrees ("within 1°", "3.6° apart", "from the cusp") are not
  fabricated absolute positions.
- Degree-to-body attribution uses the nearest body mention, not any body within
  a wide window.
- Date checks accept only dates supported by a chart period at the intended
  granularity.
- Transit and natal planet degrees are tracked separately.
- Reuse the v1 resume/config, gate/floor guard, manifest, and paired-interval
  machinery; the scoring hash covers prompts, agents, ledger, and case files.
- A 1–2 item smoke precedes the pilot; a truncated or judge-error run is
  INVALID, not silently shrunk.

## 7. Run protocol

1. **Smoke** — 1–2 items, plumbing and budget only; not a measurement.
2. **Pilot** — full 40 items. Locks the noise floor and the gate; never decides.
3. **Verdict** — full 40 items, same floor and instrument. The only run that
   reads the gate.
4. Any run with exclusions, disqualifications, judge errors, or cap hits is
   INVALID and must be reported as such; it is not a verdict.

## 8. Reporting and Evidence Log

- One append-only Evidence Log for v2; one row per measurement.
- Intervals everywhere; the gate value lives only in this file and the log.
- No trophy language, no external benchmark, no predictive-accuracy claim, no
  point estimate standing alone.
- The result is reported whether it flatters the doctrine or not.
- Release notes may state that the claim gate was or was not cleared; they may
  not cite a point estimate or a benchmark comparison.

| date | commit | corpus size | SE rule | arm | margin observed | verdict | notes |
|---|---|---|---|---|---|---|---|
| 2026-11-14 | 869df95 | 40 | rule 1: SE = 0.079057; locked gate delta > 0.079057 | bare 13/40 = 0.325 [0.2008, 0.4798]; shipped 22/40 = 0.550 [0.3983, 0.6929] | delta = +0.225 [0.075, 0.375]; consumed 31,246 bare-arm tokens / 109,799 shipped-arm tokens | pilot — no verdict | GLM/DeepSeek/default/12000/OpenCode Go; no exclusions, disqualifications, judge errors, or cap hits; corpus 40 sampled VedAstro HF births (names dropped, UTC; see cases/SOURCE.md); paired interval recomputed after fixing a v2 arm-name bug in the bootstrap (reporting-only; pass/fail and gate unchanged; no corpus or scoring change) |

## 9. Change control

Only an explicit owner rewrite changes this file. Every change is a new row
with date, commit, reason, and the owner's name — appended, never edited in.
Data never changes it. Results never change it. Time never changes it.
