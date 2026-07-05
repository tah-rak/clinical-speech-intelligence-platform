"""Upload API routes."""

import logging
from datetime import date
from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.schemas import UploadResponse, VisitResponse
from app.models.visit import Visit
from app.services.storage import get_storage_provider
from app.utils.audio import get_audio_duration_seconds
from app.utils.sample_data import load_sample_transcript, sample_transcript_to_segments

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/uploads", tags=["uploads"])

ALLOWED_EXTENSIONS = {".wav", ".mp3", ".m4a"}


@router.post("", response_model=UploadResponse)
async def upload_visit(
    patient_name: str = Form(...),
    clinician_name: str = Form(...),
    visit_date: date = Form(...),
    visit_reason: str | None = Form(None),
    use_sample_transcript: bool = Form(False),
    audio: UploadFile | None = File(None),
    db: Session = Depends(get_db),
) -> UploadResponse:
    visit = Visit(
        patient_name=patient_name,
        clinician_name=clinician_name,
        visit_date=visit_date,
        visit_reason=visit_reason,
        status="draft",
    )
    db.add(visit)
    db.flush()

    storage = get_storage_provider()
    visit.storage_provider = storage.get_provider_name()

    file_size: int | None = None
    duration: float | None = None

    if use_sample_transcript:
        sample_text = load_sample_transcript()
        segments = sample_transcript_to_segments(sample_text)
        visit.transcript_text = " ".join(
            s["text"] for s in segments
        )
        visit.transcript_segments = {
            "segments": segments,
            "formatted": sample_text,
            "speaker_labels_estimated": False,
        }
        visit.transcription_provider = "sample"
        visit.speaker_labels_estimated = False
        visit.audio_filename = "sample_transcript.txt"
        db.commit()
        db.refresh(visit)
        return UploadResponse(
            visit_id=visit.id,
            audio_filename=visit.audio_filename,
            audio_storage_uri=None,
            audio_duration_seconds=None,
            file_size_bytes=None,
            storage_provider=visit.storage_provider,
            message="Visit created with sample transcript. Ready for entity extraction.",
        )

    if not audio or not audio.filename:
        raise HTTPException(status_code=400, detail="Audio file is required unless using sample transcript")

    ext = Path(audio.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    content = await audio.read()
    file_size = len(content)
    storage_uri = await storage.save(content, audio.filename, str(visit.id))
    visit.audio_filename = audio.filename
    visit.audio_storage_uri = storage_uri

    local_path = await storage.get_path(storage_uri)
    if local_path:
        duration = get_audio_duration_seconds(local_path)

    visit.audio_duration_seconds = duration
    db.commit()
    db.refresh(visit)

    return UploadResponse(
        visit_id=visit.id,
        audio_filename=visit.audio_filename,
        audio_storage_uri=visit.audio_storage_uri,
        audio_duration_seconds=duration,
        file_size_bytes=file_size,
        storage_provider=visit.storage_provider,
        message="Audio uploaded successfully.",
    )
