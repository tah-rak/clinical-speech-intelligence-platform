"""Audio file utilities."""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def get_audio_duration_seconds(file_path: Path) -> float | None:
    try:
        import mutagen

        audio = mutagen.File(str(file_path))
        if audio and audio.info:
            return float(audio.info.length)
    except Exception:
        pass

    try:
        import wave

        if file_path.suffix.lower() == ".wav":
            with wave.open(str(file_path), "rb") as wf:
                frames = wf.getnframes()
                rate = wf.getframerate()
                return frames / float(rate)
    except Exception as e:
        logger.debug("Could not read wav duration: %s", e)

    return None


def get_file_size_bytes(file_path: Path) -> int | None:
    try:
        return file_path.stat().st_size
    except Exception:
        return None
