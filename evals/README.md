# Eval Gate Pre-Commitment — rishi ground-truth plugin

This file is the plugin's honesty checkpoint. It states, in writing and before any measurement is taken, exactly what the plugin must prove before tool-grounded verification ships, what happens if it does not prove it, and what is never allowed to happen afterwards. It is binding. It is the only document of its kind in this repository.

It binds the maintainer of this repository, always. Anyone who builds, measures, reviews, or releases this plugin is bound by every clause in it.

It does not bind rishi at runtime. rishi never reads this file. No skill, agent, hook, or MCP tool loads it, references it as a feature, or cites it to a user. It is NOT shipped in the plugin bundle: it is not in the manifest, not in `skills/`, not in `.mcp.json`, not in any host install path. Workflows, SKILL.md files, and reference doctrine must not reference this file as a bill of sale, a selling point, or a benchmark result. The gate exists; the gate's existence is statable. The gate's outcomes are reported here and nowhere else.

No clause in this file is softened after data exists. No clause in this file is renegotiated against a measurement. The only way this file changes is an explicit owner rewrite, recorded in the Evidence Log with the reason. Nothing else rewrites it — not convenience, not a good result, not a bad one.

## 0. Reading order

Read this file in order, once, and then every clause applies every time. §1 is the vocabulary; §2–§3 describe what is measured and on what floor; §4 is the pre-commitment itself and is the binding core; §5–§6 are logs that exist to keep §4 honest; §7 is the pre-registered stop rules; §8–§11 are enforcement, scope, change control. Nothing here is background. Nothing here is aspirational. This is binding doctrine, in force from the moment it is committed.

---

## 1. Definitions

Read these before the clauses. They are used exactly as defined, everywhere in this file.

- **with / without arms** — `with` = the plugin with tool-grounded verification (hesitation gate, verifier subagents, per-claim approvals). `without` = the plugin with verification disabled; sample-and-vote plus the deterministic tool-check. These are the only two arms. There is no third arm, no variant arm, no "partially verified" arm.
- **diagnostic arm `bare`** *(added by owner rewrite 2026-11-08)* — a third, DIAGNOSTIC arm: the tools with no doctrine, no contract, no verification, measured only to report the full plugin's lift over a bare-MCP baseline for the owner. It never enters the gate. The gate remains exactly `with` minus `without` under Section 4, unchanged. `bare` results are informational and carry all Section 4.3 reporting discipline.
- **delta** — with-minus-without per-item correctness on the JyotishQA seed set, expressed as a proportion difference.
- **standard error (SE)** — the seed-set standard error from Section 4.1, the noise floor against which the gate is locked.
- **verdict-capable n** — a set size at which a positive margin is possible at all (n large enough that a delta above the locked SE is achievable on the item set). Below verdict-capable n, only the pilot rule applies; no ship decision is taken.
- **locked gate** — the gate value recorded at first measurement. It is final. It is not re-derived, re-rounded, or re-interpreted after it is recorded, and it is not adjusted when the answer is inconvenient.
- **inference floor** — the fixed substrate shared by both arms: base model, engine version, decoding configuration, prompts outside the verification machinery, and token budget per turn.
- **intervals** — confidence intervals reported with every result. A result without its interval is not a result; it is a vibe.
- **n** — the number of seed items in play for a given measurement.

## 2. The corpora

### 2.1 The JyotishQA seed set

Built by this project, in this repository, under `evals/`. It is not derived from any published benchmark and makes no publication claim. It is not a valid comparison point against any external leaderboard, and no external leaderboard is a comparison point for it.

**Size.** 10–30 interpretation questions at the time of first measurement — no more, no fewer. If the set cannot yield a positive margin at this size, it is expanded per Section 4.2(b); expansion is the only permitted growth, and every expansion is logged in the Evidence Log.

**Construction rule.** Every question is tagged, at construction time, as exactly one of:

| tag | what it means | scoring |
|---|---|---|
| `chart-grounded` | the question has a verifiable chart ground; the required planetary positions are calculated via the engine | scored against engine output; off-by stated per field |
| `interpretation-only` | the question is about framing, wording, or emphasis where no single chart fact settles it | scored against a machine-auditable outcome criterion stated before any run |

