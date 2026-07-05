"""Tests for transcription utilities."""

from app.services.transcription.speaker_formatter import (
    assign_alternating_speakers,
    format_speaker_turns,
)
from app.models.schemas import TranscriptSegment


def test_alternating_speakers():
    raw = [
        {"start": 0, "end": 2, "text": "How are you?"},
        {"start": 2, "end": 5, "text": "I have pain."},
    ]
    segments = assign_alternating_speakers(raw)
    assert segments[0].speaker == "Doctor"
    assert segments[1].speaker == "Patient"


def test_format_speaker_turns():
    segments = [
        TranscriptSegment(start=0, end=2, text="Hello", speaker="Doctor"),
        TranscriptSegment(start=2, end=5, text="Hi doctor", speaker="Patient"),
    ]
    formatted = format_speaker_turns(segments, estimated=True)
    assert "Doctor:" in formatted
    assert "Patient:" in formatted
    assert "estimated" in formatted.lower()
