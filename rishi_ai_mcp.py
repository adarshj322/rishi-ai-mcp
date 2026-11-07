"""
RishiAI MCP Server — Vedic astrology tools via the Model Context Protocol.

Thin wrapper around the DashaFlow library. Exposes 12 tools:
  cast_vedic_chart, cast_transit_chart, calculate_compatibility_tool,
  check_muhurtha_tool, analyze_career_chart, get_dasha_periods_tool,
  get_strength_table_tool, get_yoga_list_tool, get_time_sensitivity_tool,
  get_transit_ingresses_tool, get_sade_sati_timeline_tool, get_gochara_tool.

Install:  pip install rishi-ai-mcp
Run:      rishi-ai-mcp            (console entry-point)
  or:     python rishi_ai_mcp.py  (direct)
"""

__version__ = "1.5.0"

from typing import Dict, Any
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError
from dashaflow import (
    cast_chart,
    cast_transit,
    calculate_compatibility,
    check_muhurtha,
    analyze_career,
    summarize_chart,
    get_dasha_periods,
    get_strength_table,
    get_yoga_list,
    get_time_sensitivity,
    get_transit_ingresses,
    get_sade_sati_timeline,
    get_gochara,
)
from dashaflow.errors import DashaFlowError, InvalidInputError


def _raise(err: Exception) -> None:
    """Convert engine errors to MCP ToolError (isError) with guidance."""
    if isinstance(err, DashaFlowError):
        raise ToolError(str(err)) from err
    raise ToolError(f"Unexpected error: {err}") from err

mcp = FastMCP(
    "vedic-astrology",
    instructions="Vedic Astrology chart calculator using Swiss Ephemeris (Sidereal Lahiri)",
)


@mcp.tool()
def cast_vedic_chart(
    dob: str,
    time: str,
    lat: float,
    lon: float,
    timezone: str,
    query_date: str = "",
    detail: str = "compact",
    gender: str = "",
    ayanamsha: str = "lahiri",
) -> Dict[str, Any]:
    """
    Calculate a Vedic birth chart (Sidereal Lahiri ayanamsha).

    detail="compact" (default, <4KB): lagna, condensed planets
    (sign/house/nakshatra/dignity + vargottama/yogakaraka flags), active
    dasha lords (Vimshottari/Yogini/Chara — no timelines), yoga names,
    strength totals, SAV, dosha flags, birth-time sensitivity verdict
    (robust/borderline/fragile). Each section names the slice tool for
    full data.
    detail="full": the complete chart (planets with 14 vargas, 5-level
    dasha timelines for all 3 systems, full yogas, Shadbala, Vimshopaka,
    Sodhita Ashtakavarga, Jaimini, Bhava Chalit, avasthas, doshas).

    Full output keys: metadata, panchang, lagna, planets, dashas,
    yogini_dasha, chara_dasha, yogas, ashtakavarga, sodhita_ashtakavarga,
    jaimini_karakas, shadbala, vimshopaka, bhava_chalit, avasthas,
    kaal_sarpa, graha_yuddha, gandanta, arudha_padas, upapada, karakamsha.
    Planet dignity is one of: exalted, mooltrikona, own_sign, great_friend,
    friend, neutral, enemy, great_enemy, debilitated.

    Parameters:
        dob: Date of birth as "YYYY-MM-DD" (e.g. "1990-04-15")
        time: Time of birth as "HH:MM[:SS]" in 24-hour format (e.g. "14:30")
        lat: Birth latitude as decimal degrees (e.g. 28.6139 for New Delhi)
        lon: Birth longitude as decimal degrees (e.g. 77.2090 for New Delhi)
        timezone: IANA timezone string (e.g. "Asia/Kolkata", "America/New_York")
        query_date: Optional date for Dasha lookup as "YYYY-MM-DD". Defaults to today.
        detail: "compact" (default) or "full" (complete chart).
        gender: Optional "male" / "female" — interpretation framing only
            (e.g. Stree Deergha context). Does not change calculations.
        ayanamsha: One of lahiri (default), lahiri_icrc, true_citra, raman,
            krishnamurti, krishnamurti_vp291, yukteshwar, fagan_bradley.
    """
    try:
        if gender and gender not in ("male", "female"):
            raise InvalidInputError(
                f"Invalid gender '{gender}'. Expected 'male' or 'female'.")
        if detail not in ("compact", "full"):
            raise InvalidInputError(
                f"Invalid detail '{detail}'. Expected 'compact' or 'full'.")
        chart = cast_chart(dob, time, lat, lon, timezone, query_date or None,
                           ayanamsha=ayanamsha)
        if detail == "compact":
            sensitivity = get_time_sensitivity(
                dob, time, lat, lon, timezone, query_date=query_date or None,
                ayanamsha=ayanamsha)
            result = summarize_chart(chart, detail=detail,
                                     time_sensitivity=sensitivity)
        else:
            result = summarize_chart(chart, detail=detail)
        if gender:
            result["interpretation_context"] = {"gender": gender}
        return result
    except Exception as e:
        _raise(e)


