from app.models import TriageRequest
from app.rules import CATEGORY_EMERGENCY, CATEGORY_SELF, CATEGORY_SOON, CATEGORY_URGENT, evaluate


def test_emergency_red_flag():
    req = TriageRequest(
        age_group="13_to_64",
        main_symptom="headache",
        severity="mild",
        red_flags=["signs_of_stroke"],
        fever_temp="none_or_unknown",
        duration="less_24h",
        risk_factors=["none"],
    )
    res = evaluate(req)
    assert res.category == CATEGORY_EMERGENCY
    assert any("Red flag" in r for r in res.reasons)


def test_urgent_high_fever():
    req = TriageRequest(
        age_group="13_to_64",
        main_symptom="fever",
        severity="moderate",
        red_flags=[],
        fever_temp="39_5_or_more",
        duration="less_24h",
        risk_factors=["none"],
    )
    res = evaluate(req)
    assert res.category == CATEGORY_URGENT


def test_soon_moderate_duration():
    req = TriageRequest(
        age_group="13_to_64",
        main_symptom="vomiting_diarrhea",
        severity="moderate",
        red_flags=[],
        fever_temp="none_or_unknown",
        duration="1_to_3_days",
        risk_factors=["none"],
    )
    res = evaluate(req)
    assert res.category == CATEGORY_SOON


def test_self_care_benign():
    req = TriageRequest(
        age_group="13_to_64",
        main_symptom="sore_throat_cough",
        severity="mild",
        red_flags=[],
        fever_temp="none_or_unknown",
        duration="less_24h",
        risk_factors=["none"],
    )
    res = evaluate(req)
    assert res.category == CATEGORY_SELF
