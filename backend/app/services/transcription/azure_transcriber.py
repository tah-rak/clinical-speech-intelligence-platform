"""Azure AI Speech transcription provider (optional)."""

import logging
import time
from pathlib import Path

from app.core.config import get_settings
from app.models.schemas import TranscriptSegment, TranscriptionResult
from app.services.transcription.base import TranscriptionProvider
from app.services.transcription.speaker_formatter import (
    assign_alternating_speakers,
    format_speaker_turns,
)

logger = logging.getLogger(__name__)
settings = get_settings()


class AzureSpeechTranscriber(TranscriptionProvider):
    async def transcribe(self, audio_path: Path) -> TranscriptionResult:
        if not settings.AZURE_SPEECH_KEY or not settings.AZURE_SPEECH_REGION:
            raise RuntimeError("Azure Speech credentials not configured")

        start = time.time()
        try:
            import azure.cognitiveservices.speech as speechsdk
        except ImportError:
            raise RuntimeError(
                "azure-cognitiveservices-speech required. "
                "Install with: pip install azure-cognitiveservices-speech"
            )

        speech_config = speechsdk.SpeechConfig(
            subscription=settings.AZURE_SPEECH_KEY,
            region=settings.AZURE_SPEECH_REGION,
        )
        speech_config.speech_recognition_language = "en-US"

        audio_config = speechsdk.audio.AudioConfig(filename=str(audio_path))
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config, audio_config=audio_config
        )

        raw_segments: list[dict] = []
        done = False

        def recognized_cb(evt):
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                raw_segments.append(
                    {
                        "start": 0.0,
                        "end": 0.0,
                        "text": evt.result.text,
                        "confidence": None,
                    }
                )

        def stop_cb(evt):
            nonlocal done
            done = True

        recognizer.recognized.connect(recognized_cb)
        recognizer.session_stopped.connect(stop_cb)
        recognizer.canceled.connect(stop_cb)

        recognizer.start_continuous_recognition()
        while not done:
            time.sleep(0.1)
        recognizer.stop_continuous_recognition()

        segments = assign_alternating_speakers(raw_segments) if raw_segments else []
        transcript_text = " ".join(s["text"] for s in raw_segments)
        formatted = format_speaker_turns(segments, estimated=True)
        elapsed = time.time() - start

        return TranscriptionResult(
            transcript_text=transcript_text,
            segments=segments,
            formatted_transcript=formatted,
            provider="azure",
            processing_time_seconds=round(elapsed, 2),
            speaker_labels_estimated=True,
        )

    def get_provider_name(self) -> str:
        return "azure"
