from __future__ import annotations

from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


AgeGroup = Literal["under_2", "2_to_12", "13_to_64", "65_plus"]
MainSymptom = Literal[
    "chest_pain",
    "breathing_trouble",
    "abdominal_pain",
    "fever",
    "headache",
    "vomiting_diarrhea",
    "sore_throat_cough",
    "rash",
]
Severity = Literal["mild", "moderate", "severe"]

RedFlag = Literal[
    "fainting_or_unresponsive",
    "severe_shortness_of_breath",
    "blue_lips_face",
    "new_confusion",
    "signs_of_stroke",
    "uncontrolled_bleeding",
    "seizure",
    "severe_allergic_reaction",
]

FeverTemp = Literal["none_or_unknown", "below_38", "38_to_39_4", "39_5_or_more"]

Duration = Literal["less_24h", "1_to_3_days", "more_3_days"]

RiskFactor = Literal[
    "pregnant",
    "immunocompromised",
    "serious_heart_lung_disease",
    "diabetes_kidney_disease",
    "infant_under_3_months",
    "none",
]


class TriageRequest(BaseModel):
    age_group: AgeGroup
    main_symptom: MainSymptom
    severity: Severity

    red_flags: List[RedFlag] = Field(default_factory=list)

    fever_temp: Optional[FeverTemp] = "none_or_unknown"
    duration: Duration

    risk_factors: List[RiskFactor] = Field(default_factory=lambda: ["none"])


class TriageResponse(BaseModel):
    category: Literal[
        "Emergency now",
        "Urgent today",
        "See a clinician soon (24–72h)",
        "Self-care / monitor",
    ]
    reasons: List[str]
    disclaimer: str
    version: str
    timestamp: datetime