@mcp.tool()
def cast_transit_chart(
    transit_date: str,
    dob: str,
    time: str,
    lat: float,
    lon: float,
    timezone: str = "Asia/Kolkata",
    ayanamsha: str = "lahiri",
) -> Dict[str, Any]:
    """
    Calculate planetary transits for a given date overlaid on a natal chart.

    Returns (JSON):
    - `planets`: For each transit planet:
      - `sign`, `degree`, `is_retrograde`, `nakshatra`
      - `sav_points`: Ashtakavarga points in the transiting sign
      - `house_from_lagna`, `house_from_moon`
    - `sade_sati`: `{ active, phase, saturn_transit_sign, natal_moon_sign }`
    - `rahu_ketu_axis`: `{ rahu_house_from_lagna, ketu_house_from_lagna, rahu_sign, ketu_sign }`

    Parameters:
        transit_date: The date to compute transits for as "YYYY-MM-DD" (e.g. "2026-02-28")
        dob: Date of birth as "YYYY-MM-DD"
        time: Time of birth as "HH:MM" in 24-hour format
        lat: Birth latitude as decimal degrees
        lon: Birth longitude as decimal degrees
        timezone: IANA timezone string (defaults to "Asia/Kolkata")
        ayanamsha: One of lahiri (default), lahiri_icrc, true_citra, raman,
            krishnamurti, krishnamurti_vp291, yukteshwar, fagan_bradley.
    """
    try:
        return cast_transit(transit_date, dob, time, lat, lon, timezone,
                            ayanamsha=ayanamsha)
    except Exception as e:
        _raise(e)


@mcp.tool()
def get_transit_ingresses_tool(
    dob: str,
    time: str,
    lat: float,
    lon: float,
    timezone: str,
    start_date: str,
    end_date: str,
    bodies: list[str] | None = None,
    ayanamsha: str = "lahiri",
) -> Dict[str, Any]:
    """
    Exact sign-ingress instants for selected bodies over a date range.

    Answers "when does Saturn enter Pisces?" with the precise instant, not
    just the sign on a given day. Retrograde re-entries appear as separate
    events, because a body that backs over a boundary really does cross it
    twice.

    Returns (JSON):
    - `range`: { `start`, `end` } (inclusive local dates)
    - `bodies`: the bodies scanned
    - `ingresses`: chronological list of { `planet`, `date` (local calendar
      date), `instant_utc` (minute precision), `from_sign`, `to_sign`,
      `direction` (direct/retrograde), `house_from_lagna`, `house_from_moon` }

    Parameters:
        dob, time, lat, lon, timezone: birth details (time "HH:MM[:SS]")
        start_date, end_date: "YYYY-MM-DD", inclusive, 15 years maximum
        bodies: optional list; default Jupiter, Saturn, Rahu. Allowed: Sun,
            Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu. Moon is
            rejected (changes sign every ~2.25 days) — use cast_transit_chart.
        ayanamsha: One of lahiri (default), lahiri_icrc, true_citra, raman,
            krishnamurti, krishnamurti_vp291, yukteshwar, fagan_bradley.
    """
    try:
        return get_transit_ingresses(
            dob, time, lat, lon, timezone, start_date, end_date, bodies=bodies,
            ayanamsha=ayanamsha)
    except Exception as e:
        _raise(e)


