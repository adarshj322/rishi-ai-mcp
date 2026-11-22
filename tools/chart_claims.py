"""Sign and house claim checks for the zero-human screen.

Numeric degree/date checks stay in eval_scoring. This module adds the
sign and house claims those checks cannot see. Aspects, yogas and
dignities are still out of scope.
"""

import re

SIGNS = {
    "aries": "Aries", "mesha": "Aries",
    "taurus": "Taurus", "vrishabha": "Taurus",
    "gemini": "Gemini", "mithuna": "Gemini",
    "cancer": "Cancer", "karka": "Cancer", "karkata": "Cancer",
    "leo": "Leo", "simha": "Leo",
    "virgo": "Virgo", "kanya": "Virgo",
    "libra": "Libra", "tula": "Libra",
    "scorpio": "Scorpio", "vrishchika": "Scorpio", "vrischika": "Scorpio",
    "sagittarius": "Sagittarius", "dhanu": "Sagittarius", "dhanus": "Sagittarius",
    "capricorn": "Capricorn", "makara": "Capricorn",
    "aquarius": "Aquarius", "kumbha": "Aquarius",
    "pisces": "Pisces", "meena": "Pisces", "mina": "Pisces",
}

PLANETS = (
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
    "Rahu", "Ketu", "Lagna", "Ascendant",
)

_SIGN_ALT = "|".join(sorted((re.escape(s) for s in SIGNS), key=len, reverse=True))
_PLANET_ALT = "|".join(sorted((re.escape(p) for p in PLANETS), key=len, reverse=True))

_SIGN_RE = re.compile(
    rf"\b({_PLANET_ALT})\b[,\s]*(?:(?:is|was|remains|sits|lies)\s+)?"
    rf"(?:placed|posited|located)?\s*(?:in|into)\s+(?:the\s+)?({_SIGN_ALT})\b",
    re.I,
)
_LAGNA_SIGN_RE = re.compile(
    rf"\b(Lagna|Ascendant)\b[,\s]*(?:(?:is|was)\s+)?(?:in\s+)?({_SIGN_ALT})\b",
    re.I,
)
_HOUSE_RE = re.compile(
    rf"\b({_PLANET_ALT})\b[,\s]*(?:(?:is|was|remains|sits|lies)\s+)?"
    rf"(?:placed|posited|located)?\s*(?:in|into)\s+(?:the\s+)?"
    rf"(?:(\d{{1,2}})(?:st|nd|rd|th)?\s+house|house\s+(\d{{1,2}}))\b",
    re.I,
)


def _varga_context(text, start, chars=30):
    """Return the divisional chart labelled immediately before the claim."""
    window = text[max(0, start - chars): start].lower()
    matches = list(
        re.finditer(r"\bd[\s-]?(\d{1,2})\b|\bdashamsha\b|\bdasamsha\b|\bnavamsha\b", window)
    )
    if not matches:
        return None
    last = matches[-1]
    if last.group(1):
        return f"d{int(last.group(1))}"
    return "d10" if "dash" in last.group(0) else "d9"


def _clause(text, start, end):
    left = text[:start]
    clause_start = max(left.rfind("."), left.rfind(";"), left.rfind("\n")) + 1
    right = text[end:]
    ends = [pos for pos in (right.find("."), right.find(";"), right.find("\n")) if pos != -1]
    clause_end = end + (min(ends) if ends else len(right))
    return text[clause_start:clause_end].lower()


def _paragraph_has_varga(text, start, end):
    """A varga label elsewhere in the paragraph makes the claim ambiguous."""
    left = text[:start]
    pstart = max(left.rfind("."), left.rfind("\n")) + 1
    right = text[end:]
    ends = [pos for pos in (right.find("."), right.find("\n")) if pos != -1]
    pend = end + (min(ends) if ends else len(right))
    return re.search(
        r"\bd[\s-]?\d{1,2}\b|\bdashamsha\b|\bdasamsha\b|\bnavamsha\b",
        text[pstart:pend],
        re.I,
    ) is not None


def _is_transit(text, start, end):
    """True only when `transit` is in the same clause as the claim."""
    return "transit" in _clause(text, start, end)


