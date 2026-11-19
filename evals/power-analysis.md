# Power analysis — v2 + v2r paired results

**Status: exploratory, post-hoc. Not a pre-committed verdict.** The v2 and v2r
Evidence Log rows remain the claims of record. Pooling the two runs was not
pre-specified, so the pooled intervals below do not upgrade the claim.

## Inputs

Both verdicts are valid: 40/40 items, no exclusions, no disqualifications, no
judge errors, no cap hits.

| run | n | delta (shipped − bare) | paired SD | 95% bootstrap CI |
|---|---|---|---|---|
| v2 | 40 | +0.100 | 0.4414 | [−0.025, 0.225] |
| v2r | 40 | +0.150 | 0.6222 | [−0.05, 0.35] |

Discordant counts (shipped-only / tie / bare-only): v2 6/32/2, v2r 11/24/5.

## Pooled (post-hoc)

- Pooled items, n = 80: delta **+0.125**, paired SD 0.5366, SE 0.0600,
  normal 95% CI **[+0.0074, +0.2426]**; paired bootstrap **[0.0, 0.2375]**.
- Fixed-effect inverse-variance meta-analysis: delta **+0.117**, SE 0.0569,
  95% CI **[+0.0052, +0.2283]**.

The pooled point estimate is consistent with a small positive effect, but the
paired bootstrap lower bound touches zero. The fixed-effect meta interval
excludes zero only barely and assumes a common effect across the two runs;
with two studies the between-run variance is not reliably estimable.

## What n would settle it

Using the pooled observed paired SD (0.537) and the pooled delta (0.125):

| target | required n |
|---|---|
| 95% CI excludes zero | **71** |
| 80% power, two-sided 0.05 | **145** |

With the conservative SE rule (SD = 0.5): 62 and 126 respectively.

At n = 40 the power to detect the pooled effect is about **0.31**; the minimum
detectable effect at n = 40 and 80% power is **0.238**, roughly twice the
observed 0.125.

Power at the pooled effect (normal approximation): n=80 → 0.55, n=120 → 0.72,
n=160 → 0.84, n=200 → 0.91.

## Recommendation

- **Do not run another n = 40 replication expecting a conclusive interval.** It
  is underpowered (≈31%) and its result would be another directional row.
- Either accept the directional claim from the two pre-committed runs, or
  pre-commit a fresh corpus at **n ≈ 150** for 80% power. The n ≈ 71 figure is
  the floor for the pooled point estimate to exclude zero, not a power target;
  it is sensitive to the observed effect and would still leave the result
  fragile.
- Any new corpus must follow the existing rules: fresh items, no reuse, locked
  gate and floor before data, one pilot then one verdict, append-only Evidence
  Log.

## Decision (2026-11-19)

Owner accepted the recommendation: **the eval program stops at the directional
claim.** No n = 150 or n = 230 run is planned. The two pre-committed Evidence
Log rows remain the claims of record; the pooled analysis above is exploratory
and is not a new verdict. The next measurement is the Vedic agreement panel /
v3 registry, which addresses whether the readings are actually good rather
than another correctness corpus. Any future correctness run requires a new
owner-written pre-commitment.

## Reproduction

The per-item `pass` flags are in
`evals/results/2026-11-14-v2-verdict/results.json` and
`evals/results/2026-11-15-v2r-verdict/results.json`. The paired difference is
`shipped.pass − bare.pass` per item; the bootstrap uses
`tools/eval_runner.py::_paired_delta_interval` with the same seed.