@mcp.tool()
def get_sade_sati_timeline_tool(
    dob: str,
    time: str,
    lat: float,
    lon: float,
    timezone: str,
    start_date: str,
    end_date: str,
    merge_gap_days: int = 180,
    ayanamsha: str = "lahiri",
) -> Dict[str, Any]:
    """
    Sade Sati timeline: Saturn's rising, peak, and setting phases over the
    natal Moon, as disjoint date spans.

    Answers "when is my Sade Sati and when does it end?". Short gaps where
    Saturn steps outside the 12th/1st/2nd from the Moon are absorbed into the
    surrounding span when they are <= `merge_gap_days`; a retrograde excursion
    into a different phase stays its own span and also appears in `crossings`.

    Returns (JSON):
    - `natal_moon_sign`, `range`, `merge_gap_days`
    - `active_at_start`, `active_at_end`: whether Sade Sati is on at each edge
    - `spans`: { `phase` (rising/peak/setting), `start`, `end`, `days`,
      `gap_days`, `in_phase_days`, `interruptions`, `starts_before_range`,
      `ends_after_range` }. Range-edge flags mean the span was clipped, not
      that it began/ended there.
    - `crossings`: every Saturn sign change with `date`, `instant_utc`,
      `from_sign`, `to_sign`, `from_phase`, `to_phase`, `direction`.

    Parameters:
        dob, time, lat, lon, timezone: birth details (time "HH:MM[:SS]")
        start_date, end_date: "YYYY-MM-DD", inclusive, 15 years maximum
        merge_gap_days: absorb off gaps up to this many days (default 180;
            0 returns literal spans)
        ayanamsha: One of lahiri (default), lahiri_icrc, true_citra, raman,
            krishnamurti, krishnamurti_vp291, yukteshwar, fagan_bradley.
    """
    try:
        return get_sade_sati_timeline(
            dob, time, lat, lon, timezone, start_date, end_date,
            merge_gap_days=merge_gap_days, ayanamsha=ayanamsha)
    except Exception as e:
        _raise(e)


@mcp.tool()
def get_gochara_tool(
    dob: str,
    time: str,
    lat: float,
    lon: float,
    timezone: str,
    transit_date: str,
    ayanamsha: str = "lahiri",
) -> Dict[str, Any]:
    """
    Transit quality from the natal Moon on one date, weighted by natal SAV.

    Each transiting planet is scored by its house from the natal Moon against
    the classical favourable-house table; the natal sign's Sarvashtakavarga
    points then temper the verdict. Reference is always the Moon, the classical
    gochara reference.

    Returns (JSON):
    - `transit_date`, `reference` ("moon"), `natal_moon_sign`
    - `sav_average`: mean of the 12 natal SAV values
    - `planets`: per planet { `sign`, `house_from_moon`, `is_retrograde`,
      `sav_points`, `house_quality` (favorable/unfavorable),
      `weighted_verdict` (favorable/mixed/unfavorable), `notes` }
      Notes state the house rule, the SAV comparison, and for Rahu/Ketu the
      "Raman convention (nodes)" provenance (BPHS gives no node transit rules).

    Parameters:
        dob, time, lat, lon, timezone: birth details (time "HH:MM[:SS]")
        transit_date: "YYYY-MM-DD"
        ayanamsha: One of lahiri (default), lahiri_icrc, true_citra, raman,
            krishnamurti, krishnamurti_vp291, yukteshwar, fagan_bradley.
    """
    try:
        return get_gochara(dob, time, lat, lon, timezone, transit_date,
                           ayanamsha=ayanamsha)
    except Exception as e:
        _raise(e)


