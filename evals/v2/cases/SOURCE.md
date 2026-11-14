# v2 corpus source

The 40 birth records are sampled (seed 20261114) from
`vedastro-org/15000-Famous-People-Birth-Date-Location` on Hugging Face (MIT).
Only birth date, birth time, latitude, longitude, and the supplied UTC offset
are used; **names are dropped**. The supplied local time + offset is converted
to UTC, and dashaflow computes every chart with Lahiri/whole-sign. No VedAstro
calculation or expected verdict is used, so its methodology does not enter the
corpus.

Questions, clauses, required grounds, tags, and authoring rationale are
project-authored. The corpus was committed before any v2 arm output.
