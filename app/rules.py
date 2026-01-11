from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .models import Duration, FeverTemp, MainSymptom, RiskFactor, Severity, TriageRequest


DISCLAIMER = (
    "Not medical advice. If symptoms are severe, rapidly worsening, or you feel unsafe, "
    "seek urgent care or call local emergency services."
)


CATEGORY_EMERGENCY = "Emergency now"
CATEGORY_URGENT = "Urgent today"
CATEGORY_SOON = "See a clinician soon (24–72h)"
CATEGORY_SELF = "Self-care / monitor"


RED_FLAG_LABELS = {
    "fainting_or_unresponsive": "Fainting or unresponsive",
    "severe_shortness_of_breath": "Severe shortness of breath",
    "blue_lips_face": "Blue lips/face",
    "new_confusion": "New confusion",
    "signs_of_stroke": "Possible stroke signs (face/arm/speech)",
    "uncontrolled_bleeding": "Uncontrolled bleeding",
    "seizure": "Seizure",
    "severe_allergic_reaction": "Severe allergic reaction (swelling + breathing trouble)",
}

RISK_LABELS = {
    "pregnant": "Pregnancy",
    "immunocompromised": "Immunocompromised",
    "serious_heart_lung_disease": "Serious heart/lung disease",
    "diabetes_kidney_disease": "Diabetes/kidney disease",
    "infant_under_3_months": "Infant under 3 months",
    "none": "None",
}


@dataclass(frozen=True)
class RuleResult:
    category: str
    reasons: List[str]


def _has_any_high_risk(risks: List[RiskFactor]) -> bool:
    return any(r != "none" for r in risks)


def _duration_label(d: Duration) -> str:
    return {
        "less_24h": "Less than 24 hours",
        "1_to_3_days": "1–3 days",
        "more_3_days": "More than 3 days",
    }[d]


def evaluate(req: TriageRequest) -> RuleResult:
    reasons: List[str] = []

    # Normalize "none" in risk_factors
    risk_factors = req.risk_factors or ["none"]
    if "none" in risk_factors and len(risk_factors) > 1:
        risk_factors = [r for r in risk_factors if r != "none"]

    # A) EMERGENCY NOW
    if req.red_flags:
        reasons.extend([f"Red flag: {RED_FLAG_LABELS[r]}" for r in req.red_flags])
        return RuleResult(CATEGORY_EMERGENCY, reasons)

    if req.main_symptom == "chest_pain" and req.severity == "severe":
        return RuleResult(CATEGORY_EMERGENCY, ["Severe chest pain"])

    if req.main_symptom == "breathing_trouble" and req.severity in ("moderate", "severe"):
        return RuleResult(CATEGORY_EMERGENCY, ["Breathing trouble with moderate/severe severity"])

    # B) URGENT TODAY
    if req.severity == "severe":
        return RuleResult(CATEGORY_URGENT, ["Severe symptom severity"])

    if req.main_symptom == "fever":
        ft: FeverTemp = req.fever_temp or "none_or_unknown"
        if ft == "39_5_or_more":
            return RuleResult(CATEGORY_URGENT, ["High fever (≥ 39.5°C)"])

        if ft in ("38_to_39_4", "39_5_or_more") and _has_any_high_risk(risk_factors):
            hr = ", ".join(RISK_LABELS[r] for r in risk_factors if r != "none")
            return RuleResult(CATEGORY_URGENT, [f"Fever with high-risk condition(s): {hr}"])

        if req.age_group == "under_2" and ft != "below_38" and ft != "none_or_unknown":
            return RuleResult(CATEGORY_URGENT, ["Fever in very young child (conservative rule)"])

    if req.duration == "more_3_days" and req.severity != "mild":
        return RuleResult(
            CATEGORY_URGENT,
            [f"Symptoms > 3 days with {req.severity} severity"],
        )

    # C) SEE CLINICIAN SOON (24–72h)
    if req.severity == "moderate" and req.duration != "less_24h":
        return RuleResult(
            CATEGORY_SOON,
            [f"Moderate symptoms lasting {_duration_label(req.duration)}"],
        )

    if _has_any_high_risk(risk_factors) and req.severity == "moderate":
        hr = ", ".join(RISK_LABELS[r] for r in risk_factors if r != "none")
        return RuleResult(CATEGORY_SOON, [f"Moderate symptoms with high-risk condition(s): {hr}"])

    if req.main_symptom in ("abdominal_pain", "headache", "vomiting_diarrhea") and req.duration != "less_24h":
        return RuleResult(
            CATEGORY_SOON,
            [f"{req.main_symptom.replace('_', ' ').title()} lasting {_duration_label(req.duration)}"],
        )

    # D) SELF-CARE / MONITOR
    return RuleResult(CATEGORY_SELF, ["No red flags detected and overall risk appears low"])