**Tagging discipline.** The tag is fixed at creation. A question whose chart ground turns out not to be calculable via the engine is re-tagged `interpretation-only` (with its criterion) or excluded — never scored against a recollection. A question whose outcome cannot be made machine-auditable is excluded. An item is never scored against an astrologer's memory of a chart, and never against "what a good reading would say".

**Scoring rule for `interpretation-only` items.** Each such item carries a machine-auditable outcome criterion stated before any run. The criterion names the chart field, the expected outcome, and what counts as off; for example:

```text
item:        A reading asserts a decisive career window in the 10th lord's dasha.
chart field: 10th lord (whole-sign), its sign, its house, and the running dasha at reading time
correct:     "dasha result requires the 10th lord dasha-antardasha to be operative" — the operand stated in the reading matches the engine's dasha timeline; off-by = any other operative pair
```

Second example of the same shape: "the Sade Sati verdict requires the Saturn–Moon sign distance; correct = the distance the engine returns; off-by = any other distance." Third: "the dasha result requires the Moon's nakshatra; correct = the nakshatra the engine returns; off-by = any other nakshatra." If an item would require expert judgment without a panel to score meaningfully, the item is excluded from the seed set entirely — not adapted, not approximated, excluded. If a panel of astrologers would be required to score the item at all, the item is excluded. The seed set is therefore not an expert-opinion dataset and must never be presented as one.

**What the seed set is not.** It asserts nothing about predictive power, correspondence validity, or the truth of any astrological claim. It measures whether tool-grounded verification changes per-turn output correctness on this project's own reading tasks at equal token cost. That is all it measures.

**Construction ledger.** At creation, each question is committed with: an id, the tag (`chart-grounded` / `interpretation-only`), for chart-grounded items the required chart fields and their engine-computed values, for interpretation-only items the machine-auditable criterion, and the scoring procedure. No item is added, removed, re-tagged, re-worded, or re-scored after the first run without a new dated entry in the Evidence Log and an owner rewrite of Section 11 of this file.

### 2.2 The Tier-1 conformance corpus

`tier1/` (see Task 13) holds 300 moments, 1900–2030, including edge cases, invoked through dual invocation paths reading the same pyswisseph / Moshier fallback.

> Shared lineage (dashaflow → pyswisseph → Moshier fallback): this is a regression/determinism gate, NOT astronomical-truth verification.

This caveat is stamped verbatim and binds every statement made about Tier-1 anywhere in this repository. Tier-1 proves that the same input produces the same pinned output, run over run, path over path. It proves nothing about whether the ephemeris is astronomically true, and it must never be cited as doing so. It is a regression and determinism gate. Nothing else.

Tier-1 status is recorded in the Determinism Log (Section 5). Tier-1 is a precondition for the plugin's computational honesty; it is not evidence for or against verification shipping, and it does not substitute for the equal-cost bar.

**Rerun policy.** Tier-1 is re-run on every engine bump, every invocation-path change, and every release. Each re-run appends to the Determinism Log; a re-run that differs from the pin fails the release. A Tier-1 drift is treated as a stop rule, not as a flake: investigate, pin, and record before any other work lands.

**What Tier-1 is allowed to conclude.** Tier-1 green means: determinism, signature stability across paths, and no silent regressions in the pinned outputs. Tier-1 green means nothing else. It is not an independent check — both paths read the same underlying ephemeris — and any sentence implying an independent verification from Tier-1 overstates this file, and is struck from whatever document it appears in.

## 3. What gets measured — and on what floor

One question only: at identical token budgets, does the plugin with tool-grounded verification beat the plugin without it on the JyotishQA seed set?

Nothing else is measured as a gate. No other metric decides whether verification ships.

**Shared inference floor.** Both arms share one inference floor: same base model, same engine version, same decoding configuration, same prompts outside the verification machinery, same token budget per turn. The delta therefore measures the verification machinery and nothing else — not the model, not the engine, not the prompting style, not the budget. An arm run on a different floor is not a measurement; it is a different experiment, and it is discarded.

**Token budget.** Both arms run at identical token budgets. An arm that exceeds its budget is disqualified for that run, not re-scored. Budgets and their actual consumption are recorded per run in the Evidence Log's notes.

## 4. The pre-commitment (equal-cost bar)

This section is the verbatim pre-commitment. It was written before any measurement was taken. It is locked at the first measurement and is not revisited afterwards.

