"""Transcription provider factory with graceful fallback."""

import logging

from app.core.config import get_settings
from app.services.transcription.azure_transcriber import AzureSpeechTranscriber
from app.services.transcription.base import TranscriptionProvider
from app.services.transcription.gcp_transcriber import GcpTranscriber
from app.services.transcription.whisper_transcriber import WhisperTranscriber

logger = logging.getLogger(__name__)
settings = get_settings()


def get_transcription_provider() -> TranscriptionProvider:
    provider = settings.effective_stt_provider

    if provider == "azure":
        try:
            return AzureSpeechTranscriber()
        except Exception as e:
            logger.warning("Azure STT unavailable, falling back to local: %s", e)
            return WhisperTranscriber()

    if provider == "gcp":
        try:
            return GcpTranscriber()
        except Exception as e:
            logger.warning("GCP STT unavailable, falling back to local: %s", e)
            return WhisperTranscriber()

    return WhisperTranscriber()
