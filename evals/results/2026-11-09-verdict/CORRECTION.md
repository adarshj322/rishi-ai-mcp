# CORRECTION — this run is not a verdict

**Status: INVALID AS A VERDICT (withdrawn 2026-11-09).**

`evals/README.md` §10 (Model-substitution rule) requires that a base-model
change re-opens phase acceptance: the equal-cost bar is re-measured from
scratch, the first measurement under the new configuration is a new pilot,
and the locked gate is re-derived before any new verdict is taken.

This run changed the base model after the pilot (arms
`deepseek-v4.1-flash` → `glm-5.3-flash`; judge `muse-spark-1.3-contributor`
→ `deepseek-v4.1-flash`; reasoning none → default; budget 6000 → 12000).
It therefore cannot read against the gate locked by the pilot. It is a
**floor-change experiment**, not a verdict. The verification cut briefly
committed on top of it (`b93116d`, `9ab6fd3`, `0e5383b`, `97de940`) has
been reverted; verification remains off until a valid measurement.

The Evidence Log carries an appended correction row referencing this file.
The data in `results.json` is unmodified; `report.md` carries this warning
at its head.
