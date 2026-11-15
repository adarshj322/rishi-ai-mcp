# v2 replication — shipped path vs bare MCP (fresh corpus)

**BINDING — locked before data. Owner: Adarsh J. Ratified: 2026-11-15.**

This pre-commitment replicates the v2 result on a fresh 40-item corpus. It does
not re-open v2 and does not reuse any v2 item or chart.

## 1. The question

On a fresh 40-item JyotishQA set, does the shipped path (doctrine + sample-and-
vote + deterministic check) beat bare MCP by the same locked margin?

## 2. Locked decisions

- **n = 40** fresh items; no overlap with `evals/v2/cases/`.
- **SE rule:** rule 1, `0.5/sqrt(40) = 0.079057`.
- **Locked gate:** `delta (shipped − bare) > 0.079057`.
- **Floor:** same as v2 — `glm-5.3-flash` arms at provider-default reasoning,
  `deepseek-v4.1-flash` judge at provider-default reasoning (16k cap),
  `B = 12,000`, OpenCode Go.
- **Consequence — replication claim gate:**
  - Clears: the v2 directional result is **replicated on a second independent
    40-item corpus**. May report the replication with intervals; no
    predictive-validity claim.
  - Does not clear: the v2 result is **not replicated**; the v2 claim remains
    single-corpus/directional. No product removal.
- No tuning between pilot and verdict; same rules as v2.

## 3. Arms and scoring

- `shipped` — doctrine + three samples at temperature 0.7 + deterministic
  pick-best; `bare` — no doctrine, one call at temperature 0.
- Same scoring, judge, anonymization, validity rules, and paired bootstrap as
  v2; the instrument is the post-fix v2 instrument.
- Item-level all-or-nothing; 1–3 mandatory clauses; required grounds only on
  chart-grounded items, capped at 3.

## 4. Corpus

40 fresh records from the VedAstro 15k birth set (MIT), excluding all v2
charts; names dropped, local time + offset converted to UTC. Questions,
clauses, grounds, tags, and rationale are project-authored; see
`cases/SOURCE.md` and `cases/ledger.json`. Committed before any arm output.

## 5. Run protocol and Evidence Log

Smoke → pilot → same-floor verdict; invalid on exclusions/judge errors/cap
hits. One append-only log.

| date | commit | corpus size | SE rule | arm | margin observed | verdict | notes |
|---|---|---|---|---|---|---|---|
| `__PENDING__` | `__PENDING__` | `__PENDING__` | `__PENDING__` | `__PENDING__` | `__PENDING__` | `__PENDING__` | `__PENDING__` |

## 6. Change control

Only an explicit owner rewrite changes this file. Rows are append-only.
