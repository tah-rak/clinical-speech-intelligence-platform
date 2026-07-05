"""Local faster-whisper transcription provider."""

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


class WhisperTranscriber(TranscriptionProvider):
    def __init__(self) -> None:
        self._model = None

    def _load_model(self):
        if self._model is None:
            try:
                from faster_whisper import WhisperModel

                self._model = WhisperModel(
                    settings.WHISPER_MODEL,
                    device=settings.WHISPER_DEVICE,
                    compute_type=settings.WHISPER_COMPUTE_TYPE,
                )
            except ImportError:
                raise RuntimeError(
                    "faster-whisper is required for local transcription. "
                    "Install with: pip install faster-whisper"
                )
        return self._model

    async def transcribe(self, audio_path: Path) -> TranscriptionResult:
        start = time.time()
        model = self._load_model()

        segments_iter, info = model.transcribe(
            str(audio_path),
            beam_size=5,
            word_timestamps=False,
            vad_filter=True,
        )

        raw_segments: list[dict] = []
        texts: list[str] = []
        confidences: list[float] = []

        for seg in segments_iter:
            raw_segments.append(
                {
                    "start": seg.start,
                    "end": seg.end,
                    "text": seg.text.strip(),
                    "confidence": getattr(seg, "avg_logprob", None),
                }
            )
            texts.append(seg.text.strip())
            if hasattr(seg, "avg_logprob") and seg.avg_logprob is not None:
                confidences.append(float(seg.avg_logprob))

        segments = assign_alternating_speakers(raw_segments)
        transcript_text = " ".join(texts)
        formatted = format_speaker_turns(segments, estimated=True)
        elapsed = time.time() - start

        avg_conf = sum(confidences) / len(confidences) if confidences else None

        return TranscriptionResult(
            transcript_text=transcript_text,
            segments=segments,
            formatted_transcript=formatted,
            provider="local",
            processing_time_seconds=round(elapsed, 2),
            speaker_labels_estimated=True,
            confidence=round(avg_conf, 3) if avg_conf else None,
        )

    def get_provider_name(self) -> str:
        return "local"