@mcp.tool()
def get_dasha_periods_tool(
    dob: str,
    time: str,
    lat: float,
    lon: float,
    timezone: str,
    query_date: str = "",
    ayanamsha: str = "lahiri",
) -> Dict[str, Any]:
    """
    Full dasha chains with dates for all three timing systems.

    Drill-down for the compact chart's dasha section. Returns Vimshottari
    (Maha→Prana + 120-year timeline), Yogini (Maha/Antar/Pratyantar +
    36-year cycles), and Chara (sign Maha/Antar + timeline).

    Parameters: same birth details as cast_vedic_chart.
        ayanamsha: One of lahiri (default), lahiri_icrc, true_citra, raman,
            krishnamurti, krishnamurti_vp291, yukteshwar, fagan_bradley.
    """
    try:
        chart = cast_chart(dob, time, lat, lon, timezone, query_date or None,
                           ayanamsha=ayanamsha)
        return get_dasha_periods(chart)
    except Exception as e:
        _raise(e)


@mcp.tool()
def get_strength_table_tool(
    dob: str,
    time: str,
    lat: float,
    lon: float,
    timezone: str,
    query_date: str = "",
    ayanamsha: str = "lahiri",
) -> Dict[str, Any]:
    """
    Per-planet strength table: Shadbala rupas + requirement + is_strong,
    Vimshopaka total + band, Sodhya Pinda.

    Drill-down for the compact chart's strengths section.

    Parameters: same birth details as cast_vedic_chart.
        ayanamsha: One of lahiri (default), lahiri_icrc, true_citra, raman,
            krishnamurti, krishnamurti_vp291, yukteshwar, fagan_bradley.
    """
    try:
        chart = cast_chart(dob, time, lat, lon, timezone, query_date or None,
                           ayanamsha=ayanamsha)
        return get_strength_table(chart)
    except Exception as e:
        _raise(e)


@mcp.tool()
def get_time_sensitivity_tool(
    dob: str,
    time: str,
    lat: float,
    lon: float,
    timezone: str,
    query_date: str = "",
    ayanamsha: str = "lahiri",
) -> Dict[str, Any]:
    """
    Birth-time sensitivity: how fragile this chart is to time uncertainty.

    Re-casts at +-4 minutes and reports what moves (Lagna sign/degree,
    Moon pada, houses, Vimshottari balance lord) with a verdict:
    robust (nothing structural moves), borderline (a cusp lies within
    one window of movement — twice the error would flip it), or fragile
    (a flip inside the window). Advise the user to verify birth time
    when the verdict is not robust.

    Parameters: same birth details as cast_vedic_chart.
    time accepts "HH:MM[:SS]".
        ayanamsha: One of lahiri (default), lahiri_icrc, true_citra, raman,
            krishnamurti, krishnamurti_vp291, yukteshwar, fagan_bradley.
    """
    try:
        return get_time_sensitivity(
            dob, time, lat, lon, timezone, query_date=query_date or None,
            ayanamsha=ayanamsha)
    except Exception as e:
        _raise(e)


@mcp.tool()
def get_yoga_list_tool(
    dob: str,
    time: str,
    lat: float,
    lon: float,
    timezone: str,
    query_date: str = "",
    ayanamsha: str = "lahiri",
) -> Dict[str, Any]:
    """
    Full yoga entries: name, formed_by planets, description.

    Drill-down for the compact chart's yoga names.

    Parameters: same birth details as cast_vedic_chart.
        ayanamsha: One of lahiri (default), lahiri_icrc, true_citra, raman,
            krishnamurti, krishnamurti_vp291, yukteshwar, fagan_bradley.
    """
    try:
        chart = cast_chart(dob, time, lat, lon, timezone, query_date or None,
                           ayanamsha=ayanamsha)
        return {"yogas": get_yoga_list(chart)}
    except Exception as e:
        _raise(e)


