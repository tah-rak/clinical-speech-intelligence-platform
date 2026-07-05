"""Transcription API routes."""

import logging
import time
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.schemas import TranscriptionResult
from app.models.visit import Visit
from app.services.storage import get_storage_provider
from app.services.transcription import get_transcription_provider
from app.utils.sample_data import load_sample_transcript, sample_transcript_to_segments

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/visits", tags=["transcription"])


@router.post("/{visit_id}/transcribe", response_model=TranscriptionResult)
async def transcribe_visit(
    visit_id: UUID,
    db: Session = Depends(get_db),
) -> TranscriptionResult:
    visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")

    if visit.transcript_text and visit.transcription_provider == "sample":
        segments_data = visit.transcript_segments or {}
        from app.models.schemas import TranscriptSegment

        segments = [
            TranscriptSegment(**s)
            for s in segments_data.get("segments", [])
        ]
        return TranscriptionResult(
            transcript_text=visit.transcript_text,
            segments=segments,
            formatted_transcript=segments_data.get("formatted", visit.transcript_text),
            provider="sample",
            processing_time_seconds=0.0,
            speaker_labels_estimated=False,
        )

    if not visit.audio_storage_uri:
        raise HTTPException(status_code=400, detail="No audio file for this visit")

    storage = get_storage_provider()
    audio_path = await storage.get_path(visit.audio_storage_uri)
    if not audio_path:
        raise HTTPException(status_code=400, detail="Audio file not found in storage")

    start = time.time()
    transcriber = get_transcription_provider()

    try:
        result = await transcriber.transcribe(audio_path)
    except Exception as e:
        logger.error("Transcription failed: %s", e)
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

    visit.transcript_text = result.transcript_text
    visit.transcript_segments = {
        "segments": [s.model_dump() for s in result.segments],
        "formatted": result.formatted_transcript,
    }
    visit.transcription_provider = result.provider
    visit.speaker_labels_estimated = result.speaker_labels_estimated
    visit.processing_time_seconds = (visit.processing_time_seconds or 0) + result.processing_time_seconds
    db.commit()

    return result