> **Release gate (locked at first measurement).** The with-minus-without delta on the seed set must exceed the seed-set standard error at first measurement. The gate is computed before any item is scored, recorded in Section 6, and is locked — not revised, not re-tuned, not re-interpreted — once computed. **If the margin is impossible at this set size, the set is EXPANDED; the bar is never relaxed.** If the margin is possible and not cleared, verification does not ship.

### 4.1 The standard error rule

One of the following two SE rules is used, stated in the Evidence Log at first run together with the numbers actually used:

1. `SE = sqrt(p(1-p)/n)` with the conservative `p = 0.5` assumption, giving `SE = 0.5/sqrt(n)` for `n` seed items; or
2. the observed binomial SE over the item set, `SE = sqrt(p_observed(1-p_observed)/n)` with `p_observed` recorded in the Evidence Log.

Rule 1 is the default. Rule 2 is used only if Rule 1 is recorded as rejected, in writing, before the first item is scored. The choice is recorded; the formula and the substituted values are recorded; the gate value is recorded. Until the first run is recorded, the numbers live in the Evidence Log as `__PENDING__`. No number appears in this section that does not derive from the formula definition above.

Rule 1 vs Rule 2, stated plainly. Rule 1 prices in the worst case (p = 0.5) and costs a larger n for the same bar — choose it when the set is small or the effect size is unknown. Rule 2 prices in the observed split and is cheaper, but it is only admissible if `p_observed` was fixed before scoring; post-hoc p_observed is just the verdict wearing a hat. There is no third rule. A seed set measured under a rule not written here was not measured under this file.

### 4.2 The four sub-conditions

**(a) Release gate.** Delta > seed-set standard error at first measurement. Computed before any item is scored. Locked. Not revisited. Expansion of the set, never relaxation of the bar.

**(b) If the margin is impossible at this set size.** n too small to beat noise ⇒ the seed set is EXPANDED and the measurement is repeated under the expanded set. The bar is never relaxed to fit the set, the result, or the calendar. Every expansion is logged in the Evidence Log with the new n and the new locked gate value.

**(c) The failure branch (pre-committed).** If the margin is possible and not cleared — at first measurement or at any later one under this file — the plugin ships WITHOUT verification. What ships instead: sample-and-vote plus the deterministic tool-check. The verification subagents (`chart-verifier`, `doctrine-critic`), the hesitation gate, and the per-claim approval machinery do not ship. This is a pre-commitment, not a judge call made after data exists. No softening, no "nearly cleared", no "trending well", no re-run until it passes. The equal-cost tripwire in Section 7 is the same ruling stated as a stop rule: verification that cannot beat sampling at matched spend is removed, not tuned.

**(d) Pilot rule.** The first measurement is the noise floor ONLY. It is never the verdict. The first measurement exists to establish the standard error, the floor against which the gate is locked, and the feasibility of a positive margin. It does not decide ship or no-ship. The verdict is taken only under the locked gate, only when the set size makes a positive margin possible, and only with intervals reported — never as a point estimate standing alone.

### 4.3 Scoring rules (binding)

- With-minus-without comparison at identical token budgets. Any arm exceeding its budget is disqualified, not re-scored.
- Both runs are recorded with the engine version and the commit hash of this repository, in the Evidence Log. A run without both is not a measurement.
- No comparison is made against any published benchmark, any leaderboard, any prior model, or any external corpus. This project's seed set is the only measurement surface.
- Every result is reported with intervals — here, in commit messages, in changelogs, in release notes, everywhere. Point estimates alone are never reported. Trophy language is forbidden: no "beats", no "wins", no "state of the art", no deltas without intervals, never trophies.
- Selective correctness (correct-when-answered, at a stated coverage) is reported, when reported at all, as secondary, informational evidence only. It never overrides the gate, and it is never reported without its interval and its coverage figure.
- Metrics are reported with intervals beside means, including interval width, including when the interval includes zero. Reporting that flatters is a violation of this file.
- Latency is recorded per run. Anything sequential beyond a single fan-out plus one judge pass is a ship-blocker violation, and its measurement result is discarded.

### 4.4 What the gate decides — and what ships in each branch

The gate decides one thing: whether tool-grounded verification ships in the plugin. Enumerated, so there is no room for interpretation later:

