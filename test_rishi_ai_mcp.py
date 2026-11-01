"""
Test Suite for RishiAI MCP Server
==================================
Tests the thin MCP wrapper that delegates to the DashaFlow library.
Validates that each MCP tool function returns valid JSON with expected structure.
"""

import unittest
import json

from rishi_ai_mcp import (
    cast_vedic_chart,
    cast_transit_chart,
    calculate_compatibility_tool,
    check_muhurtha_tool,
    analyze_career_chart,
)


class TestCastVedicChart(unittest.TestCase):
    """Test the cast_vedic_chart MCP tool."""

    def test_returns_valid_json(self):
        result = cast_vedic_chart("1990-04-15", "14:30", 28.6139, 77.2090, "Asia/Kolkata")
        data = result
        self.assertNotIn("error", data)

    def test_has_all_top_level_keys(self):
        result = cast_vedic_chart("1990-04-15", "14:30", 28.6139, 77.2090, "Asia/Kolkata",
                                  detail="full")
        data = result
        for key in ["metadata", "panchang", "lagna", "planets", "dashas", "yogas",
                     "ashtakavarga", "jaimini_karakas", "shadbala",
                     "bhava_chalit", "avasthas", "kaal_sarpa", "graha_yuddha",
                     "gandanta", "arudha_padas", "upapada", "karakamsha"]:
            self.assertIn(key, data, f"Missing top-level key: {key}")

    def test_all_nine_planets(self):
        result = cast_vedic_chart("1990-04-15", "14:30", 28.6139, 77.2090, "Asia/Kolkata")
        data = result
        for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
            self.assertIn(planet, data["planets"])

    def test_invalid_date_returns_error(self):
        from mcp.server.fastmcp.exceptions import ToolError
        with self.assertRaises(ToolError):
            cast_vedic_chart("bad-date", "14:30", 28.6139, 77.2090, "Asia/Kolkata")

    def test_invalid_timezone_returns_error(self):
        from mcp.server.fastmcp.exceptions import ToolError
        with self.assertRaises(ToolError):
            cast_vedic_chart("1990-04-15", "14:30", 28.6139, 77.2090, "Bogus/Zone")

    def test_invalid_lat_returns_error(self):
        from mcp.server.fastmcp.exceptions import ToolError
        with self.assertRaises(ToolError):
            cast_vedic_chart("1990-04-15", "14:30", 999.0, 77.2090, "Asia/Kolkata")

    def test_query_date_parameter(self):
        result = cast_vedic_chart("1990-04-15", "14:30", 28.6139, 77.2090, "Asia/Kolkata", "2025-06-15")
        data = result
        self.assertNotIn("error", data)
        self.assertIn("dashas", data)

    def test_bvr_chart_lagna_capricorn(self):
        result = cast_vedic_chart("1918-10-16", "14:20", 12.9716, 77.5946, "Asia/Kolkata")
        data = result
        self.assertEqual(data["lagna"]["sign"], "Capricorn")


class TestCastTransitChart(unittest.TestCase):
    """Test the cast_transit_chart MCP tool."""

    def test_returns_valid_json(self):
        result = cast_transit_chart("2025-06-15", "1990-04-15", "14:30", 28.6139, 77.2090, "Asia/Kolkata")
        data = result
        self.assertNotIn("error", data)

    def test_has_planets_and_sade_sati(self):
        result = cast_transit_chart("2025-06-15", "1990-04-15", "14:30", 28.6139, 77.2090, "Asia/Kolkata")
        data = result
        self.assertIn("planets", data)
        self.assertIn("sade_sati", data)
        self.assertIn("rahu_ketu_axis", data)

    def test_transit_planet_fields(self):
        result = cast_transit_chart("2025-06-15", "1990-04-15", "14:30", 28.6139, 77.2090, "Asia/Kolkata")
        data = result
        for name, pdata in data["planets"].items():
            self.assertIn("sign", pdata)
            self.assertIn("degree", pdata)
            self.assertIn("house_from_lagna", pdata)

    def test_invalid_date_returns_error(self):
        from mcp.server.fastmcp.exceptions import ToolError
        with self.assertRaises(ToolError):
            cast_transit_chart("not-a-date", "1990-04-15", "14:30", 28.6139, 77.2090, "Asia/Kolkata")

    def test_invalid_dob_returns_error(self):
        from mcp.server.fastmcp.exceptions import ToolError
        with self.assertRaises(ToolError):
            cast_transit_chart("2025-06-15", "not-a-date", "14:30", 28.6139, 77.2090, "Asia/Kolkata")


