# Dignity table — the deterministic strength reference

Dignity is read from the tool. It is never estimated, approximated, "felt," or re-derived by the model. If the cast does not print a dignity for a planet, that is a missing-field flag, not an invitation to guess.

## The nine dignity values (as printed by the engine)

| Tool value | Meaning | Claim weight |
|---|---|---|
| `exalted` | Planet in the sign of its maximum elevation | Supports strong claims; still gated by avastha and shadbala |
| `mooltrikona` | Planet in its mooltrikona arc | Supports strong claims |
| `own_sign` | Planet ruling its sign | Supports strong claims |
| `great_friend` | Great friendship (panchadha maitri gradient, high) | Supports claims |
| `friend` | Friendly sign | Supports claims |
| `neutral` | Neutral relationship | Claims valid but weakly supported; lean flagged if inferred |
| `enemy` | Hostile sign | Claims constrained; must be flagged |
| `great_enemy` | Great enmity | Claims heavily constrained; flagged; delivery weak |
| `debilitated` | Planet in the sign of its fall | Claims flagged; delivery severely weakened unless the tool's yoga array names a forming Neecha Bhanga |

Note on debilitation: Neecha Bhanga is a yoga with forming conditions. If the tool's `yogas` array names it as formed, cite it with its conditions. Absent that, debilitation stands at full force and every claim resting on the planet is flagged.

## Combustion

`is_combust: true` strips a planet's independent delivery. A claim resting on a combust planet prints with a combustion flag; the claim survives only if another, unafflicted ground carries it. A combust dasha or antardasha lord prints as constrained (dashas.md, transition flags). Combustion is a state to name, not a vibe to weigh: "combust" appears in the grounds with the field named.

## Retrograde

`is_retrograde: true` — inward motion, delays, past-life or unresolved themes. Retrograde is named as a condition of delivery with the field cited. It is neither blessing nor blight; the reading names it and moves on. A retrograde planet in Yuva with high shadbala is not demoted; a direct planet in Mrita is not rescued. Avastha outranks direction.

## Avastha capacity — delivery by age-state

| Tool value (age-state) | Capacity | Rule |
|---|---|---|
| Yuva (adult) | Full | The planet delivers at capacity; claims still bounded by dignity, shadbala, transit |
| Bala (infant) | Partial | Claims flagged: delivery diminished regardless of dignity |
| Mrita (dead) | Severely diminished | Claims heavily flagged; dignity and shadbala do not repair Mrita |

Read whatever set of avasthas the tool returns; the delivery rule is the same across names: only the mature adult state carries full capacity. Bala or Mrita demotes any claim rooted in the planet, whatever its sign.

## Ishta vs Kashta Phala — the ranking

`shadbala.ishta_kashta_phala` prints two values per planet. Rank their joint reading:

1. **High Ishta, low Kashta** — delivery supported as a theme; full wording available (with grounds).
2. **High Ishta, high Kashta** — delivery arrives with difficulty or cost; claims print with a difficulty flag; remedies gate stays R5.
3. **Low Ishta, high Kashta** — constrained delivery; claims flagged; no favourable wording.
4. **Low Ishta, low Kashta** — neutral; no delivery claim either direction. "Neither supported nor constrained" prints; no lean is invented.

Ishta/Kashta never promotes a combust or Mrita planet to full delivery, and never rescues a below-threshold claim into printable form (R2 gates apply with full force).

## What outranks what — the precedence list

When two readings of the same planet conflict, the higher-ranked instrument wins. Lower instruments are descriptive; they never override the higher.

1. Tool output itself — sign, house, degree, dignity, shadbala, avastha, combustion, retrograde, varga. Nothing outranks the ephemeris.
2. `shadbala.percentage` — primary capacity measure.
3. Avastha — delivery capacity right now.
4. Dignity — contextual elevation or depression.
5. Combustion and retrograde flags — conditions of delivery.
6. Ishta/Kashta phala — quality of what is delivered.
7. Varga placement with vargottama status — D9 congruence strengthens; D9 split flags.
8. Bhava Chalit shift — functional house for delivery; Rashi for lordship.
9. House placement and aspect structure — the interpretive frame, exercised only after 1–8.
10. Named yogas from the tool's array — formal combinations, real only with forming conditions.
11. Prose impressions ("strong energy," "good sign," "favourable vibe") — banned inputs; citing them prints UNSUPPORTED.

A reading that obeys items 9–11 while inverting 1–8 is invalid; the failure is visible in the appendix, which is the point (R6).

## Strength thresholds used elsewhere in this tree

- **9th lord `shadbala.percentage` above 100** — supports "natural dharmic alignment" as a theme (spiritual reading). At or below 100, that claim is flagged as unsupported.
- **5th lord `shadbala.percentage` above 100** — purva-punya (past-life merit) differential; cited as a field-level strength note, never as a karmic verdict.
- **SAV ≥ 30 / < 25** — see bphs-rulebook.md, Ashtakavarga thresholds; these govern abundance/struggle wording in finance and wealth-house claims.
- **Jaimini karakas** — Atmakaraka, Amatyakaraka, Darakaraka are read from the tool's `jaimini_karakas` output. They are never re-derived by degree comparison in the reading; the tool's assignment is the authority, and legacy disagreement between skills on the Darakaraka definition is resolved by this rule, not by re-calculation.

## Determinism rule

Every row in this file maps a tool field to a claim weight. No model judgment enters between the field and the weight. Where a chart is genuinely near a boundary (dignity at a Mooltrikona arc edge, degree near a sign edge), the reading prints the degree, names the boundary, and flags — the same boundary discipline as contract R4 triggers 2–3. It does not split the difference silently.