- **If the gate clears** (delta > locked SE at a verdict-capable n): the plugin ships with the hesitation gate (verify-by-default on marriage / health / career), `chart-verifier` and `doctrine-critic` as gated per-turn subagents, and the grounds appendix on every reading.
- **If the gate does not clear** (margin possible, not cleared): the plugin ships WITHOUT verification. Sample-and-vote plus the deterministic tool-check ships. `chart-verifier`, `doctrine-critic`, the hesitation gate, and the per-claim approval machinery do not ship in any form — not behind a flag, not "experimental", not "opt-in". A hidden verification path is a verification ship, and a verification ship that did not clear the bar is a violation of this file.
- **What ships in neither branch**: no predictive-accuracy language, no benchmark claims, no engine endorsement, no external comparison. Both branches ship the grounds appendix (claims cite chart grounds or are tagged UNSUPPORTED); the grounds appendix is not part of the gate and is never traded away against it.
- **What “pilot” means for release notes**: first-run numbers are recorded in the Evidence Log as the noise floor. They appear in no changelog, no release notes, no README, no marketing. The locked gate value appears only in Section 6, after it is computed.

## 5. Determinism Log (Tier-1)

Record of Tier-1 runs. The first run is filled by Task 13 (execution), not by this file. `__PENDING_FIRST_RUN__` means exactly that — not yet measured, not estimated, not imagined.

| field | value |
|---|---|
| first run | filled — see run record below |
| date | 2026-11-08 |
| commit | 119d7a6 |
| engine versions | dashaflow 1.5.0 (import-time `dashaflow.__file__` → editable sibling checkout `/home/adarsh/cursorProjects/dashaflow/src/dashaflow/__init__.py`; pip dist-info 1.5.0 records the release) · swisseph 2.10.03 (bundled, Moshier fallback, no `.se1`) · Python 3.12.9 |
| moments passed / failed | 300 / 0 |
| delta vs zero-pin | 0 |

| date | commit | result | notes |
|---|---|---|---|
| 2026-11-08 | 119d7a6 | 300/300 OK (exit 0) | First full pin pass, executed on the tree that became 119d7a6 (pre-commit). Gate re-run on the amended 300-moment corpus (J2000 landmark added; one filler manual entry removed — count unchanged) → 300/300 OK, 2026-11-08, before the fix commit carrying this entry. |
| 2026-11-08 | b4857f7 | 300/300 OK (exit 0) | First full UNPINNED pass after upstream dashaflow 1.5.1 fix: PYTHONHASHSEED pin removed from `tools/tier1_check.py`; every dump subprocess ran under a fresh random hash seed. No corpus change (byte-identical moments, including the 5 historically seed-sensitive ones — fix verified, not just pinned). |

Mechanics and honesty notes (binding on any re-run):

- Dual invocation = one fresh subprocess per cast (`python tools/tier1_check.py`); no dashaflow import in the parent process. `metadata.computed_at_utc` (wall clock) stripped before comparison; `yogas` array order canonicalized. No values altered.
- Hash randomization is NOT pinned: each dump subprocess inherits a fresh random seed, so the gate itself guards against hash-seed nondeterminism anywhere in the engine. History: dashaflow 1.5.0 `yoga.py` iterated `BENEFICS = {"Jupiter", "Venus", "Mercury"}` (a set) with a `break`, so the Amala Yoga benefic named was hash-seed dependent when two or more benefics occupied the 10th. Before the upstream fix, 5/300 moments (`1906-07-01 12:00`, `1925-01-01 00:00`, `1952-01-01 00:00`, `1971-01-01 00:00`, `2016-08-31 08:30`) differed only in that selection; every other field was byte-identical. dashaflow 1.5.1 fixed it upstream by iterating `BENEFIC_ORDER` in canonical significance order; the `PYTHONHASHSEED=0` workaround pin was removed in this repo at the commit recorded below, after verifying the 5 historically seed-sensitive moments byte-identical across seeds 0/1/42. Residual risk: none known beyond what the gate now measures — any future set-ordering defect fails loudly.
- No lower-level / second-engine comparison is implemented; the subprocess dual-invocation path is the accepted gate. Both invocations read the same pyswisseph → Moshier lineage, so the shared-lineage caveat (§2.2) applies unchanged — this is a regression/determinism gate, NOT astronomical-truth verification.
- Engine provenance is logged as observed at run time (paper-tape symbolic): gate behavior is governed by the live editable sibling checkout at `/home/adarsh/cursorProjects/dashaflow/src/dashaflow`; the site-packages dist-info 1.5.0 records the release only. Corpus provenance: `evals/tier1/moments.json` — 260 generated pins + 40 hand-tagged manual landmarks; 294 unique instants; the 6 generated∩manual overlaps are intentional and hand-tagged.

