"""Transcription provider interface."""

from abc import ABC, abstractmethod
from pathlib import Path

from app.models.schemas import TranscriptionResult


class TranscriptionProvider(ABC):
    @abstractmethod
    async def transcribe(self, audio_path: Path) -> TranscriptionResult:
        """Transcribe audio file."""

    @abstractmethod
    def get_provider_name(self) -> str:
        """Return provider identifier."""
