"""Tests for plug-and-play LLM module."""

from app.services.llm.presets import PROVIDER_PRESETS, list_preset_names
from app.services.llm.utils import parse_json_content


def test_list_presets_includes_openai():
    names = list_preset_names()
    assert "openai" in names
    assert "groq" in names
    assert "custom" in names


def test_openai_preset_has_base_url():
    preset = PROVIDER_PRESETS["openai"]
    assert "openai.com" in preset.base_url
    assert preset.default_model


def test_parse_json_plain():
    result = parse_json_content('{"subjective": "test", "plan": "rest"}')
    assert result["subjective"] == "test"


def test_parse_json_fenced():
    text = '```json\n{"assessment": "stable"}\n```'
    result = parse_json_content(text)
    assert result["assessment"] == "stable"