Tier-1 gate criterion (locked, from the design spec): 100% deterministic pass; delta zero-vs-pin. A Tier-1 failure blocks the computational claims of the release. A Tier-1 pass changes nothing about the equal-cost bar.

## 6. Evidence Log

One row per measurement; `with` and `without` arms are recorded separately; intervals are stated in the margin column. `verdict` is informational only — it never decides anything; the gate is pre-committed and this column cannot reopen it.

| date | commit | corpus size | SE rule | arm (with/without) | margin observed | verdict (informational only) | notes |
|---|---|---|---|---|---|---|---|
| 2026-11-09 | 74efce7 | 26 | rule 1: SE = sqrt(0.5×0.5/26) = 0.098058; locked gate delta > 0.098058 | with 4/26 = 0.154 [0.0615, 0.3353]; without 5/26 = 0.192 [0.0851, 0.3788] | delta = −0.0385 [−0.3173, 0.2502]; consumed 86,170 with-arm tokens / 72,513 without-arm tokens | pilot — no verdict | opencode-go transport; arm deepseek-v4.1-flash (reasoning_effort none; without = 3×2000 @ temp 0.7, with = 2000/1000/1000/2000 @ temp 0); judge muse-spark-1.3-contributor (8000 max_tokens, mandatory reasoning); budget 6000 output tokens/item/arm; p_observed with 0.1538, without 0.1923 (recorded, rule 2 not used); items g-01…g-12, s-01…s-08, r-01…r-06; no exclusions, disqualifications, judge errors, or outputs at the 6000 cap; dashaflow 1.5.1 (Moshier fallback) |

Column definitions:

- **corpus size** — n used for this row.
- **SE rule** — rule 1 or rule 2 from Section 4.1, and the substituted values (p, n, the computed SE, the locked gate value).
- **arm** — `with` or `without`; the delta is computed across the pair, never from either arm alone.
- **margin observed** — delta in proportion, with its interval and the token budget actually consumed. Never a bare point estimate.
- **verdict (informational only)** — what the locked gate reads on this row. Recorded for the record; binding force lives in Section 4, not here.
- **notes** — expansions of the set, re-taggings, re-runs, engine bumps, model swaps; each with a date and a reason.

Rows are append-only. A row is never edited after the fact; corrections are new rows referencing the corrected row.

**What belongs in a row.** Exactly enough for a stranger to rerun the measurement: engine version, commit, model identifier, decoding configuration, token budget per arm, and the item ids scored in each arm. What does not belong in a row: commentary, justification, narrative about what the delta "suggests". The interval speaks; the row records.

**Anonymization.** No row records personal data about any rater, reader, or user. The log records measurements, not people.

**Anatomy of a first-measurement row (template, filled by the run — never invented):**

```text
date            = __PENDING__
commit          = __PENDING__
corpus size n   = __PENDING__
SE rule         = rule 1  (default; rule 2 only if rule 1 rejected in writing before scoring)
SE value        = sqrt(p(1-p)/n) with p = 0.5  →  __PENDING__
locked gate     = __PENDING__   (delta required to beat)
p_observed      = __PENDING__   (recorded, not used unless rule 2 was pre-approved)
arm(with)       = __PENDING__   (engine version + commit + items scored + interval)
arm(without)    = __PENDING__   (engine version + commit + items scored + interval)
margin observed = __PENDING__   (with minus without, with interval)
verdict         = __PENDING__   (informational only)
notes           = __PENDING__   (budget consumed, anomalies, item ids)
```

Any cell left `__PENDING__` after a claimed measurement means the measurement did not happen. There is no partial honesty in this table.

**How an expansion of the set is logged.** One row per expansion, with: the date; the n before and after; the re-derived locked gate value; the reason (margin impossible at the prior n); and a pointer to the commits adding the new items. Items added by expansion carry the same construction rule and tagging discipline as the original set — expansion is not a backdoor for re-weighting the corpus toward a desired result.

