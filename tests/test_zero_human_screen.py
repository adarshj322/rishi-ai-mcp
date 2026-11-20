import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))

from zero_human_screen import chart_text_divergence, shift_birth


def test_a1_flags_fabricated_degree():
    chart = {"planets": {"Sun": {"degree": 10.0}}}
    result = chart_text_divergence("The Sun is at 99.99°.", "The Sun is at 10.0°.", chart)
    assert result["real_fabrications"] == ["99.99°"]


def test_a2_fails_identical_texts():
    chart = {"planets": {"Sun": {"degree": 10.0}}}
    text = "The Sun is at 10.0°."
    result = chart_text_divergence(text, text, chart)
    assert result["claim_overlap"] == 1.0
    assert result["pass"] is False


def test_a2_passes_when_decoy_diverges():
    chart = {"planets": {"Sun": {"degree": 10.0}}}
    result = chart_text_divergence(
        "The Sun is at 10.0°.", "The Sun is at 22.0° and the Moon is at 5.0°.", chart
    )
    assert result["pass"] is True


def test_shift_birth_changes_time():
    assert (
        shift_birth(
            {"dob": "2000-01-01", "time": "04:20", "lat": 0, "lon": 0, "tz": "UTC"}
        )["time"]
        == "16:20"
    )