class TestCalculateCompatibility(unittest.TestCase):
    """Test the calculate_compatibility MCP tool."""

    def test_returns_valid_json(self):
        result = calculate_compatibility_tool(
            "1990-04-15", "14:30", 28.6139, 77.2090, "Asia/Kolkata",
            "1992-08-20", "10:00", 19.076, 72.8777, "Asia/Kolkata",
        )
        data = result
        self.assertNotIn("error", data)

    def test_has_scores_and_total(self):
        result = calculate_compatibility_tool(
            "1990-04-15", "14:30", 28.6139, 77.2090, "Asia/Kolkata",
            "1992-08-20", "10:00", 19.076, 72.8777, "Asia/Kolkata",
        )
        data = result
        self.assertIn("total_score", data)
        self.assertIn("scores", data)
        self.assertIn("kuja_dosha", data)

    def test_total_in_range(self):
        result = calculate_compatibility_tool(
            "1990-04-15", "14:30", 28.6139, 77.2090, "Asia/Kolkata",
            "1992-08-20", "10:00", 19.076, 72.8777, "Asia/Kolkata",
        )
        data = result
        self.assertGreaterEqual(data["total_score"], 0)
        self.assertLessEqual(data["total_score"], 36)

    def test_invalid_input_returns_error(self):
        from mcp.server.fastmcp.exceptions import ToolError
        with self.assertRaises(ToolError):
            calculate_compatibility_tool(
                "bad", "14:30", 28.6139, 77.2090, "Asia/Kolkata",
                "1992-08-20", "10:00", 19.076, 72.8777, "Asia/Kolkata",
            )


class TestCheckMuhurtha(unittest.TestCase):
    """Test the check_muhurtha MCP tool."""

    def test_returns_valid_json(self):
        result = check_muhurtha_tool("marriage", "2025-06-15", "10:00", 28.6139, 77.2090, "Asia/Kolkata")
        data = result
        self.assertNotIn("error", data)

    def test_has_verdict_and_score(self):
        result = check_muhurtha_tool("business", "2025-06-15", "10:00", 28.6139, 77.2090, "Asia/Kolkata")
        data = result
        self.assertIn("verdict", data)
        self.assertIn("score", data)
        self.assertIn(data["verdict"], ["auspicious", "mixed_favorable", "mixed", "inauspicious"])

    def test_invalid_activity_returns_error(self):
        from mcp.server.fastmcp.exceptions import ToolError
        with self.assertRaises(ToolError):
            check_muhurtha_tool("swimming", "2025-06-15", "10:00", 28.6139, 77.2090, "Asia/Kolkata")

    def test_invalid_date_returns_error(self):
        from mcp.server.fastmcp.exceptions import ToolError
        with self.assertRaises(ToolError):
            check_muhurtha_tool("travel", "bad-date", "10:00", 28.6139, 77.2090, "Asia/Kolkata")


class TestAnalyzeCareerChart(unittest.TestCase):
    """Test the analyze_career_chart MCP tool."""

    def test_returns_valid_json(self):
        result = analyze_career_chart("1990-04-15", "14:30", 28.6139, 77.2090, "Asia/Kolkata")
        data = result
        self.assertNotIn("error", data)

    def test_has_career_keys(self):
        result = analyze_career_chart("1990-04-15", "14:30", 28.6139, 77.2090, "Asia/Kolkata")
        data = result
        for key in ["tenth_house", "d10_indicators", "career_themes", "strength_factors"]:
            self.assertIn(key, data)

    def test_invalid_input_returns_error(self):
        from mcp.server.fastmcp.exceptions import ToolError
        with self.assertRaises(ToolError):
            analyze_career_chart("bad", "14:30", 28.6139, 77.2090, "Asia/Kolkata")


class TestCompactDetail(unittest.TestCase):
    """Slice 1: compact-by-default payloads."""

    def test_cast_chart_compact_default(self):
        result = cast_vedic_chart("1990-04-15", "14:30", 28.6139, 77.2090, "Asia/Kolkata")
        size = len(json.dumps(result).encode("utf-8"))
        self.assertLess(size, 4096, f"compact chart is {size} bytes")

    def test_cast_chart_full_detail(self):
        result = cast_vedic_chart("1990-04-15", "14:30", 28.6139, 77.2090,
                                  "Asia/Kolkata", detail="full")
        for key in ("planets", "dashas", "shadbala", "vimshopaka"):
            self.assertIn(key, result)

    def test_get_dasha_periods_tool(self):
        from rishi_ai_mcp import get_dasha_periods_tool
        result = get_dasha_periods_tool("1990-04-15", "14:30", 28.6139, 77.2090,
                                        "Asia/Kolkata")
        self.assertIn("vimshottari", result)
        self.assertIn("yogini", result)
        self.assertIn("chara", result)


class TestStructuredErrors(unittest.TestCase):
    """Slice 1: errors raise ToolError instead of returning data."""

    def test_invalid_date_raises_tool_error(self):
        from mcp.server.fastmcp.exceptions import ToolError
        with self.assertRaises(ToolError):
            cast_vedic_chart("bad-date", "14:30", 28.6139, 77.2090, "Asia/Kolkata")


class TestDetailValidationUpfront(unittest.TestCase):
    """Invalid detail must fail before paying for a full chart cast."""

    def test_invalid_detail_does_not_cast_chart(self):
        import rishi_ai_mcp
        from mcp.server.fastmcp.exceptions import ToolError
        calls = []
        orig = rishi_ai_mcp.cast_chart
        rishi_ai_mcp.cast_chart = lambda *a, **k: (calls.append(1), orig(*a, **k))[1]
        try:
            with self.assertRaises(ToolError):
                cast_vedic_chart("1990-04-15", "14:30", 28.6139, 77.2090,
                                 "Asia/Kolkata", detail="bogus")
        finally:
            rishi_ai_mcp.cast_chart = orig
        self.assertEqual(calls, [], "cast_chart ran before detail validation")


if __name__ == "__main__":
    unittest.main()
