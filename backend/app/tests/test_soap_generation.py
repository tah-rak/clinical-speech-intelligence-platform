"""Tests for SOAP note generation."""

import pytest

from app.models.schemas import MedicalEntities
from app.services.soap.template_generator import generate_template_soap


def test_template_soap_generation():
    entities = MedicalEntities(
        symptoms=["Chest Pain", "Shortness of Breath"],
        medications=["Lisinopril"],
        allergies=["Penicillin"],
        conditions=["Hypertension"],
        duration=["2 days"],
        tests_labs=["EKG"],
        follow_up=["in one week"],
    )
    soap = generate_template_soap(
        transcript="Patient has chest pain.",
        entities=entities,
        patient_name="John Doe",
        visit_reason="Chest pain",
    )
    assert soap.subjective
    assert soap.objective
    assert soap.assessment
    assert soap.plan
    assert soap.generator == "template"
    assert "John Doe" in soap.subjective
    assert "Chest Pain" in soap.subjective or "chest pain" in soap.subjective.lower()
