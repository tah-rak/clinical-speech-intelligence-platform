"""Medical entity extraction service."""

import logging
import re

from app.models.schemas import MedicalEntities
from app.services.nlp.medical_rules import (
    ALLERGY_KEYWORDS,
    CONDITION_KEYWORDS,
    DIAGNOSIS_PATTERNS,
    DURATION_PATTERNS,
    FOLLOWUP_PATTERNS,
    MEDICATION_PATTERNS,
    SYMPTOM_KEYWORDS,
    TEST_KEYWORDS,
    TREATMENT_KEYWORDS,
    extract_by_keywords,
    extract_by_patterns,
)

logger = logging.getLogger(__name__)

_nlp_model = None


def _load_spacy():
    global _nlp_model
    if _nlp_model is not None:
        return _nlp_model
    try:
        import spacy

        try:
            _nlp_model = spacy.load("en_core_sci_sm")
        except OSError:
            try:
                _nlp_model = spacy.load("en_core_web_sm")
            except OSError:
                _nlp_model = None
    except ImportError:
        _nlp_model = None
    return _nlp_model


def _extract_spacy_entities(text: str) -> dict[str, list[str]]:
    nlp = _load_spacy()
    if nlp is None:
        return {}

    doc = nlp(text)
    results: dict[str, list[str]] = {
        "medications": [],
        "conditions": [],
        "symptoms": [],
    }

    for ent in doc.ents:
        label = ent.label_.upper()
        value = ent.text.strip()
        if label in ("DRUG", "CHEMICAL"):
            results["medications"].append(value)
        elif label in ("DISEASE", "DISORDER"):
            results["conditions"].append(value)
        elif label in ("SIGN_SYMPTOM",):
            results["symptoms"].append(value)

    return results


class EntityExtractor:
    def extract(self, transcript: str) -> MedicalEntities:
        if not transcript or not transcript.strip():
            return MedicalEntities()

        spacy_entities = _extract_spacy_entities(transcript)

        symptoms = extract_by_keywords(transcript, SYMPTOM_KEYWORDS)
        symptoms.extend(spacy_entities.get("symptoms", []))

        medications = extract_by_patterns(transcript, MEDICATION_PATTERNS)
        medications.extend(spacy_entities.get("medications", []))

        allergies: list[str] = []
        for kw in ALLERGY_KEYWORDS:
            if kw.lower() in transcript.lower():
                idx = transcript.lower().find(kw.lower())
                snippet = transcript[idx : idx + 80]
                allergies.append(snippet.strip())

        conditions = extract_by_keywords(transcript, CONDITION_KEYWORDS)
        conditions.extend(spacy_entities.get("conditions", []))

        duration = extract_by_patterns(transcript, DURATION_PATTERNS)
        tests = extract_by_keywords(transcript, TEST_KEYWORDS)
        diagnosis = extract_by_patterns(transcript, DIAGNOSIS_PATTERNS)
        treatment = extract_by_keywords(transcript, TREATMENT_KEYWORDS)
        follow_up = extract_by_patterns(transcript, FOLLOWUP_PATTERNS)

        return MedicalEntities(
            symptoms=_dedupe(symptoms),
            medications=_dedupe(medications),
            allergies=_dedupe(allergies)[:5],
            conditions=_dedupe(conditions),
            duration=_dedupe(duration),
            tests_labs=_dedupe(tests),
            diagnosis=_dedupe(diagnosis),
            treatment_plan=_dedupe(treatment),
            follow_up=_dedupe(follow_up),
        )


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        key = item.lower().strip()
        if key and key not in seen and len(key) > 2:
            seen.add(key)
            result.append(item.strip())
    return result
