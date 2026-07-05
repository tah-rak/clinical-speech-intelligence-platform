"""Speaker turn formatting utilities."""

from app.models.schemas import TranscriptSegment


def format_speaker_turns(
    segments: list[TranscriptSegment],
    estimated: bool = True,
) -> str:
    """Format transcript segments into doctor/patient conversation blocks."""
    if not segments:
        return ""

    lines: list[str] = []
    current_speaker: str | None = None
    current_text: list[str] = []

    for seg in segments:
        speaker = seg.speaker or "Speaker"
        if speaker != current_speaker:
            if current_speaker and current_text:
                lines.append(f"{current_speaker}: {' '.join(current_text)}")
            current_speaker = speaker
            current_text = [seg.text.strip()]
        else:
            current_text.append(seg.text.strip())

    if current_speaker and current_text:
        lines.append(f"{current_speaker}: {' '.join(current_text)}")

    result = "\n\n".join(lines)
    if estimated:
        result = (
            "[Speaker labels are estimated based on transcript segments]\n\n" + result
        )
    return result


def assign_alternating_speakers(segments: list[dict]) -> list[TranscriptSegment]:
    """Assign Doctor/Patient labels by alternating segments."""
    result: list[TranscriptSegment] = []
    speakers = ["Doctor", "Patient"]

    for i, seg in enumerate(segments):
        speaker = speakers[i % 2]
        result.append(
            TranscriptSegment(
                start=seg.get("start", 0.0),
                end=seg.get("end", 0.0),
                text=seg.get("text", ""),
                speaker=speaker,
                confidence=seg.get("confidence"),
            )
        )
    return result