@mcp.tool()
def calculate_compatibility_tool(
    dob1: str, time1: str, lat1: float, lon1: float, tz1: str,
    dob2: str, time2: str, lat2: float, lon2: float, tz2: str,
    ayanamsha: str = "lahiri",
) -> Dict[str, Any]:
    """
    Calculates traditional 36-point Ashtakoot relationship compatibility between two people.
    By tradition, Person 1 (dob1) should be Male and Person 2 (dob2) should be Female for accurate points.

    Returns (JSON):
    - 8 Ashtakoot kutas (total 36 pts): Varna, Vashya, Tara, Yoni, Graha Maitri, Gana, Bhakoot, Nadi
    - Additional kutas: Mahendra, Stree Deergha, Vedha, Rajju (5-group nakshatra durability), BadConstellations, LagnaHouse7, SexEnergy
    - Exception logic: Nadi mitigated by Bhakoot+Rajju, Rajju mitigated by GrahaMaitri+Bhakoot+Tara+Mahendra
    - Kuja Dosha: per-person Mars/Saturn/Rahu/Ketu/Sun analysis in houses 2,4,7,8,12 with dignity-based scoring and compatibility verdict

    Parameters:
        dob1, time1, lat1, lon1, tz1: Birth details for Person 1 (e.g. "1990-04-15", "14:30")
        dob2, time2, lat2, lon2, tz2: Birth details for Person 2
        ayanamsha: One of lahiri (default), lahiri_icrc, true_citra, raman,
            krishnamurti, krishnamurti_vp291, yukteshwar, fagan_bradley.
    """
    try:
        return calculate_compatibility(
            dob1, time1, lat1, lon1, tz1,
            dob2, time2, lat2, lon2, tz2,
            ayanamsha=ayanamsha,
        )
    except Exception as e:
        _raise(e)


@mcp.tool()
def check_muhurtha_tool(
    activity: str,
    date: str,
    time: str,
    lat: float,
    lon: float,
    timezone: str,
    ayanamsha: str = "lahiri",
) -> Dict[str, Any]:
    """
    Check if a date/time is auspicious for a specific activity (electional astrology).

    Evaluates Panchang purity, nakshatra suitability, tithi, weekday, Lagna, and
    activity-specific doshas to determine muhurtha quality. 

    Returns (JSON):
    - `verdict`: "auspicious" / "mixed_favorable" / "mixed" / "inauspicious"
    - `score`: numeric score (positive*10 - negative*15)
    - `positive_factors`, `negative_factors`: specific reasons
    - `panchang_suddhi`: tithi/vara/nakshatra/yoga/karana assessment
    - `marriage_doshas` (marriage only): Sagraha, Shashtashta, Bhrigupta Shatka, Kujaasthama

    Parameters:
        activity: Type of activity — one of 'marriage', 'travel', 'business', 'education', 'house_entry', 'medical'
        date: Date to evaluate as "YYYY-MM-DD"
        time: Time to evaluate as "HH:MM" (24h format)
        lat: Location latitude
        lon: Location longitude
        timezone: IANA timezone string
        ayanamsha: One of lahiri (default), lahiri_icrc, true_citra, raman,
            krishnamurti, krishnamurti_vp291, yukteshwar, fagan_bradley.
    """
    try:
        return check_muhurtha(activity, date, time, lat, lon, timezone,
                              ayanamsha=ayanamsha)
    except Exception as e:
        _raise(e)


@mcp.tool()
def analyze_career_chart(
    dob: str,
    time: str,
    lat: float,
    lon: float,
    timezone: str,
    ayanamsha: str = "lahiri",
) -> Dict[str, Any]:
    """
    Analyze career potential using the 10th house, D10 Dashamsha, and planetary significations.

    Returns (JSON):
    - `tenth_house`: lord, sign, occupants, dignity, D10 sign
    - `d10_indicators`: planet-by-planet D10 placements with career domain significations
    - `career_themes`: ranked career domains derived from planetary + sign analysis
    - `strength_factors`: supporting indicators (6th/7th lord connections, etc.)

    Parameters:
        dob: Date of birth as "YYYY-MM-DD"
        time: Time of birth as "HH:MM" (24h)
        lat: Birth latitude
        lon: Birth longitude
        timezone: IANA timezone string
        ayanamsha: One of lahiri (default), lahiri_icrc, true_citra, raman,
            krishnamurti, krishnamurti_vp291, yukteshwar, fagan_bradley.
    """
    try:
        return analyze_career(dob, time, lat, lon, timezone,
                              ayanamsha=ayanamsha)
    except Exception as e:
        _raise(e)


def main():
    """Console entry point for `rishi-ai-mcp` command."""
    mcp.run()


if __name__ == "__main__":
    main()