**How a re-run is logged.** Re-runs of an unchanged configuration are new rows that reference the original row. Repeated re-runs until a favorable result appears are a violation of this file, full stop — the pilot rule applies to the first measurement, and the locked gate applies to every measurement after it.

## 7. Tripwires (binding; restated from the research report, Section 8, and pre-registered)

Each of these is a stop rule. When a tripwire fires, the pre-registered response fires with it. No tripwire is "reviewed" into inaction. The signal for each is observable in the Evidence Log or in the calibration record; the response is not discretionary.

1. **equal-cost failure.** Signal: the locked gate is not cleared at a verdict-capable n. Response: verification that cannot beat sampling at matched spend is removed, not tuned. No re-tuning, no prompt tweak and re-measure until it passes.
2. **interpretation-concentration of errors.** Signal: itemized failures are concentrated in the weighing/interpretation layer while the calculable claims pass. Response: the verifier layer is re-scoped to its calculable core or dropped; interpretation claims are not verifier-blocked.
3. **calibration failure.** Signal: hedging language graded by the judge fails on astrological prose (agreement with humans does not survive swap-and-obfuscation controls). Response: numeric thresholds replace judge hedging; the judge stops grading prose hedging and grades numbers.
4. **overcorrection sag.** Signal/response, in the report's wording: "rejecting over a third of tool-supported user corrections (acceptance <65%) loosens the agreement penalty" — with 65% marked directional/TBD-fit by the report, not committed as law here; this file does NOT commit a number. Acceptance of tool-supported user corrections falls below the TBD-fit floor — loosen the selection-time agreement penalty proportionally to the sag. If the floor is unmeasurable or the sag is severe, freeze interpretation-promotion criteria and rescope the verifier to high-stakes slices. [ADDED BY THIS FILE — an explicit addition of the pre-committed gate; not in the report's precedent wording; binding only after owner ratification at first measurement; until ratified, the only binding response is the report-faithful loosening.] No hard number ships in this file — deliberately.
5. **near-tie saturation.** Signal: abstention rates on near-tie judgments approach saturation. Response: verification is compressed to the high-stakes slice only (marriage / health / career). The grounds appendix is never removed.
6. **security or context regression.** Signal: script-bundling skills, egressing hooks, over-budget idle context, or replicated vulnerability findings appear in the bundle or its footprint estimator. Response: cut-first review before any feature work; the offending component is cut or fixed before anything new is added.

If the agreement study returns chance, if the registry never clears chance, or if verification never beats sampling at equal cost, this file has already said what gets cut, what gets capped, and what never ships. That is the point of writing it first.

**Order of operations when several tripwires fire at once.** Security/context regression first — the bundle is cut to safe before it is measured for anything else. Equal-cost second — the verification question is settled and, if it fails, nothing downstream of verification ships. Calibration third — thresholds, not hedging. Overcorrection fourth — the agreement penalty is adjusted per measurement or frozen. Near-tie fifth — compression to the high-stakes slice. Interpretation-concentration sixth — the verifier is re-scoped or dropped. No ordering discretion is held by the maintainer; this order is the order.

## 8. Reading this file at release time

Before any release carrying this plugin is tagged, the maintainer walks this checklist in order. A failed box stops the release; it is not a checkbox to be waived.

1. Tier-1 is green on the release commit: 100% deterministic pass, delta zero-vs-pin, provenance complete (engine version + commit) in the Determinism Log.
2. The Evidence Log contains rows for the current engine and commit. A release without current rows is not measured, and an unmeasured release does not ship.
3. The locked gate value recorded at first measurement matches the value in force in Section 4. If it does not match, this file was changed without an owner rewrite — stop, revert the change, re-derive from this file.
4. The verdict column on the relevant rows is read as informational only, and the release proceeds or halts exactly as Section 4 dictates — not as the verdict column suggests, not as the trend suggests.
5. No release note, changelog, README, or tag annotation cites a point estimate. Intervals only. No trophy language. No comparison to any external benchmark.
6. No SKILL.md, agent definition, hook, or manifest references this file's outcomes as a selling point. The plugin bundle contains no copy of this file.
7. If the base model, quantization, or engine changed since the last measurement, Section 10 applies before anything else in this checklist: re-measure from scratch, re-validate the corpus from scratch.
8. No badge, shield, or README build-status link implies eval performance, and no release tag is annotated with a delta. Release tags carry version, date, and nothing else.
9. If a tripwire fired during this release cycle, the release notes name the tripwire and state the pre-registered response that was applied. A tripwire fired and not named is a hidden decision, and a hidden decision is a violation of this file.

