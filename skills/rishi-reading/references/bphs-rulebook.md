# BPHS rulebook — the interpretive frame

This file is the operating rulebook for reading a cast. It elaborates the contract (`../contract.md`) and never contradicts it. Every sentence binds the reading; none is advisory. The ephemeris is the only calculation authority; the model is an interpreter of tool output, never a calculator.

## Desh–Kaal–Patra — the three frames

Every claim is made inside exactly one of three frames. Cross-frame import is a defect.

- **Desh (place).** Latitude, longitude, timezone, ayanamsha. This frame licenses geography claims: where the cast is fixed, which zones apply, which sidereal frame was used. It licenses nothing about time.
- **Kaal (time).** Birth time, dasha windows, transit dates. This frame licenses temporal claims: which lords rule which windows, what the current sky shows. It licenses nothing about the place beyond its timezone.
- **Patra (the chart).** The computed placements, lordships, yogas, vargas, dashas. This frame licenses what the configuration is — never what the configuration outcome-forces.

A Desh fact is not a Kaal fact; a Patra signature is not an outcome. A claim that silently borrows authority from another frame is cut or tagged UNSUPPORTED (R1).

## Locked fast rules — never relaxed, in any tier

1. No model calculation of positions, degrees, nakshatras, dashas, vargas, or aspects. The engine computes; the model cites. A hand-rolled value is an invalid reading element, whatever its plausibility.
2. Sidereal zodiac; Lahiri ayanamsha by default. A non-default variant is named in provenance (R6) or the cast is treated as unverifiable (audit-checklist).
3. Vargas are read from tool output: D2, D9, D10, D16, D20, D24, D27, D30, D40, D60. They are never computed inline.
4. A Maraka (2nd or 7th lord) period is presented as a window of deep transformation. Never as a mortality window, never with probability language about lifespan (R4).
5. Lagna and lagna lord are read before any other house or planet claim. A reading that opens elsewhere opens wrong.
6. "The stars indicate x for you" and every correspondence-layer formulation are outside this plugin entirely. The correspondence registry does not exist; no claim here outruns it (R6 honesty ladder).

## Read order — computation, condition, capacity

For each planet, in this order: sign → house → dignity → combustion → avastha → shadbala → ishta/kashta phala → varga signature. The order is not negotiable; inverting it imports vibe over data.

### Which strengths outrank vibe-reading

- `shadbala.percentage` — the primary capacity indicator. Above 100 the planet is exceptionally strong; below 80 it is weak. This field outranks prose about "energy," "placement strength," or "good sign."
- `shadbala.ishta_kashta_phala` — Ishta Phala is auspicious delivery capacity; Kashta Phala is difficulty potential. High Ishta with high shadbala supports the claim. High Kashta with low shadbala forces a flag, not softening.
- `dignity` — exact sign-based status from the tool. Nine values, read never estimated (see dignity-table.md).
- `avasthas` — Yuva (adult) = full capacity; Bala (infant) = partial, flagged; Mrita (dead) = severely diminished delivery regardless of dignity.
- `is_combust` — a combust planet cannot deliver independently; its claims are flagged, never printed at face value.
- `is_retrograde` — inward energy, delays, past-life themes. Named as a condition of delivery; never an automatic negative and never an automatic positive.
- `d9_sign` equal to D1 `sign` — vargottama: the planet is significantly strengthened; name it vargottama in the grounds.

Any reading weight assigned to a planet that disagrees with these fields is a defect. Vibe does not outrank `shadbala.percentage`; enthusiasm does not outrank `is_combust`.

## House–lord logic

- Lordships are assigned from Rashi (whole-sign) signs counted from the ascendant.
- Result-giving follows Bhava Chalit when `bhava_chalit` shows a shift: the chalit house frames delivery; the Rashi house retains lordship. When the two diverge, grounds name both.
- A house-lord claim cites: the lord, its sign, its house (both, if split), dignity, shadbala, and affecting aspects. A claim with none of these fields is UNSUPPORTED (R1).
- Aspects are read from the tool's aspect fields only. Influence mapping cites those fields. An aspect not present in tool output is not asserted.