def _planet_data(chart, name, is_transit):
    """Return (data, display_name, scope) for the claim's chart context."""
    key = name.lower()
    if is_transit:
        for planet, data in ((chart.get("transit") or {}).get("planets") or {}).items():
            if planet.lower() == key:
                return data, planet, "transit "
        return None, name, "transit "
    if key in ("lagna", "ascendant"):
        return chart.get("lagna"), "Lagna", ""
    for planet, data in (chart.get("planets") or {}).items():
        if planet.lower() == key:
            return data, planet, ""
    return None, name, ""


def _canonical_sign(value):
    if not value:
        return None
    return SIGNS.get(str(value).strip().lower(), str(value).strip())


def _record_sign(text, match, chart, claims, contradictions, seen):
    planet, sign_raw = match.group(1), match.group(2)
    clause = _clause(text, match.start(), match.end())
    if any(term in clause for term in ("ishta devata", "karakamsha", "arudha", "indicated by")):
        return
    if planet.lower() in ("lagna", "ascendant"):
        if "lord" in clause:
            return
        pre = clause.split("lagna")[0] if "lagna" in clause else clause
        if "from" in pre:
            return
    varga = _varga_context(text, match.start())
    if not varga and _paragraph_has_varga(text, match.start(), match.end()):
        return
    sign = _canonical_sign(sign_raw)
    is_transit = _is_transit(text, match.start(), match.end())
    data, display, scope = _planet_data(chart, planet, is_transit)
    if varga:
        expected = _canonical_sign(data.get(f"{varga}_sign")) if data else None
        scope = f"{varga.upper()} "
    else:
        expected = _canonical_sign(data.get("sign")) if data else None
    key = (f"{scope}sign", planet.lower(), sign.lower() if sign else sign_raw.lower())
    if key in seen:
        return
    seen.add(key)
    claims.append({"kind": "sign", "planet": planet, "value": sign,
                   "expected": expected, "scope": scope.strip()})
    if expected and sign and sign.lower() != expected.lower():
        contradictions.append(f"{scope}{display} in {sign} (chart: {expected})")


def check_claims(text, chart):
    """Extract sign/house claims and compare the checkable ones to the chart.

    Claims are scoped by the nearest chart label: `D10`/`D9` signs use the
    matching `d10_sign`/`d9_sign`, and `transit` claims use the transit block.
    Relative houses ("from Moon") and varga houses are skipped because the
    chart does not carry those fields.

    Returns `claims` (all unique extracted claims), `checked` (claims whose
    chart value exists), and `contradictions` (mismatches against the chart).
    """
    claims = []
    contradictions = []
    seen = set()

    for match in _SIGN_RE.finditer(text):
        _record_sign(text, match, chart, claims, contradictions, seen)
    for match in _LAGNA_SIGN_RE.finditer(text):
        _record_sign(text, match, chart, claims, contradictions, seen)

    for match in _HOUSE_RE.finditer(text):
        planet = match.group(1)
        house = int(match.group(2) or match.group(3))
        if _varga_context(text, match.start()) or _paragraph_has_varga(
            text, match.start(), match.end()
        ):
            continue
        if any(
            term in _clause(text, match.start(), match.end())
            for term in ("ishta devata", "karakamsha", "arudha", "indicated by")
        ):
            continue
        if re.match(r"\s*from\b", text[match.end(): match.end() + 24], re.I):
            continue
        is_transit = _is_transit(text, match.start(), match.end())
        data, display, scope = _planet_data(chart, planet, is_transit)
        expected = data.get("house") if data else None
        key = (f"{scope}house", planet.lower(), house)
        if key in seen:
            continue
        seen.add(key)
        claims.append({"kind": "house", "planet": planet, "value": house,
                       "expected": expected, "scope": scope.strip()})
        if expected is not None and int(expected) != house:
            contradictions.append(
                f"{scope}{display} in house {house} (chart: house {int(expected)})"
            )

    checked = sum(1 for claim in claims if claim["expected"] is not None)
    return {"claims": claims, "checked": checked, "contradictions": contradictions}
