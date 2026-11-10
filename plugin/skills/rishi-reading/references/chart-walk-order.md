# Chart walk — canonical order of a reading

This file is the order of operations. Steps are sequential; a step is skipped only by refusal (a failed gate), never by preference. Refusal triggers live in refusal-triggers.md; the gates live in the contract.

## The walk (natal chart)

1. **Lagna.** Sign, nakshatra, degree, time_sensitivity verdict. If verdict is borderline or fragile, ascendant- and house-1-dependent claims are flagged uncertain and birth-time verification is advised in-line (full-reading keep-rule). No later step proceeds without this line.
2. **Lagna lord.** Sign, house, dignity, `shadbala.percentage`, avastha, combustion, retrograde. The lagna lord's read is the constitutional baseline; every later claim sits on or under it.
3. **Planets in shadbala order (descending).** For each: sign, house, dignity, degree, `shadbala.percentage`, ishta/kashta, avastha, combust/retrograde, vargottama status, and the varga placements the question uses. Weakest-first is banned; read strength descending so the strong planets frame the themes.
4. **Yogas.** From the tool's `yogas` array only. Each cited yoga lists forming conditions with met/unmet marks. Yoga delivery is gated by forming-planet strength (bphs-rulebook.md). No hand detection.
5. **House-lord claims.** Each claim cites fields (R1): lord, sign, house (Rashi; both if chalit split), dignity, shadbala, aspects. Lordship from Rashi; delivery from Chalit when shifted.
6. **Dashas.** Prerequisite: lunar-mansion degree in grounds (trigger 4). Then maha → antar → pratyantar via `dashas.timeline`; dasha-lords read as in dashas.md. A timing claim without the degree refuses.
7. **Transits.** `cast_transit_chart` with the query date. Transit `house_from_lagna`, `house_from_moon`, `sav_points` (28+ easy, below 25 struggle), `sade_sati`, `rahu_ketu_axis`. Transits overlay; they never restate the natal picture as if new.
8. **Refusal checks.** Run refusal-triggers.md top to bottom before the reading prints. Any trigger fires: refuse or flag in-line per that file. No trigger is conditioned on user mood or patience.

The output blocks then print in contract order: grounding → reading → remedies (gated; absent by default) → grounds appendix → calibration footer → disagreement log → provenance.

## Unknown-time handling

- Unknown or unknown-ish time ("morning," "after lunch," ±90 minutes): houses, ascendant, angles, chalit shifts, house-lord delivery, and Sade Sati from the ascendant are unavailable. Not approximated — unavailable.
- The reading restricts itself to sign-level claims: sign lords, sign aspects, wealth and yoga signatures that fire at sign level. Everything house-anchored is refused in-line.
- A noon placeholder cast is attempted only if flagged as a placeholder, in-line and in provenance (`cast noon placeholder`); it is never presented as degree-true.
- The reading ends with the standard blocks; provenance names the placeholder. Honesty about the cast's limits is R1 applied to the tool itself.

## Per-domain fetch orders (locked tools order)

Each flow names its tool order. Interpretation before its fetch order completes is a defect, whatever its quality.

**Career.** `cast_vedic_chart(detail="full")` + `cast_transit_chart` + `analyze_career_chart` before any career or D10 interpretation. Amatyakaraka read from `jaimini_karakas` (never re-derived). 10th lord or Amatyakaraka in Bala/Mrita avastha: no confident "full career capacity" claim — flagged diminished capacity. `shadbala.ishta_kashta_phala` of the 10th lord confirms or denies gate-passing. D10 cross-reference for domain-level claims. Career-giving themes cite fields; no offer, date, or promotion is claimable (correspondence ban, R6).

**Children.** `cast_vedic_chart` + `cast_transit_chart`, then 5th-house, avastha, gandanta checks; timing last. 5th lord or Jupiter in `gandanta`: progeny claims print with a weakening flag; no promise wording. 5th lord shifting to 4th/6th in `bhava_chalit`: progeny language flags weakened/delayed wording. Beeja/Kshetra Sphuta: only if a deterministic tool path computes it; then cite the tool's values; otherwise never compute by hand.

