# Dashas — Vimshottari read order

This file binds every dasha, antardasha, and pratyantar utterance. The engine computes the dasha system; the reading cites it. The prerequisite is absolute: no dasha timing claim prints without the natal lunar-mansion degree in the grounds (contract R4, trigger 4).

## Prerequisite — the lunar-mansion degree

- The cast prints Moon's nakshatra and Moon's degree within it. That degree is the seed of the Vimshottari sequence.
- Any dasha claim that prints without this degree in the appendix is invalid, regardless of how plausible the window is.
- If the tool output lacks the lunar-mansion degree, the dasha section refuses: print the missing field, print nothing else about timing, and ask the user to verify the cast.
- "Approximately degree" is not the degree. Compression is not a substitute for the field.

## Levels 1–3 — the read order

Read strictly maha → antar → pratyantar. No level is read before its parent. Each level cites: lord, sign, house, dignity, `shadbala.percentage`, avastha, and window start–end dates from `dashas.timeline`.

- **Maha dasha.** Sets the frame for the whole window. Claims attach to the maha lord's placement and strength first; every lower-level claim sits inside that frame.
- **Antar dasha.** Modifies within the maha. Claims attach to the antar lord's house and its relationship to the maha lord (conjunction, mutual aspect, exchange, or none visible in tool output).
- **Pratyantar dasha.** Adds granularity only when the question demands it (an event-adjacent window, an election overlay). Still never renders a date. Pratyantar used to flatter a date request is R4/R6 behaviour: refuse the date, print the window.

Levels 4–5 (sukshma, prana) are exposed by the engine. They are read only for day-level questions and only with the full cast in hand. They do not rescue a weak maha or antar read; they refine it inside its constraints.

## Timeline — the only date authority

- `dashas.timeline` is the only accepted source for window boundaries. Windows are quoted from it; they are never interpolated, summed, or averaged from antar lengths.
- When two lords exchange influence across a transition, the reading names the transition date and the grounds for both sides, in order.
- If the timeline and the prose disagree, the timeline wins and the prose is rewritten.

## Transition flags

- **Approaching transition inside the window**: name the transition date and both lords' grounds; the reading divides into before/after statements. A transition is never smoothed into "a changing phase."
- **Weak dasha lord** (`shadbala.percentage` below 80, combust, debilitated, Bala or Mrita avastha): the window's themes print as constrained delivery — flagged, not denied, and never presented as favourable by omission.
- **Strong dasha lord** (above 100, Yuva, unafflicted, vargottama where applicable): the window's themes print as supported themes. Never as outcomes.
- **Neecha Bhanga or Viparita Raj fire on the dasha lord per the tool's `yogas` array**: the flag names the yoga and its forming conditions; delivery language stays bounded.

## Sade Sati — next-TS check via the tool

- Sade Sati is claimable only from `cast_transit_chart`'s `sade_sati` output combined with the natal Moon's sign and nakshatra. It is never derived from arithmetic on the page.
- Before any statement about an upcoming Sade Sati window ("next TS"), re-call `cast_transit_chart` for the target date. The natal cast alone cannot time a transit.
- The statement names: the tool's `sade_sati` field value, transiting Saturn's sign and house (from lagna and from Moon per the cast), and the `sav_points` of the transit sign where the tool prints them.
- Language is structural: Saturn–Moon 12th/1st/2nd cadence. Fear framing is banned (R4). What ameliorates the cadence is named only from fields (dignity, shadbala, SAV) — never from optimism.
- A Sade Sati invocation never carries mortality language, implicit or explicit. Maraka logic does not enter here.

## Dasha-lord strength by shadbala

Every lord in the active chain (maha, antar, pratyantar used) receives the same three reads:

1. `shadbala.percentage` — above 100 supports emphasis; below 80 flags constraint.
2. Avastha — Yuva full, Bala partial, Mrita diminished regardless of sign dignity.
3. Affliction — combust or debilitated flags the lord's claims.

The chain is reported as its weakest link constraining it. If the maha lord is strong but the antar lord is Mrita, the antara's materially weaker delivery is the operative constraint for the sub-window and the reading says so with both fields cited.

## Dasha claims and the boundary of validity

Every dasha statement ends with its boundary: the window frames themes the chart supports; it does not determine events, choices, or dates. The correspondence layer is unclaimed in this plugin regardless of how strong the chain reads (R6, honesty ladder).

## Other dasha systems

The engine exposes Yogini and Chara dashas alongside Vimshottari. Vimshottari is the doctrine default for timing language. A non-default system is named in the grounds and in provenance; it is never mixed mid-sentence with Vimshottari without naming both.

## What this file forbids, with consequences

- Dasha date without lunar-mansion degree: refuse (trigger 4).
- "Favourable by 2027" and every date-flattering formulation: cut; the window is printed with its boundary instead.
- Sade Sati timed from natal-only reasoning: refuse; re-call the transit cast.
- Weakest-link chain printed as strong: audit finding; the reading is rewritten.
- Five-level dasha arithmetic quoted without the timeline: refuse; quote the timeline.
