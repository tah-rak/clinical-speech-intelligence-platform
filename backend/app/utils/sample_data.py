"""Sample transcript loader for demo without audio."""

from pathlib import Path

def _find_sample_data_dir() -> Path:
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "sample_data" / "sample_transcript.txt"
        if candidate.exists():
            return parent / "sample_data"
    return Path(__file__).resolve().parents[3] / "sample_data"


SAMPLE_TRANSCRIPT_PATH = _find_sample_data_dir() / "sample_transcript.txt"


def load_sample_transcript() -> str:
    if SAMPLE_TRANSCRIPT_PATH.exists():
        return SAMPLE_TRANSCRIPT_PATH.read_text(encoding="utf-8")
    return """Doctor: Good morning. How are you feeling today?
Patient: I have had chest pain since yesterday. It gets worse when I walk.
Doctor: Any shortness of breath or nausea?
Patient: A little shortness of breath. No nausea. I take lisinopril for hypertension.
Doctor: Any allergies to medications?
Patient: I am allergic to penicillin.
Doctor: We should order an EKG and blood work. I will prescribe nitroglycerin as needed.
Patient: When should I follow up?
Doctor: Please return in one week or sooner if symptoms worsen."""


def sample_transcript_to_segments(text: str) -> list[dict]:
    segments: list[dict] = []
    time = 0.0
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        if ":" in line:
            speaker, content = line.split(":", 1)
            segments.append(
                {
                    "start": time,
                    "end": time + 5.0,
                    "text": content.strip(),
                    "speaker": speaker.strip(),
                    "confidence": 0.95,
                }
            )
            time += 5.5
    return segments
