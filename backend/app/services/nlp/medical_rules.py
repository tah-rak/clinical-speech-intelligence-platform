"""Rule-based medical entity patterns."""

import re

SYMPTOM_KEYWORDS = [
    "pain", "ache", "fever", "cough", "nausea", "vomiting", "headache",
    "fatigue", "dizziness", "shortness of breath", "chest pain", "swelling",
    "rash", "numbness", "weakness", "sore throat", "congestion", "chills",
    "diarrhea", "constipation", "insomnia", "anxiety", "depression",
]

MEDICATION_PATTERNS = [
    r"\b(?:take|prescribe|prescribed|start|started|on)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*(?:\d+\s*mg)?",
    r"\b([a-z]+(?:pril|olol|statin|mycin|cillin|azole|pam|pine))\b",
    r"\b(ibuprofen|acetaminophen|aspirin|metformin|lisinopril|atorvastatin|amoxicillin|omeprazole|levothyroxine|albuterol|prednisone|gabapentin|sertraline|amlodipine)\b",
]

ALLERGY_KEYWORDS = ["allergic", "allergy", "allergies", "anaphylaxis", "reaction to"]

CONDITION_KEYWORDS = [
    "diabetes", "hypertension", "asthma", "copd", "heart disease",
    "arthritis", "depression", "anxiety", "cancer", "stroke",
    "kidney disease", "liver disease", "obesity", "hypothyroidism",
]

DURATION_PATTERNS = [
    r"\b(?:for|since|about|approximately)\s+(\d+\s*(?:days?|weeks?|months?|years?|hours?))\b",
    r"\b(\d+\s*(?:days?|weeks?|months?|years?))\s+(?:ago|now)\b",
    r"\b(last|past)\s+(\d+\s*(?:days?|weeks?|months?))\b",
]

TEST_KEYWORDS = [
    "blood test", "lab work", "x-ray", "xray", "mri", "ct scan", "ultrasound",
    "ekg", "ecg", "cbc", "bmp", "lipid panel", "urinalysis", "biopsy",
]

DIAGNOSIS_PATTERNS = [
    r"\b(?:diagnos(?:is|ed)|impression|likely|suspect(?:ing)?|consistent with)\s+(?:with\s+)?([^.]+)",
    r"\b(?:appears to be|probably)\s+([^.]+)",
]

TREATMENT_KEYWORDS = [
    "prescribe", "recommend", "treatment", "therapy", "medication",
    "rest", "fluids", "ice", "heat", "physical therapy", "referral",
]

FOLLOWUP_PATTERNS = [
    r"\b(?:follow[- ]?up|return|come back|see (?:me|us) again)\s+(?:in\s+)?([^.]+)",
    r"\b(?:schedule|book)\s+(?:a\s+)?(?:appointment|visit)\s+([^.]+)?",
]


def extract_by_keywords(text: str, keywords: list[str]) -> list[str]:
    text_lower = text.lower()
    found: list[str] = []
    for kw in keywords:
        if kw.lower() in text_lower:
            found.append(kw.title() if kw.islower() else kw)
    return list(dict.fromkeys(found))


def extract_by_patterns(text: str, patterns: list[str]) -> list[str]:
    found: list[str] = []
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            groups = [g.strip() for g in match.groups() if g and g.strip()]
            if groups:
                found.extend(groups)
            else:
                found.append(match.group(0).strip())
    return list(dict.fromkeys(found))