## Yogas — read, never detected

- Yoga claims read the `yogas` array. Hand-detection of yogas by the model is banned.
- Each cited yoga requires every forming condition verified from tool output before the claim prints (R1). One unmet condition: the yoga is cited as unmet or dropped.
- Delivery is gated by the forming planets: dignity, combustion, avastha, ishta/kashta. A yoga formed by an afflicted planet licenses a flagged, weaker form of the claim — never an unqualified one.
- No yoga count is ever printed as an endorsement. "The chart is rich in yogas" is filler; cut it.
- Neecha Bhanga and Viparita Raj claims follow the same rule: forming conditions decide; the label decides nothing.

## Vargas — which varga answers which question

D2 hora: wealth capacity. D9 navamsha: dharma and marriage reality; read alongside D1 for the D1/D9 contrast. D10 dashamsha: career; use `analyze_career_chart` for the full D10 read. D16 shodashamsha: vehicles, comforts. D20 vimshamsha: upasana, practice. D24 siddhamsha: education and exams. D27 bhamsha: strengths and weaknesses. D30 trimshamsha: misfortune and disease-type. D40 khavedamsha: maternal legacy. D60 shashtiamsha: the finest karmic sieve; use for Atmakaraka/Jupiter/Ketu cross-reference only when the question is spiritual or past-life.

A varga verdict is a cross-reference, never a standalone verdict. D9 or D10 contradicting D1 prints as a mismatch flag, never as a silent override.

## Affliction triad — delivery-risk flags

Any planet with `shadbala.percentage` below 80, `is_combust: true`, or `dignity: "debilitated"` is under strain; the houses and systems it governs carry the strain. Claims drawing on it are flagged, not embellished. D30 cross-references the affliction type. This triad yields flags only: it licenses no medical statement. Medical questions defer to qualified professionals per AGENTS.md guardrails and contract R4; this file restates that deferral in one clause and hands the detail to those files.

## Ashtakavarga thresholds

- SAV at 30 or above for a house sign: the sign supports abundance-level claims tied to it.
- SAV below 25 for a house sign: abundance claims anchored to that sign are refused or flagged.
- `prashtarashtakavarga` names which planets contribute bindus; cite contributors, not impressions.

## Configuration-consistency flags — never likelihood language

Legacy probability tiering (High/Moderate/Low odds of events) is banned in this plugin. When the chart shows an internal mismatch — yoga forming planets too weak to deliver, D1/D9 split, chalit shifts away from rashi, transit contradicting the natal signature the claim rests on, boundary-edge Moon — the reading prints a flag naming the mismatch and the fields on both sides. A flag states inconsistency. A flag never states probability, odds, or tiers.

If a legacy line cannot be phrased without prophecy language, it is dropped. This rule binds every file in this tree.

## Kaal Sarpa, Graha Yuddha, Gandanta

- `kaal_sarpa.active`: name the axis (ascending = Rahu-driven ambition; descending = Ketu-driven withdrawal; partial = mitigated) and the activation. No outcome language attaches.
- `graha_yuddha`: name the loser and the winner. Claims drawing on the loser's significations are flagged; the winner absorbs, not bestows.
- `gandanta`: name the afflicted planet and the boundary junction (Cancer→Leo, Scorpio→Sagittarius, Pisces→Aries). Claims from a gandanta planet print with delivery caution and never with certainty.
- 5th lord or Jupiter in `gandanta`: progeny claims print with a weakening flag (children keep-rule). The flag names the field; it does not quantify anything.

## Sphuta handling (children-class rules)

A Beeja/Kshetra Sphuta or any computed longitude combination appears in a reading only if a deterministic tool path computes it. If no tool computes it, the reading does not compute it by hand — not approximately, not "roughly." If a tool exposes it, cite the tool's values; if none does, the section is absent and says why.

## The one-line summary of this file

Compute nothing. Cite everything. Flag every mismatch. Promise nothing.
