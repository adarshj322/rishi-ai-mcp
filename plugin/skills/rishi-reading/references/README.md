# References manifest — rishi-reading doctrine

Authority order, binding on this whole tree: **the ephemeris is the only calculation authority; the LLM is an interpreter of tool output, never a calculator.** `skills/rishi-reading/contract.md` is canonical for behaviour; these files elaborate it — rulebook interpretation, tables, walk order, remedies, refusals, audit. Where any of these files and the contract appear to diverge, the contract wins and the file here is defective; report it, do not improvise a reconciliation. `AGENTS.md` carries host guardrails (medical, financial, crisis deferral); this tree references it and never duplicates it.

## Manifest

| File | Purpose (one line) | Load when |
|---|---|---|
| `bphs-rulebook.md` | Desh–Kaal–Patra frame; locked fast rules; dignity/avastha/shadbala read order; aspect, yoga, varga reading; configuration-consistency flag rules | Always — before the first interpretive claim of any reading |
| `dashas.md` | Vimshottari levels 1–3 read order; `dashas.timeline` as sole date authority; Sade Sati via tool re-cast; transition flags; lunar-mansion-degree prerequisite | Any dasha, antardasha, pratyantar, timing, or Sade Sati claim |
| `dignity-table.md` | The nine engine dignity values; combustion, retrograde, avastha capacity, ishta/kashta ranking; the what-outranks-what precedence list; vargottama | Any claim leaning on planetary strength |
| `chart-walk-order.md` | Canonical reading order (lagna → dashas → refusal checks); unknown-time handling; per-domain tool-order locked flows; election (muhurtha) bans | Start of every reading; re-check at each new domain question |
| `remedies.md` | R5 spelled out: the three-part gate, match not spray, sattvic-first ordering, "no remedy needed," the three-step answer format, banned pairings | When the user asks for remedies, or the gate passes |
| `refusal-triggers.md` | The five checkable-error refusal triggers with exact detection tests; the chart-absent refusal rule; adjacent hard limits by reference | Before the reading prints; whenever a boundary case appears |
| `audit-checklist.md` | The three artifacts (grounds appendix, calibration footer, disagreement log); provenance line spec and PROVENANCE-INCOMPLETE rule; the reviewer's pass | Before delivery; before any sign-off |

## Reading order suggestion

`chart-walk-order.md` → `bphs-rulebook.md` → `dignity-table.md` and `dashas.md` as the claims demand → `remedies.md` only if gated → `refusal-triggers.md` then `audit-checklist.md` before the reading ships.

## Notation and conventions here

- Field names in backticks are printed exactly as the five-tool server prints them; a missing field is a flag, never an invitation to compute it.
- "Flag" = printed, marked weak or unsupported. "Refuse" = claim withheld or section declined, with the failed check named. "Defect" = audit finding against the reading.
- Example values are marked FICTIONAL-EXAMPLE and are never real chart data.
- Numbers printed here are doctrine thresholds (e.g. SAV cut-offs, dignity ordering), not measurements of this plugin's accuracy; correspondence-layer claims remain unlicensed here as everywhere in the plugin (contract R6).

## CI footprint note

This file is the manifest CI reads. Every other file in this directory loads on demand during a reading (progressive disclosure); none of them is always-loaded context. `README.md` itself stays one line away from every other file so CI can resolve the bundle without opening doctrine.

## Amendment rule

These files amend by git with auditable diffs, exactly like the contract. A doctrine line loosens only on new measurement captured in the contract's provenance or an ingested decision record — never by convenience, never silently.
