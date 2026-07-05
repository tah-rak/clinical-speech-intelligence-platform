"""Utilities for parsing LLM JSON responses."""

import json
import re


def parse_json_content(text: str) -> dict:
    """Parse JSON from model output, including fenced code blocks."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    return json.loads(cleaned)
