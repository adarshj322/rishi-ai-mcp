# Audit checklist — the three artifacts, provenance, and the reviewer's pass

Contract R6 signs every reading. This file spells out the three artifacts, the provenance line, and the pass a checker (human, judge model, or lint script) runs before a reading is delivered. Missing, malformed, or reassuring-looking artifacts do not weaken a reading; they invalidate it.

## Artifact 1 — grounds appendix (R6a)

Every reading prints it, including one-line fast-path answers. Contents, minimum set:

- Cast inputs: date of birth, time (or "unknown — houses and angles off"), place with coordinates and timezone; ayanamsha.
- Lagna (sign and nakshatra) and lagna lord (sign, house, dignity, shadbala).
- Every planet used: sign, house, degree, dignity, `shadbala.percentage` where claimed, combustion/retrograde where claimed, vargottama where claimed.
- Every yoga cited: forming conditions listed with met/unmet per condition.
- Active dasha and antardasha with window dates from `dashas.timeline`.
- Varga placements only where a claim leans on them; fields not consulted do not appear; fields consulted always do.

The appendix is checkable field by field. A claim in the body without its appendix fields is an audit finding, not a style issue.

## Artifact 2 — calibration footer (R6b)

One line: `withheld N, flagged N`. Integers at or above zero, both printed, zeros included.

- Withheld: claims below threshold, not printed in the body (counted, not vanished).
- Flagged: claims printed but marked unverified or unsupported.
- Any negative, fractional, or missing count: defect.
- Reading rule: zero withheld on a contested chart (boundary Moon, contested yoga, unsettled dasha) is a finding that the gate did not fire; the audit asks why. A persistently zero footer across every session is the failure mode that matters, not a flex.

## Artifact 3 — disagreement log (R6c)

Never an empty string. It prints either:

- `none` — the reading refused or revised no user premise; or
- One line per refused/revised premise, in the form `premise → grounds (fields)`.

"None" is a claim about the turn, not a courtesy filler; it is legal only when no premise was refused or revised. A blank log line, a dash, a shrug emoji, or a trailing space is a defect. The log is never compressed below one line (stop conditions, R6/5).

## Provenance line (R6d)

Required elements, all printed:

- Engine name and version; commit hash of the tool build.
- Plugin version.
- Ayanamsha — `Lahiri (default)` or the variant named explicitly; never omitted, never "ayanamsha per defaults."
- Cast date. Unknown-time placeholder named as such (`cast noon placeholder`).
- One reading, one provenance. In-session provenance drift (different ayanamsha, engine, or commit across readings without disclosure) is a self-contradiction; the drift itself is logged in the disagreement log.

Any element honestly unknown is printed as unknown — never approximated, never omitted. Missing commit hash, missing version, or unknown engine means **PROVENANCE-INCOMPLETE**: the reading is treated as unverifiable and must not be delivered as a valid reading. It is never repaired by estimate.

## Reviewer's pass — ordered checks

Run top to bottom; each failure points at the artifact that catches it.

1. **Skeleton present.** Grounding, reading, remedies (if gated; omission legal), grounds appendix, calibration footer, disagreement log, provenance. Missing block: reading invalid.
2. **Appendix coverage.** Every body claim traces to printed fields; every printed field either supports a claim or is listed under fields-consulted. Mismatch: flag; claim corrected or withheld.
3. **Footer sanity.** Integers at or above zero, non-missing. Zero on a boundary-Moon or contested-yoga chart: gate finding, route for deeper review.
4. **Log sanity.** Non-empty-string; `none` with no refused premises, or entries pairing premises to fields. Empty: reject.
5. **Provenance complete** or marked PROVENANCE-INCOMPLETE and held back.
6. **Trigger sweep.** The five triggers of refusal-triggers.md: tropical-as-sidereal; boundary Moon degree printed; unknown time kept out of house claims; dasha degree present; remedy grounds named.
7. **Footer-log coherence.** Log shows refused premises; footer shows corresponding withheld counts above zero. Zero footer beside a non-empty refused log is suspicious in the same way a stopped clock is suspicious: both look right once.
8. **Word ban.** No banned vocabulary anywhere in the reading (the plugin's banned list of outcome-and-determinism words; see contract R6 and this repository's constraints). Presence: the section is rewritten.
9. **Correspondence silence.** No named window as an outcome, no "you will," no prophecy. The correspondence registry does not exist; any such sentence is a violation, not a style flaw.
10. **Remedies audit.** If present: only after facts, at most three, matched to afflictions, means-checked, framed once, no outcome, no fear pairing, no purchase language without explicit user ask.
11. **Fast-path completeness.** A short reading is never a thin reading: it still prints skeleton blocks 1–10 in order.

## Failure handling

- **PROVENANCE-INCOMPLETE**: withhold delivery; missing element is printed as missing; never reconstructed.
- **Appendix mismatch**: claim corrected to grounds or tagged UNSUPPORTED; footer count increments.
- **Banned vocabulary**: the offending sentence is rewritten; if rewriting is impossible without inventing grounds, the sentence is cut.
- **Footer/log incoherence**: audit finding recorded; the reading routes to reviewer judgment (a human, or a separate model for an advisory read where available; no model judge ships, and same-model second passes are not verification).

## The audit's one-line summary

Counts at or above zero, fields or no claim, grounds or no remedy, signature or no delivery.