## 9. What this file is NOT

- It is not a product claim. No feature, performance, or benefit of the plugin is asserted by it, before or after measurement.
- It is not a benchmark publication. Nothing in it is a leaderboard entry, a comparison table, or a paper result. It is released as repository doctrine and nowhere else.
- It is not an endorsement of any engine. dashaflow, pyswisseph, and the Moshier fallback are named only as the current lineage of the Tier-1 corpus. Selection of the engine is an engineering decision made elsewhere and justified elsewhere; this file neither blesses nor censures it.
- It carries no predictive-accuracy language whatsoever. No outcome recorded here licenses the phrase "predictive accuracy", "predicts", "forecasts", or any equivalent, in this file, in the repo, or in release materials. Correspondence claims are out of scope until the Level-2 calibration tier and the prospective registry exist, and even then they are bounded by those instruments' intervals.
- It is not a ceiling on honesty and not a floor under marketing. If marketing ever needs a benchmark, one is built AFTER Level-2 (the calibrated, isotonic-mapped tier) exists and never before. There is no version of this file that authorizes a pre-Level-2 benchmark claim.
- It is not a second document. It is the only such document in this repository. There is no companion pre-commitment, no "eval summary", no README section restating these bars with different numbers. If a conflict appears between this file and any other document, this file wins.
- It is not the agreement study. The jyotishi panel, blind endorsement rates, and the verifier-reliability statistic are separate instruments with their own acceptance criteria. This file gates the ship of verification; it does not certify correspondence, and it does not speak for the panel.
- It is not the calibration artifact. The isotonic map, selective-correctness curves, Brier error, and abstention thresholds are Level-2 outputs. This file does not contain them, and no Level-2 claim is made from anything recorded here.

## 10. Model-substitution rule

Every threshold in this plugin is fit to a model family and a quantization level. A base-model change re-opens phase acceptance: the equal-cost bar is re-measured from scratch, the corpus is re-validated from scratch, and the calibration floor is re-checked. A quantization change inside the same family re-opens the same doors. Engine swaps re-validate the corpus from scratch, full stop. No threshold, gate, cap, or abstention point survives a base-model change, a quantization change, or an engine swap by continuity of assumption; each is re-derived from this file.

**What re-validation from scratch means, concretely.** (1) Tier-1 re-run and delta checked against the pin — any failure halts the substitution. (2) Seed set re-tagged and re-verified: every `chart-grounded` item's engine values recomputed against the new engine/model context. (3) The first measurement under the new configuration is a new pilot: it measures the noise floor only, under Section 4.2(d), and the locked gate value is re-derived and recorded before any new verdict is taken. (4) Calibration floor re-checked — abstention points and thresholds refit, never inherited.

Every recalibration re-derives from this file: SE rule, gate value, locked bar, failure branch, pilot rule, tripwires. A recalibration that does not touch this file was not a recalibration.

## 11. Changes to this file

Only an explicit owner rewrite changes this file. Every change is a new Evidence Log row with date, commit, reason, and the owner's name — appended, never edited in. Data never changes it. Results never change it. Time never changes it. Pressure, compromise, and promising trends never change it.

**The owner-rewrite procedure, in order.** (1) The owner writes the requested change as a diff against this file, with the reason stated in the diff message. (2) The diff is committed with an Evidence Log row naming the reason and the owner. (3) Any downstream document whose correctness depended on the changed clause is updated in the same commit — a rewrite that leaves a contradiction behind is not a rewrite. (4) If the change relaxes any gate in Section 4, the relaxed gate does not apply to measurements already taken; it applies from the next first measurement onward, treated as a new pilot.

No silence constitutes a change. No instruction in any other document overrides this section. No measurement, however decisive, edits a clause here by implication.

The pre-commitment holds because it was written before the data existed. If it ever stops holding, the fault is here — in the keeping of this file — and not in the numbers it will print.

This file is the ground-truth plugin's ground truth about itself: an engineered artifact that tests whether honesty is worth its token cost, measured before it is sold, and believed after it passes.