**Education.** `cast_vedic_chart` + `cast_transit_chart`, then D24 (Siddhamsha) cross-reference for exam and higher-education claims. Mercury, Jupiter, or 4th/5th lords in Bala/Mrita: diminished academic delivery flagged regardless of dignity. Chalit shift of education lords: the learning-arena claim shifts with the chalit house; Rashi retains lordship.

**Finance.** `cast_vedic_chart` + `cast_transit_chart`; `yogas` array read before any Dhana/Lakshmi claim. SAV (`sarvashtakavarga`) by wealth-house sign: at or above 30 an abundance claim is supported; below 25 it is refused or flagged. Dhana Yoga (1/2/5/9/11 lords in mutual connection) is confirmed by the tool's yoga array plus per-lord fields; the label alone never prints unsupported. Lakshmi Yoga: Venus strong and 9th lord in Kendra/Trikona, per tool fields. Ishta/kashta of 2nd/11th lords cited. Wealth claims never print with return projections (R4: no financial advice).

**Health.** `cast_vedic_chart` + `cast_transit_chart`; D30 (Trimshamsha) cross-reference after base fetch. Affliction triad (`shadbala.percentage` under 80, `is_combust`, `debilitated`) flags the governed systems; a flag is not a diagnosis. No medical statement; professional deferral per AGENTS.md guardrails and contract R4. Maraka framing only as deep transformation.

**Marriage.** `cast_vedic_chart` + `cast_transit_chart` for the native. `calculate_compatibility` only if BOTH partners' birth details are provided; if not, compatibility is skipped explicitly. Thresholds (as printed by the tool, 36-point scale): at or below 18 flag below-acceptable; above 28 supports favourable framing; between, print mixed. Kuja Dosha mismatch flagged with both charts' fields. D9 (Navamsha) read as the D1-vs-D9 contrast; malefics in the 2nd from Upapada flag continuity wording; Darakaraka read only from `jaimini_karakas`. Compatibility is dual-chart data only; it is never fabricated from one chart. Professional and crisis deferral per AGENTS.md guardrails and contract R4.

**Spiritual.** `cast_vedic_chart` + `cast_transit_chart`; read `karakamsha` directly (Karakamsha sign, its lord, planets in it). Ishta Devata = the planet ruling the sign 12th from the Karakamsha lord; cite the derivation fields. "Natural dharmic alignment" requires 9th lord `shadbala.percentage` above 100; at or below 100 the claim is flagged unsupported. D60 cross-reference of Atmakaraka/Jupiter/Ketu cited as fields, never as a verdict.

**Full reading.** Steps 1–8 above in order; `time_sensitivity` gate before anything ascendant-dependent; no output before the fetch completes.

## Electional (muhurtha) checks

`check_muhurtha` first; the tool owns verdict, score, `panchang_suddhi`. Prose defers to the tool verdict; optimization-by-anecdote is banned. Natal cast and transit are fetched only if birth details are provided, then Tarabala and Chandrabala are checked from the tool's Moon data.

Hard bans — each prints as a ban with its field cited; the reading never calls the election auspicious when any holds:

- Tarabala: transit Moon in the 3rd (Vipat), 5th (Pratyak), or 7th (Vadha) Tara from the birth Moon — banned.
- Chandrabala: transit Moon in the 6th, 8th, or 12th from the birth Moon — banned.
- Gandanta Moon: transit Moon in `gandanta` (within 3°20′ of the Cancer→Leo, Scorpio→Sagittarius, Pisces→Aries junctions) — banned.
- `kaal_sarpa.active` at the elected time — flagged; never "auspicious beginnings."
- Malefics in the lagna or 8th at the proposed time — flagged.

If the elected time fails, alternatives are offered with reasoning; pressure framing and fear pairing are banned (R4, R5). The tool verdict is the verdict; the reading interprets it, never outranks it.

## After the walk

The reading prints only what survived Steps 1–8. Anything below threshold was withheld and counted (R2). The disagreement log records every refused premise. Provenance signs the whole thing (R6). Nothing after the walk is decorative.
