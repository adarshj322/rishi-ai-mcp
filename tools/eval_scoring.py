"""Deterministic scoring primitives for the equal-cost bar runner.

Only two things here are deterministic: fabrication detection against the
chart whitelist, and mechanical required-ground presence. Everything
semantic belongs to the judge (tools/eval_runner.py).
"""

import math
import re

# Degree with optional minutes/seconds: "23°", "23.5°", "23°30'", "23° 30' 12\"".
_DEGREE_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*°(?:\s*(\d+(?:\.\d+)?)\s*['′])?(?:\s*(\d+(?:\.\d+)?)\s*[\"″])?"
)
_ISO_DATE_RE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
_MONTH_DATE_RE = re.compile(
    r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(\d{4})\b", re.I
)
_PLANET_NAMES = (
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu",
)
_MONTH_TO_NUM = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}
_ADJACENCY = 40


def compute_se(n: int) -> float:
    """Rule 1: SE = sqrt(p(1-p)/n) with p = 0.5, i.e. 0.5/sqrt(n)."""
    if n <= 0:
        raise ValueError("n must be positive")
    return 0.5 / math.sqrt(n)


def wilson_interval(k: int, n: int, z: float = 1.96) -> tuple:
    """Wilson score interval for k successes out of n at ~95% (z=1.96)."""
    if n <= 0:
        raise ValueError("n must be positive")
    if not 0 <= k <= n:
        raise ValueError("k must satisfy 0 <= k <= n")
    p = k / n
    denom = 1.0 + z * z / n
    centre = (p + z * z / (2.0 * n)) / denom
    half = z * math.sqrt(p * (1.0 - p) / n + z * z / (4.0 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def _chart_values(chart: dict, out: set, depth: int = 0) -> None:
    """Walk the chart JSON collecting every numeric value and string."""
    if depth > 40:
        return
    if isinstance(chart, dict):
        for v in chart.values():
            _chart_values(v, out, depth + 1)
    elif isinstance(chart, (list, tuple)):
        for v in chart:
            _chart_values(v, out, depth + 1)
    elif isinstance(chart, (int, float)):
        out.add(float(chart))
    elif isinstance(chart, str):
        out.add(chart.strip().lower())


def _planet_degrees(chart: dict) -> dict:
    """Map lowercase planet name -> list of degree values from the planets block."""
    result = {}
    planets = chart.get("planets") if isinstance(chart, dict) else None
    if isinstance(planets, dict):
        for name, data in planets.items():
            if not isinstance(data, dict):
                continue
            values = [
                float(data[key])
                for key in ("degree", "degree_precise", "longitude")
                if isinstance(data.get(key), (int, float))
            ]
            if values:
                result[name.lower()] = values
    lagna = chart.get("lagna")
    if isinstance(lagna, dict):
        for key in ("degree", "degree_precise"):
            v = lagna.get(key)
            if isinstance(v, (int, float)):
                result.setdefault("lagna", []).append(float(v))
    return result


def _degree_value(match: re.Match) -> float:
    deg = float(match.group(1))
    minutes = float(match.group(2) or 0)
    seconds = float(match.group(3) or 0)
    return deg + minutes / 60.0 + seconds / 3600.0


def _angular_delta(a: float, b: float) -> float:
    diff = abs((a % 360.0) - (b % 360.0))
    return min(diff, 360.0 - diff)


def extract_numeric_claims(text: str) -> list:
    """Return degree strings, ISO dates, and Month-YYYY dates found in text."""
    claims = [m.group(0).strip() for m in _DEGREE_RE.finditer(text)]
    claims.extend(m.group(0) for m in _ISO_DATE_RE.finditer(text))
    claims.extend(m.group(0) for m in _MONTH_DATE_RE.finditer(text))
    return claims


def find_fabrications(text: str, chart: dict) -> list:
    """Return claims that cannot be derived from the chart JSON.

    Degrees are planet-scoped: a degree near a planet name must match that
    planet's degree within 0.5 degrees. A degree that exists in the chart but
    belongs to another planet is still a fabrication. Unattached degrees must
    match some chart value within 0.5 degrees. Dates are checked against the
    whitelist of every chart value.
    """
    fabricated = []
    planet_degrees = _planet_degrees(chart)
    values = set()
    _chart_values(chart, values)

    for m in _DEGREE_RE.finditer(text):
        deg = _degree_value(m)
        window = text[max(0, m.start() - _ADJACENCY): m.end() + _ADJACENCY].lower()
        nearby = [p for p in _PLANET_NAMES if p.lower() in window]
        if nearby:
            ok = any(
                any(_angular_delta(deg, known) <= 0.5 for known in planet_degrees.get(p.lower(), []))
                for p in nearby
            )
        else:
            ok = any(
                _angular_delta(deg, v) <= 0.5
                for v in values
                if isinstance(v, float) and 0.0 <= v <= 360.0
            )
        if not ok:
            fabricated.append(m.group(0).strip())

    for m in _ISO_DATE_RE.finditer(text):
        if m.group(0).lower() not in values:
            fabricated.append(m.group(0))

    for m in _MONTH_DATE_RE.finditer(text):
        month = _MONTH_TO_NUM[m.group(1).lower()[:3]]
        year = int(m.group(2))
        iso_ok = any(
            isinstance(v, str)
            and _ISO_DATE_RE.fullmatch(v)
            and int(v[0:4]) == year
            and int(v[5:7]) == month
            for v in values
        )
        if not iso_ok:
            fabricated.append(m.group(0))

    seen = set()
    out = []
    for item in fabricated:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def deterministic_verdict(text: str, ledger_entry: dict, chart: dict) -> dict:
    """Deterministic pass/fail: fabrication + mechanical required grounds.

    `ledger_entry` shape (from evals/cases/ledger.json):
      {"clauses": [{"text": str, "mechanical": bool}], "required_grounds": [str]}
    A required ground is satisfied when its literal substring appears in the
    text (case-insensitive). Only mechanical clauses are enforced here.
    """
    failures = []
    checked = []

    fabricated = find_fabrications(text, chart)
    checked.append("fabrication")
    failures.extend(f"fabricated: {item}" for item in fabricated)

    lowered = text.lower()
    for ground in ledger_entry.get("required_grounds", []):
        checked.append(f"required_ground: {ground}")
        if ground.lower() not in lowered:
            failures.append(f"missing required ground: {ground}")

    return {"pass": not failures, "failures": failures, "checked": checked}
