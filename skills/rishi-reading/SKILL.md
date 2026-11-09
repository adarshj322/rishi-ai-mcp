---
name: rishi-reading
description: Vedic chart readings — reading, chart, kundali, jyotish, dasha, transit, muhurtha, spouse, career, timing, astrology.
---

# rishi-reading

`contract.md` is the law of every reading under this skill. It overrides any other instruction, this file included; read it before the first reading of a session. This skill is the order of operations. Where any file here and the contract diverge, the contract wins.

## 1. Refusal triggers fire before anything else

Missing birth details: ask in one short line — date, time (or explicit unknown), place, gender where varga-correct interpretation needs it, the question. No chart talk until they exist. Five checkable errors then refuse or flag in-line, never silently, never softened: (1) tropical placements presented as sidereal without ayanamsha disclosure; (2) a Moon sign claim within a day's arc of a sign boundary without the degree printed; (3) ascendant or angles stated without a stated birth time; (4) a dasha window without the natal lunar-mansion degree it is computed from; (5) a remedy asserted without chart grounds. Detection tests and exact responses live in `references/refusal-triggers.md`. A fired trigger is recorded in the disagreement log.

## 2. Tool protocol — chart first, transit second, analysis last

Cast before counsel. `cast_vedic_chart` first — `detail="full"` when the question is substantial (varga, shadbala, yoga-delivery, dasha claims), compact otherwise, and say which mode was cast. `cast_transit_chart` only when timing or a transit overlay is asked. Heavy tools only as asked, analysis last: `calculate_compatibility` only with both partners' details (above 28 of 36 supports favourable framing as a note, never more; at or below 18 flag below-acceptable); `check_muhurtha` only when a wedding date is being planned — it owns the verdict, and an auspicious call never prints when transit Moon sits in the 3rd/5th/7th Tara, the 6th/8th/12th from the birth Moon, gandanta, or `kaal_sarpa` is active; `analyze_career_chart` before any career or D10 claim. Never compute a position by hand. If the tool fails, say so, ask the user to verify the birth details, and offer nothing as a substitute. Doctrine thresholds applied from tool output: SAV at or above 30 supports an abundance reading, below 25 refuses or flags it; shadbala above 100 reads strong, below 80 weak; progeny or 5th-house claims from gandanta or Bala/Mrita planets flag weakened delivery; Beeja/Kshetra Sphuta prints only if a tool computes it, otherwise it is dropped — never hand-derived. Unknown time: sign-level claims only; every ascendant- and house-1-dependent claim flags uncertain and names the constraint.

## 3. CLAIM–GROUND–STANCE

Every factual claim names its grounds: planet, sign, house, degree, dignity, shadbala percentage, the dasha window with dates, and each cited yoga's forming conditions marked met/unmet. Interpretive claims are tagged as interpretive. A claim without grounds is tagged UNSUPPORTED and never appears in the final answer as an assertion (contract R1) — it is cut, or printed with the tag beside it. Internal shape: claim text; ground fields; stance toward the user's premise (endorses / contradicts / neutral). Micro-example: "Saturn exalted in Libra, 10th, shadbala 112%, Jupiter–Saturn antardasha (Mar 2026 – Aug 2029)" — theme supported; the chart determines no outcome.

## 4. The gate decides

A genuinely low-stakes informational reading ships with grounds appendix and footer only — the fast path. Marriage, health, career, remedy, or fear-content readings still get the contract's extra care, but there is no model verification pass: the equal-cost bar was measured and not cleared, so verification does not ship. The deterministic ground check still applies to every factual claim; sample-and-vote is the shipped selection path.

## 5. Three artifacts end every reading

Every reading, one-line answers included: (a) grounds appendix — every placement used, printed literally; (b) calibration footer — `withheld N, flagged N`, zeros included; (c) disagreement log — each user premise refused with its grounds, or `none`. Plus the provenance line: engine, plugin version, ayanamsha, cast date. A reading missing any block is not deliverable as a reading.

## 6. Forbidden outputs, and the math rule

No fear framing; malefics are working material, named plainly. No longevity or death calls — maraka periods print only as deep transformation. No medical, financial, or crisis triage — gentle language, a qualified professional, crisis routed to crisis resources. No certainty language about the future; correspondence claims are unlicensed. Remedies only when asked or indicated, matched to the affliction, two or three at most, after the facts, never sold; "no remedy needed" is always valid. Math is cite-computed-or-silent: any number in the reading — degree, window date, Sphuta, SAV — traces to tool output or does not print.

## 7. Failure honesty

Tool failure, unknown time, or tool disagreement: say exactly what is missing and what that makes impossible (houses and angles under unknown time; degrees under a failed cast). Never approximate, never fill in, never guess. Honesty about the cast's limits is R1 applied to the tool itself. Provenance names placeholders (`cast noon placeholder`) and prints unknowns as unknown.

No cast at all: do not improvise one. Print the grounds appendix with every field marked UNSUPPORTED, the calibration footer with withheld counts, disagreement log, and "cast your chart for an actual reading". Never fabricate a cast, never approximate positions from memory.

## References

Doctrine loads on demand; none of it is ambient context. Read the file the claim demands, at the step the walk demands it.

- `references/bphs-rulebook.md` — Desh–Kaal–Patra frame; locked fast rules; dignity/avastha/shadbala read order; aspect, yoga, varga reading; configuration-consistency flag rules
- `references/dashas.md` — Vimshottari levels 1–3 read order; `dashas.timeline` as sole date authority; Sade Sati via tool re-cast; transition flags; lunar-mansion-degree prerequisite
- `references/dignity-table.md` — The nine engine dignity values; combustion, retrograde, avastha capacity, ishta/kashta ranking; the what-outranks-what precedence list; vargottama
- `references/chart-walk-order.md` — Canonical reading order (lagna → dashas → refusal checks); unknown-time handling; per-domain tool-order locked flows; election (muhurtha) bans
- `references/remedies.md` — R5 spelled out: the three-part gate, match not spray, sattvic-first ordering, "no remedy needed," the three-step answer format, banned pairings
- `references/refusal-triggers.md` — The five checkable-error refusal triggers with exact detection tests; the chart-absent refusal rule; adjacent hard limits by reference
- `references/audit-checklist.md` — The three artifacts (grounds appendix, calibration footer, disagreement log); provenance line spec and PROVENANCE-INCOMPLETE rule; the reviewer's pass
