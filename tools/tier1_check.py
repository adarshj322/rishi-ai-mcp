#!/usr/bin/env python3
"""
Tier-1 determinism gate — rishi ground-truth plugin.

Binding caveat (evals/README §2.2, stamped verbatim there):
    "Shared lineage (dashaflow → pyswisseph → Moshier fallback):
     this is a regression/determinism gate, NOT astronomical-truth verification."

What this proves: the same input produces the same pinned output across fresh
interpreter invocations (dual invocation path, fresh subprocess per cast — this
is the path that avoids global pyswisseph state contamination). What it proves
nothing else. It says nothing about whether the ephemeris is astronomically
true, and must never be cited as doing so.

Method, per moment in evals/tier1/moments.json:
  1. Cast the chart twice, each time in a FRESH subprocess of this file
     (`--dump UTC LAT LON TZ`); wall-clock `metadata.computed_at_utc` is
     stripped before serialization — it is the only non-deterministic field;
     `yogas` array order is hash-randomized inside dashaflow (Python set
     iteration), so its order is canonicalized before serialization. No
     values are altered; only volatile ordering/timestamp noise is removed.
  2. Compare the two stdout byte strings for equality.
  3. Compare planet `degree_precise` positions (and lagna `degree`) between
     the two invocations: |a-b| / max(|b|, 1.0) <= 1e-6, i.e. relative with a
     1-degree floor (sub-degree positions are effectively absolute, 1e-6 deg).

Hash randomization is PINNED (PYTHONHASHSEED=0) in the dump subprocesses —
deliberately, and narrowly for this reason: dashaflow 1.5.0 yoga.py iterates
the set BENEFICS = {"Jupiter", "Venus", "Mercury"} with a `break` when a
natural benefic sits in the 10th from Lagna/Moon, so WHICH benefic is named
("Amala Yoga") otherwise depends on the interpreter's hash seed (observed:
5/300 corpus moments differ only in that selection; everything else in the
chart is byte-identical across fresh interpreters). Pinning the seed makes
runs byte-identical without touching engine output. Known residual risk: the
gate can no longer detect set-iteration-order nondeterminism elsewhere in the
engine — those are stable under the pinned seed and therefore invisible. The
`yogas` order is additionally canonicalized in the dump so order noise alone
cannot fail the gate. Fix belongs upstream in dashaflow (deterministic
iteration, e.g. sorted(BENEFICS)); until then this gate pins the environment,
not the engine bug.

Usage:
  python tools/tier1_check.py             # all 300 moments
  python tools/tier1_check.py --sample N  # deterministically sample N moments (even spacing)
  python tools/tier1_check.py --dump "YYYY-MM-DD HH:MM:SS" LAT LON TZ   # internal

Exit codes: 0 all pass · 5 at least one mismatch (moment named on stderr) · 2 usage/corpus error.
Prints "N moments OK" on success.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).resolve().parents[1]
CORPUS = REPO_ROOT / "evals" / "tier1" / "moments.json"
UTC_FMT = "%Y-%m-%d %H:%M:%S"
POS_TOL = 1e-6
POS_FLOOR_DEG = 1.0  # denominator floor for the relative comparison


def dump_chart(utc: str, lat: str, lon: str, tz: str) -> None:
    """Cast one chart and write normalized chart JSON (no trailing newline) to stdout."""
    from dashaflow import cast_chart

    dt_utc = datetime.strptime(utc, UTC_FMT).replace(tzinfo=timezone.utc)
    local = dt_utc.astimezone(ZoneInfo(tz))
    query_date = local.strftime("%Y-%m-%d")
    chart = cast_chart(local.strftime("%Y-%m-%d"), local.strftime("%H:%M:%S"),
                       float(lat), float(lon), tz, query_date=query_date)
    chart.get("metadata", {}).pop("computed_at_utc", None)
    chart["yogas"] = sorted(chart.get("yogas") or [],
                            key=lambda y: json.dumps(y, sort_keys=True, default=str))
    sys.stdout.write(json.dumps(chart, sort_keys=True, separators=(",", ":"), default=str))


def cast_subprocess(utc: str, lat: float, lon: float, tz: str) -> subprocess.CompletedProcess:
    env = {**os.environ, "PYTHONHASHSEED": "0"}  # pinned for dashaflow BENEFICS set-order defect; see module docstring
    return subprocess.run(
        [sys.executable, str(Path(__file__).resolve()),
         "--dump", utc, repr(lat), repr(lon), tz],
        capture_output=True,
        timeout=120,
        check=False,
        env=env,
    )


def position_deltas(a: dict, b: dict) -> list[str]:
    problems = []
    for name, pa in a.get("planets", {}).items():
        pb = b.get("planets", {}).get(name)
        if pb is None:
            problems.append(f"planet {name!r} missing from second invocation")
            continue
        da, db = pa.get("degree_precise"), pb.get("degree_precise")
        if da is None or db is None:
            problems.append(f"planet {name!r} missing degree_precise")
            continue
        delta = abs(da - db)
        rel = delta / max(abs(db), POS_FLOOR_DEG)
        if rel > POS_TOL:
            problems.append(f"planet {name}: |{da}-{db}| = {delta} deg (rel {rel:.3g} > {POS_TOL})")
    la, lb = a.get("lagna", {}).get("degree"), b.get("lagna", {}).get("degree")
    if la is not None and lb is not None:
        delta = abs(la - lb)
        rel = delta / max(abs(lb), POS_FLOOR_DEG)
        if rel > POS_TOL:
            problems.append(f"lagna: |{la}-{lb}| = {delta} deg (rel {rel:.3g} > {POS_TOL})")
    return problems


def check_moment(entry: dict) -> list[str]:
    utc = entry["utc"]
    lat, lon, tz = entry["lat"], entry["lon"], entry["timezone"]
    runs = [cast_subprocess(utc, lat, lon, tz) for _ in range(2)]
    failures = []
    for i, proc in enumerate(runs, start=1):
        if proc.returncode != 0:
            tail = proc.stderr.decode("utf-8", "replace")[-400:].strip()
            failures.append(f"invocation {i} exited {proc.returncode}: {tail}")
    if failures:
        return failures
    out1, out2 = runs[0].stdout, runs[1].stdout
    if out1 != out2:
        differ_at = next((i for i, (x, y) in enumerate(zip(out1, out2)) if x != y), min(len(out1), len(out2)))
        failures.append(f"chart JSON bytes differ at offset {differ_at} "
                        f"(len {len(out1)} vs {len(out2)})")
    try:
        chart1, chart2 = json.loads(out1), json.loads(out2)
    except json.JSONDecodeError as exc:
        failures.append(f"chart JSON did not parse: {exc}")
        return failures
    failures.extend(position_deltas(chart1, chart2))
    return failures


def sample_indices(n_total: int, n_sample: int) -> list[int]:
    if n_sample >= n_total:
        return list(range(n_total))
    if n_sample <= 1:
        return [0]
    return sorted({round(i * (n_total - 1) / (n_sample - 1)) for i in range(n_sample)})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dump", nargs=4, metavar=("UTC", "LAT", "LON", "TZ"),
                        help=argparse.SUPPRESS)  # internal: dump one normalized chart to stdout
    parser.add_argument("--sample", type=int, default=0,
                        help="deterministically check only N evenly spaced moments")
    args = parser.parse_args()

    if args.dump:
        dump_chart(*args.dump)
        return 0

    try:
        entries = json.loads(CORPUS.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"corpus not found: {CORPUS}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"corpus is not valid JSON: {exc}", file=sys.stderr)
        return 2
    if not isinstance(entries, list) or not entries:
        print("corpus must be a non-empty JSON array of moments", file=sys.stderr)
        return 2

    if args.sample:
        idxs = sample_indices(len(entries), args.sample)
        selected = [entries[i] for i in idxs]
    else:
        selected = entries

    failures_total = 0
    for entry in selected:
        problems = check_moment(entry)
        if problems:
            failures_total += 1
            print(f"FAIL {entry['utc']} ({entry.get('source')}, {entry.get('place')}):", file=sys.stderr)
            for p in problems:
                print(f"    {p}", file=sys.stderr)

    if failures_total:
        print(f"Tier-1 FAIL: {failures_total}/{len(selected)} moments mismatched", file=sys.stderr)
        return 5
    print(f"{len(selected)} moments OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
