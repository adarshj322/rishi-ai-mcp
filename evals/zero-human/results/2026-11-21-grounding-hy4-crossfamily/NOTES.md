# Zero-human grounding run — 2026-11-21/22

**Config:** arm `hy4-flash-free` @ max; judges `deepseek-v4.1-flash` @ max,
`muse-spark-1.3-contributor` @ xhigh, `beam-free` @ max; 3 trials; budget 120,000 per arm.
Transport `opencode-go`; corpus `grounding.jsonl` (20 items); dashaflow 1.5.3.

## Results

| Check | Pass | Exercised | Notes |
|---|---|---|---|
| A1 chart-fact | 16/20 | 16/20 | 0 fabrications in any reading |
| A2 chart-swap | 14/20 | 14/20 | every exercised item passed |
| A4 judge consistency | 12/20 | 20/20 | 0 judge errors; failures are disagreement |

Arm output tokens: 844,795.

Per-judge pass totals: `deepseek-v4.1-flash` 46/60, `muse-spark-1.3-contributor` 52/60,
`beam-free` 47/60.

## What this says

- No reading fabricated a degree or date. Chart-grounding held on every item that
  asserted a checkable numeric claim.
- The four A1 and six A2 non-passes are **not exercised**, not contradictions: the
  reading (or its decoy) asserted no numeric claim. A2 passed on all 14 items where
  both readings made a claim.
- A4 is the real finding. Pairwise agreement fell to 0.44–0.50 on four items, with
  within-model agreement as low as 0.33 across three temperature-0 trials. The judges
  are unstable at these settings; the panel is flagging itself, not a coding bug.
- Three A4 failures are near-misses at 0.78 against the 0.80 gate; one is 0.61.

## Boundary

This run supports **conformance and reliability** claims only: chart-grounded,
rule-faithful, internally consistent — not validated against expert judgment. It does
not measure reading quality, correspondence to the person, or parity with a jyotishi.

## Caveats

- dashaflow used the Moshier fallback (no Swiss `.se1` files), so chart facts carry
  reduced ephemeris accuracy.
- A1 checks degrees and dates only; sign and house claims are not checked.
- One corpus, one arm model, one run. A4 is a single panel at one set of efforts.

## Post-hoc sign/house re-score (2026-11-22)

The original run used the degree/date-only checker. The saved real and decoy texts were
re-scored with the new scoped sign/house checker, without new model calls:

- **93 sign/house claims** checked across real and decoy readings, **0 contradictions**.
- **A1 exercised: 20/20** (was 16/20); every reading now has at least one checkable claim.
- **A2 exercised: 18/20** combined numeric + sign/house (was 14/20); `v2-g-19` and
  `v2-g-20` still assert no checkable claims.
- The 12-hour decoy left most planetary signs unchanged, so sign-heavy A2 comparisons
  had high overlap. The checker now shifts the decoy by 12 hours **and 15 days** (plus
  the transit date) so signs actually diverge in future runs.

This is a re-score, not a new run. Numeric date checks were excluded from the re-score
because the readings embed `query date 2026-11-21` and the chart query date has since
moved to 2026-11-22, which would flag the run-date footer as a fabricated date.
