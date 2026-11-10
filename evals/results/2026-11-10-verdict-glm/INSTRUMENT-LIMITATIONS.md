# Instrument limitations recorded with this verdict

These are known limitations of the frozen instrument used for the 2026-11-10
GLM-floor pilot and verdict. They are recorded here rather than fixed after
measurement: changing the scoring rules after the run would invalidate the
verdict under `evals/README.md` §4.

- **Relational-degree false positives.** The fabrication check treats a
  degree within ±120 characters of a body name as an absolute claim. Two
  known cases (`g-09` "~3.6° apart", `g-05` a grounded degree attributed to
  Lagna) were flagged as fabricated. Both hit the `with` arm only; the
  reviewer found neither flips a pass, so the bias is against verification,
  not in its favour.
- **Date-range leniency.** Any ISO/month date inside any chart dasha span is
  accepted, so specific invented dates inside a long dasha window are not
  detectable. This affects both arms and does not favour verification.
- **Transit/natal degree merge.** Transit planet degrees are merged into the
  natal whitelist, so a natal/transit confusion can pass the fabrication
  check.

These are scoped for a v2 instrument under a new pre-commitment; they are not
grounds to re-tune the current verdict.
