# Conservative re-score — 2026-11-22 sign/house run

The run used the first sign/house checker. Its three A1 failures were inspected and all
three were **scope errors**, not chart contradictions:

- `v2-g-01` — the `D9` label belonged to an earlier “Mars d9 Scorpio” note; “10th lord
  Mars in Libra” is a D1 claim.
- `v2-g-07` — “Lagna Pisces” is the D1 lagna inside a paragraph that also discusses D2.
- `v2-g-19` — “Ishta Devata indicated by Saturn in Aquarius” is a derived indicator,
  not a natal placement.

The checker now applies only adjacent varga labels and skips ambiguous paragraphs,
lagna-lord/“from Lagna” phrases, and Ishta/Karakamsha statements. Re-scoring the saved
texts:

| Check | Result |
|---|---|
| A1 | **18/20 clean, 18 exercised, 0 real contradictions** |
| A2 | **17/20, 18 exercised** |
| Sign/house claims | **105 checked across real + decoy, 1 contradiction** |

Remaining non-clean items:

- `v2-g-01` — A2 fails on a decoy `0.7063°` derived difference and a residual D10/Rahu
  scope ambiguity. A1 is clean.
- `v2-g-19`, `v2-g-20` — not exercised (no checkable claims).

## Interpretation

The regex sign/house checker is a **candidate detector, not a gate**. Free-form readings
mix D1, D9, D10 and karakamsha statements in one paragraph, so unambiguous attribution
needs structured claims from the arm. Until then, the sign/house layer supports coverage
and review, not a pass/fail claim. The degree/date A1 and the A2 chart-swap remain the
deterministic layers; the claim boundary is unchanged.
