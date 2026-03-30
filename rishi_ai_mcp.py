"""
RishiAI MCP Server — Vedic astrology tools via the Model Context Protocol.

Thin wrapper around the DashaFlow library. Exposes 5 tools:
  cast_vedic_chart, cast_transit_chart, calculate_compatibility_tool,
  check_muhurtha_tool, analyze_career_chart.

Install:  pip install rishi-ai-mcp
Run:      rishi-ai-mcp            (console entry-point)
  or:     python rishi_ai_mcp.py  (direct)
"""

import json
from mcp.server.fastmcp import FastMCP
from dashaflow import (
    cast_chart,
    cast_transit,
    calculate_compatibility,
    check_muhurtha,
    analyze_career,
)

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
) -> str:
    """
    Calculate a complete Vedic birth chart (Sidereal Lahiri ayanamsha).

    Returns planetary positions with sign, house, nakshatra, pada, dignity,
    combustion, retrograde status, Navamsha (D9), Dashamsha (D10), aspects,
    Vimshottari Dasha periods, detected yogas, and Panchang elements.

    Parameters:
        dob: Date of birth as "YYYY-MM-DD" (e.g. "1990-04-15")
        time: Time of birth as "HH:MM" in 24-hour format (e.g. "14:30")
        lat: Birth latitude as decimal degrees (e.g. 28.6139 for New Delhi)
        lon: Birth longitude as decimal degrees (e.g. 77.2090 for New Delhi)
        timezone: IANA timezone string (e.g. "Asia/Kolkata", "America/New_York")
        query_date: Optional date for Dasha lookup as "YYYY-MM-DD". Defaults to today.
    """
    try:
        result = cast_chart(dob, time, lat, lon, timezone, query_date or None)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def cast_transit_chart(
    transit_date: str,
    natal_chart_json: str,
    timezone: str = "Asia/Kolkata",
) -> str:
    """
    Calculate planetary transits for a given date overlaid on a natal chart.

    Returns each transit planet's current sign, nakshatra, house from natal Lagna,
    house from natal Moon, Sade Sati status, and Rahu-Ketu transit axis.

    IMPORTANT: You must call cast_vedic_chart first and pass its FULL JSON output
    as the natal_chart_json parameter.

    Parameters:
        transit_date: The date to compute transits for as "YYYY-MM-DD" (e.g. "2026-02-28")
        natal_chart_json: The FULL JSON string output from a previous cast_vedic_chart call
        timezone: IANA timezone string (defaults to "Asia/Kolkata")
    """
    try:
        natal_chart = json.loads(natal_chart_json)
        result = cast_transit(transit_date, natal_chart, timezone)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def calculate_compatibility_tool(
    dob1: str, time1: str, lat1: float, lon1: float, tz1: str,
    dob2: str, time2: str, lat2: float, lon2: float, tz2: str,
) -> str:
    """
    Calculates traditional 36-point Ashtakoot relationship compatibility between two people.
    By tradition, Person 1 (dob1) should be Male and Person 2 (dob2) should be Female for accurate points.

    Returns the score breakdown (Varna, Vashya, Tara, Yoni, Graha Maitri, Gana, Bhakoot, Nadi),
    additional kutas (Mahendra, Stree Deergha, Vedha), Kuja Dosha analysis,
    and the total score out of 36.

    Parameters:
        dob1, time1, lat1, lon1, tz1: Birth details for Person 1 (e.g. "1990-04-15", "14:30")
        dob2, time2, lat2, lon2, tz2: Birth details for Person 2
    """
    try:
        result = calculate_compatibility(
            dob1, time1, lat1, lon1, tz1,
            dob2, time2, lat2, lon2, tz2,
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def check_muhurtha_tool(
    activity: str,
    date: str,
    time: str,
    lat: float,
    lon: float,
    timezone: str,
) -> str:
    """
    Check if a date/time is auspicious for a specific activity (electional astrology).

    Evaluates Panchang purity, nakshatra suitability, tithi, weekday, Lagna, and
    activity-specific doshas to determine muhurtha quality.

    Parameters:
        activity: Type of activity — one of 'marriage', 'travel', 'business', 'education', 'house_entry', 'medical'
        date: Date to evaluate as "YYYY-MM-DD"
        time: Time to evaluate as "HH:MM" (24h format)
        lat: Location latitude
        lon: Location longitude
        timezone: IANA timezone string
    """
    try:
        result = check_muhurtha(activity, date, time, lat, lon, timezone)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def analyze_career_chart(
    dob: str,
    time: str,
    lat: float,
    lon: float,
    timezone: str,
) -> str:
    """
    Analyze career potential using the 10th house, D10 Dashamsha, and planetary significations.

    Returns career themes, strength factors, D10 planet analysis, and domain recommendations
    based on the 10th house lord, occupants, dignity, and D10 divisional chart.

    Parameters:
        dob: Date of birth as "YYYY-MM-DD"
        time: Time of birth as "HH:MM" (24h)
        lat: Birth latitude
        lon: Birth longitude
        timezone: IANA timezone string
    """
    try:
        result = analyze_career(dob, time, lat, lon, timezone)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


def main():
    """Console entry point for `rishi-ai-mcp` command."""
    mcp.run()


if __name__ == "__main__":
    main()
