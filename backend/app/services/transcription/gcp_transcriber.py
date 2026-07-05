"""GCP Speech-to-Text transcription provider (optional)."""

import logging
import time
from pathlib import Path

from app.core.config import get_settings
from app.models.schemas import TranscriptionResult
from app.services.transcription.base import TranscriptionProvider
from app.services.transcription.speaker_formatter import (
    assign_alternating_speakers,
    format_speaker_turns,
)

logger = logging.getLogger(__name__)
settings = get_settings()


class GcpTranscriber(TranscriptionProvider):
    async def transcribe(self, audio_path: Path) -> TranscriptionResult:
        if not settings.GCP_ENABLED:
            raise RuntimeError("GCP is not enabled")

        start = time.time()
        try:
            from google.cloud import speech_v1 as speech
        except ImportError:
            raise RuntimeError(
                "google-cloud-speech required. "
                "Install with: pip install google-cloud-speech"
            )

        client = speech.SpeechClient()
        content = audio_path.read_bytes()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_automatic_punctuation=True,
        )

        response = client.recognize(config=config, audio=audio)
        raw_segments: list[dict] = []

        for result in response.results:
            alt = result.alternatives[0]
            raw_segments.append(
                {
                    "start": 0.0,
                    "end": 0.0,
                    "text": alt.transcript,
                    "confidence": alt.confidence,
                }
            )

        segments = assign_alternating_speakers(raw_segments) if raw_segments else []
        transcript_text = " ".join(s["text"] for s in raw_segments)
        formatted = format_speaker_turns(segments, estimated=True)
        elapsed = time.time() - start

        return TranscriptionResult(
            transcript_text=transcript_text,
            segments=segments,
            formatted_transcript=formatted,
            provider="gcp",
            processing_time_seconds=round(elapsed, 2),
            speaker_labels_estimated=True,
        )

    def get_provider_name(self) -> str:
        return "gcp"
