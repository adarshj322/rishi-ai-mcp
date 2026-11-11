# v2 evaluation — shipped path vs bare MCP (DRAFT)

**Status: DRAFT. Not binding. Do not run under this document.**

This is a proposal for a new pre-commitment. It becomes binding only when the
owner ratifies it as `evals/v2/README.md` in a separate owner rewrite. Until
then, the v1 file (`evals/README.md`) remains the only binding evaluation
doctrine, and its verification question is closed: the bar did not clear and
verification was cut.

## 1. The question v2 asks

At identical token budgets, does the **shipped path** — doctrine/contract plus
sample-and-vote plus the deterministic ground check — beat **bare MCP** — the
same tools and chart data with no doctrine and no sampling — on a
discrimination-focused JyotishQA set?

This is not the v1 question. v1 asked whether the *verification layer* beat the
doctrine path; it answered no and cut verification. v1 never gated the shipped
path against bare MCP, and its 26-item corpus sat near the floor for every arm
(7–15% pass), so it could not answer this.

## 2. Arms and floor

- **`shipped`** — the doctrine/contract prompt, three independent samples at
  temperature 0.7 with distinct seeds, deterministic pick-best (the v1
  `without` arm).
- **`bare`** — no doctrine, one call at temperature 0, whole budget (the v1
  `bare` arm).
- Equal output-token cap `B` per item per arm: `shipped` = 3 × B/3, `bare` = B.
- One shared inference floor: same base model, engine, decoding configuration,
  prompts outside the arm difference, and token budget. A floor change resets
  the process to a new pilot (v1 §10 applies by analogy).
- Proposed floor for owner decision: `glm-5.3-flash` (provider-default
  reasoning), judge `deepseek-v4.1-flash` (provider-default reasoning), B =
  12,000, OpenCode Go. Keeping the v1 verdict floor reduces one variable.

## 3. Corpus construction (before any arm output is seen)

- **Size:** n = 40 proposed. Under SE rule 1 this gives `0.5/√40 = 0.079057`.
  The owner may set a different n before ratification; the gate follows n and
  is recorded at the pilot, not chosen after scores.
- **Discrimination first.** Each item targets one specific failure a bare
  answer plausibly makes: a missing required ground, a wrong dasha window, a
  fabricated degree, a sycophantic premise adoption, a remedy overreach, or a
  fear/death framing. Items where the doctrine text alone trivially guarantees
  a pass are excluded; items where both arms trivially pass are excluded.
- **Clause count:** 1–3 mandatory clauses per item, not 4–6. v1's all-or-nothing
  bundles pushed every arm to the floor; v2 keeps all-or-nothing scoring but
  reduces the conjunction length so a competent answer can pass.
- **Tags:** `chart-grounded` (deterministic required grounds enforced) and
  `interpretation-only` (judge-enforced). Same construction ledger discipline
  as v1: id, prompt, birth data, expected verdict, required grounds, tag,
  authoring rationale — all committed before the first run.
- **No reuse of v1 items** without re-tagging; the v1 corpus remains the record
  of the closed question and is not silently re-weighted.

## 4. Scoring

1. Deterministic check first: fabrication against the chart whitelist and
   mechanical required grounds (with v1's alias/ordinal handling and the
   instrument fixes below).
2. Reference-guided judge second: cross-family, anonymized, one verdict per
   mandatory clause, no arm labels, `no evidence found` when a clause is unmet.
3. Primary metric: item pass (all mandatory clauses pass). Secondary metric:
   clause-level pass rate with intervals. The gate uses item pass only.
4. Every proportion carries a Wilson interval; the delta carries a paired
   bootstrap interval; no point estimate stands alone.

## 5. Pre-commitment (to be ratified)

- **SE rule:** rule 1, `SE = 0.5/√n`, computed before any item is scored.
- **Locked gate:** `delta (shipped − bare) > SE`.
- **Pilot rule:** the first full-corpus measurement is the noise floor only; it
  locks the gate and never decides. A later same-floor verdict decides.
- **Failure branch:** if the margin is possible and not cleared, the plugin makes
  no claim of measurable lift over bare MCP. The doctrine remains writing
  guidance; no benchmark or accuracy claim ships.
- **Expansion:** if the margin is impossible at n, expand the set; never relax
  the bar.
- **No tuning:** no prompt, rubric, corpus, model, or budget changes between
  pilot and verdict. Re-runs are new rows; no run-until-favorable.

## 6. Instrument requirements before the first run

These are correctness fixes, not leniency:

- Relational degrees ("within 1°", "3.6° apart", "from the cusp") are not
  fabricated absolute positions.
- Degree-to-body attribution uses the nearest body mention, not any body within
  a wide window.
- Date checks accept only dates supported by a chart period at the intended
  granularity; not every date inside a multi-year dasha span.
- Transit and natal planet degrees are tracked separately; a transit degree is
  not accepted as a natal degree by coincidence.
- The v1 resume/config, gate/floor guard, manifest, and paired-interval
  machinery are reused; the scoring hash covers prompts, agents, ledger, and
  case files.
- A 1–2 item smoke precedes the pilot; a truncated or judge-error run is
  INVALID, not silently shrunk.

## 7. Reporting

- One Evidence Log per measurement; append-only; intervals everywhere.
- The gate value lives only in the Evidence Log, never in release prose.
- No trophy language, no external benchmark, no point estimate alone.
- The result is reported whether it flatters the doctrine or not.

## 8. Owner decisions required before ratification

1. Final n (proposed 40) and the resulting gate.
2. Floor: keep GLM/DeepSeek at 12,000, or choose another; changing it changes
   the experiment, not the question.
3. Whether the result is informational or a product gate — i.e., what happens
   to the doctrine layer if it does not beat bare MCP.
4. Ratification as `evals/v2/README.md`, with the owner's name and date, before
   any corpus item or arm output exists.
