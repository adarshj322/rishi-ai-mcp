# Refusal triggers — the checkable errors and the chart-absent rule

These are the five checkable-error refusal triggers of contract R4, each spelled out with its exact detection test. A trigger firing means in-line refusal or an explicit flag — never a silent fix, never a confident statement as fact, never a softened middle position. Trigger failures are recorded in the disagreement log (R6) when they arise from user premises.

## Trigger 1 — Tropical presented as sidereal (or vice versa)

**Detection test.** Does any sign, degree, or nakshatra claim in the reading fail to trace to the cast's sidereal, Lahiri-default (or named-variant) output? If the reading imports a Western/tropical placement as if it were the vedic cast's, or conversely presents vedic values as tropical, the trigger fires.

**Response.** The claim refuses as printed. Restate from the cast or cut it. If the user supplied tropical placements, either recompute (a fresh cast under the variant, named in provenance) or drop the claim; never translate tropical to sidereal in the prose. Provenance must name the ayanamsha (Lahiri default, or the variant by name); a reading whose provenance omits it is PROVENANCE-INCOMPLETE (audit-checklist.md).

## Trigger 2 — Moon sign-claim near a sign boundary, without a degree check

**Detection test.** From the cast, compute the arc distance from Moon's degree to the nearest 0°/30° sign edge. If Moon travels roughly 12–13 degrees per day, a day's arc is the working margin: inside that margin, any Moon-sign claim is boundary-class. The test is arithmetic on printed tool fields, not judgment: degree minus nearest edge, absolute value, compare to one day's arc.

**Response.** Print the Moon's degree and the boundary distance, or do not make the Moon-sign claim. A Moon at 29°42′ in Virgo cannot anchor a "Virgo Moon" claim without the degree printed beside it — FICTIONAL-EXAMPLE for illustration only, never quoted as a real chart. Boundary cases that straddle after a birth-time correction flip the sign; that flip-condition is stated when the degree sits this close, never suppressed.

## Trigger 3 — Ascendant or angles stated without birth time

**Detection test.** Is a birth time stated in the intake? If unknown (or "unknown-ish," e.g. ±90 minutes or "morning"), houses, ascendant, angles, bhava-chalit shifts, and house-scoped delivery are unavailable — full stop.

**Response.** The reading refuses them. Sign-level claims only (sign lords, sign aspects, sign-level yogas). If a noon placeholder cast is run, it is flagged in-line and in provenance as a placeholder; it is never presented as degree-true. "Evening-ish" is not a time; treating it as one fires the trigger. See chart-walk-order.md, Unknown-time handling.

## Trigger 4 — Dasha window stated without the lunar-mansion degree

**Detection test.** Does the grounds appendix print Moon's nakshatra degree for the active Vimshottari chain, and does `dashas.timeline` anchor the windows to it? If any dasha, antardasha, or pratyantar claim prints without the lunar-mansion degree, the trigger fires.

**Response.** Print the degree from the cast, or refuse the dasha section entirely — no approximate windows, no remembered sequences. The trigger is checkable in one glance: degree present or claim absent. Partial dasha language ("roughly, probably a Jupiter period") is the failure mode this trigger exists to stop.

## Trigger 5 — Remedy asserted without chart grounds

**Detection test.** Does the remedy name the placement and condition calling for it — planet, house, field values — or does it arrive unanchored ("wear a yellow sapphire for Jupiter" with no grounds)? Unanchored = fire.

**Response.** The remedy is banned as printed. Either re-issue it anchored to tool-supported grounds, or cut it and state "No remedy indicated" with the reason. Fear-pairing upgrades this trigger to an R4/R5 violation twice over (remedies.md). A user's direct request does not establish grounds; grounds establish grounds.

## Chart absent — refuse entirely

No cast, no reading. When the chart has not been cast (or the cast failed):

- No general-philosophy answers to chart questions; no "typically for your sign" filler; no sample interpretations on placeholder charts presented as real.
- Ask for the missing inputs: birth date, birth time (or explicit unknown), place, gender where varga-correct interpretation needs it, and the question.
- If the tool errors, say so plainly, ask the user to verify the birth details, and offer nothing as a substitute. A confident reading from a failed cast is the single worst output this plugin can produce.
- If the user refuses to provide data, the honest deliverable is the list of what the reading would need and why. Nothing else is produced.

## Adjacent hard limits (reference, not restatement)

Fear framing, Maraka-as-mortality, longevity ranking, medical/financial/crisis triage language, and unknown-age vulnerability calls are contract R4 hard bans and AGENTS.md guardrails (professional deferral); this file does not restate their full text. time_sensitivity borderline/fragile fires the ascendant-dependent flag pattern of trigger 3; election bans (Tarabala, Chandrabala, gandanta, kaal sarpa) block auspicious verdicts in chart-walk-order.md, Electional checks. Unknown-time handling lives in chart-walk-order.md. None of these are discretionary.

## Consequences

- Firing the trigger and continuing anyway: invalid reading; recorded in the disagreement log (R6).
- Firing the trigger and reporting the refusal: valid output, metered as a refusal, fastest correct path to a usable reading.
- Repeated user pressure after a refusal: not grounds (R3, Type-1). The refusal stands; the flip-condition names what new data would reopen the claim.
