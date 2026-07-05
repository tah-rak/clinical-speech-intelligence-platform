"""Tests for WER calculation and entity extraction."""

import pytest

from app.services.evaluation.wer import calculate_wer, normalize_text
from app.services.nlp.entity_extractor import EntityExtractor


def test_normalize_text():
    assert normalize_text("Hello, World!") == ["hello", "world"]


def test_wer_perfect_match():
    result = calculate_wer("the cat sat on the mat", "the cat sat on the mat")
    assert result["wer"] == 0.0
    assert result["substitutions"] == 0


def test_wer_with_errors():
    result = calculate_wer("the cat sat on the mat", "the dog sat on mat")
    assert result["wer"] > 0.0
    assert result["reference_word_count"] == 6


def test_wer_empty_reference():
    result = calculate_wer("", "hello world")
    assert result["wer"] == 1.0


def test_entity_extraction_symptoms():
    extractor = EntityExtractor()
    transcript = (
        "Patient reports chest pain and shortness of breath for 2 days. "
        "Takes lisinopril for hypertension. Allergic to penicillin. "
        "Order EKG and blood work. Follow up in one week."
    )
    entities = extractor.extract(transcript)
    assert len(entities.symptoms) > 0
    assert any("pain" in s.lower() or "breath" in s.lower() for s in entities.symptoms)


def test_entity_extraction_medications():
    extractor = EntityExtractor()
    transcript = "Patient takes ibuprofen and metformin daily."
    entities = extractor.extract(transcript)
    assert len(entities.medications) > 0
