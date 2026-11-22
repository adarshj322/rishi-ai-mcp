import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))

from chart_claims import check_claims

CHART = {
    "lagna": {"sign": "Aquarius"},
    "planets": {
        "Sun": {"sign": "Sagittarius", "house": 11},
        "Moon": {"sign": "Aries", "house": 3},
    },
}


def test_matching_sign_claim_is_clean():
    result = check_claims("The Sun is in Sagittarius.", CHART)
    assert result["contradictions"] == []
    assert result["checked"] == 1


def test_contradicting_sign_claim_is_flagged():
    result = check_claims("The Sun is in Leo.", CHART)
    assert result["contradictions"] == ["Sun in Leo (chart: Sagittarius)"]


def test_house_claim_contradiction():
    result = check_claims("The Moon is in the 7th house.", CHART)
    assert result["contradictions"] == ["Moon in house 7 (chart: house 3)"]


def test_lagna_and_sanskrit_sign():
    result = check_claims("Lagna is in Kumbha.", CHART)
    assert result["contradictions"] == []
    assert result["checked"] == 1


def test_aspect_phrase_is_not_a_claim():
    result = check_claims("The Sun aspects Mars in Aries.", CHART)
    assert result["checked"] == 0


def test_duplicate_claim_counted_once():
    result = check_claims("Sun in Sagittarius. Sun is in Sagittarius.", CHART)
    assert result["checked"] == 1


def test_d10_signs_are_scoped():
    chart = {
        "lagna": {"sign": "Aquarius", "d10_sign": "Aries"},
        "planets": {"Saturn": {"sign": "Libra", "d10_sign": "Capricorn"}},
    }
    result = check_claims("D10 Lagna Aries; 10th lord Saturn in Capricorn.", chart)
    assert result["contradictions"] == []
    assert result["checked"] == 2


def test_d10_mismatch_is_flagged():
    chart = {"planets": {"Saturn": {"sign": "Libra", "d10_sign": "Capricorn"}}}
    result = check_claims("D10 Saturn in Aquarius.", chart)
    assert result["contradictions"] == ["D10 Saturn in Aquarius (chart: Capricorn)"]


def test_transit_claim_uses_transit_block():
    chart = {
        "planets": {"Saturn": {"sign": "Leo"}},
        "transit": {"planets": {"Saturn": {"sign": "Pisces"}}},
    }
    result = check_claims("Transit Saturn in Pisces.", chart)
    assert result["contradictions"] == []
    assert result["checked"] == 1


def test_relative_house_is_skipped():
    chart = {"planets": {"Jupiter": {"sign": "Scorpio", "house": 2}}}
    result = check_claims("Jupiter in house 1 from Moon.", chart)
    assert result["checked"] == 0


def test_trailing_varga_makes_claim_ambiguous():
    chart = {"planets": {"Venus": {"sign": "Scorpio", "d10_sign": "Cancer"}}}
    result = check_claims(
        "Amatyakaraka Venus in Pisces, house 12, exalted, D10 Cancer.", chart
    )
    assert result["checked"] == 0


def test_from_lagna_is_not_a_lagna_claim():
    chart = {"lagna": {"sign": "Cancer"}}
    result = check_claims("6th from Cancer Lagna is Sagittarius.", chart)
    assert result["checked"] == 0


def test_d10_list_is_scoped():
    chart = {
        "lagna": {"sign": "Cancer", "d10_sign": "Aries"},
        "planets": {
            "Saturn": {"sign": "Libra", "d10_sign": "Capricorn"},
            "Venus": {"sign": "Cancer", "d10_sign": "Gemini"},
        },
    }
    result = check_claims(
        "D10 Lagna Aries; 10th lord Saturn in Capricorn; Venus in Gemini.", chart
    )
    assert result["contradictions"] == []
    assert result["checked"] == 3


def test_from_lagna_after_period_is_skipped():
    chart = {"lagna": {"sign": "Cancer"}}
    result = check_claims("Some ground. 6th from Cancer Lagna is Sagittarius.", chart)
    assert result["checked"] == 0
