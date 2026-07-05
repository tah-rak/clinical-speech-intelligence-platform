"""SOAP note generation API routes."""

import logging
import time
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.schemas import MedicalEntities, SoapNote, SoapNoteUpdate
from app.models.visit import Visit
from app.services.soap.soap_generator import SoapGenerator

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/visits", tags=["soap"])
soap_generator = SoapGenerator()


@router.post("/{visit_id}/soap", response_model=SoapNote)
async def generate_soap(
    visit_id: UUID,
    db: Session = Depends(get_db),
) -> SoapNote:
    visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")

    if not visit.transcript_text:
        raise HTTPException(status_code=400, detail="Transcript required")

    entities = MedicalEntities()
    if visit.entities_json:
        entities = MedicalEntities(**visit.entities_json)

    start = time.time()
    soap = await soap_generator.generate(
        visit.transcript_text,
        entities,
        visit.patient_name,
        visit.visit_reason,
    )
    elapsed = time.time() - start

    summary = soap_generator.generate_summary(
        visit.transcript_text, entities, visit.patient_name
    )
    action_items = soap_generator.generate_action_items(entities)

    visit.soap_note_json = soap.model_dump()
    visit.visit_summary = summary
    visit.action_items_json = [a.model_dump() for a in action_items]
    visit.processing_time_seconds = (visit.processing_time_seconds or 0) + round(elapsed, 2)
    db.commit()

    return soap


@router.patch("/{visit_id}/soap", response_model=SoapNote)
async def update_soap(
    visit_id: UUID,
    update: SoapNoteUpdate,
    db: Session = Depends(get_db),
) -> SoapNote:
    visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")

    existing = visit.soap_note_json or {}
    existing.update(update.model_dump())
    visit.soap_note_json = existing
    db.commit()

    return SoapNote(**existing)
