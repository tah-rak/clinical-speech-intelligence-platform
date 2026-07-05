"""Entity extraction API routes."""

import logging
import time
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.schemas import MedicalEntities
from app.models.visit import Visit
from app.services.nlp.entity_extractor import EntityExtractor

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/visits", tags=["entities"])
extractor = EntityExtractor()


@router.post("/{visit_id}/entities", response_model=MedicalEntities)
async def extract_entities(
    visit_id: UUID,
    db: Session = Depends(get_db),
) -> MedicalEntities:
    visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")

    if not visit.transcript_text:
        raise HTTPException(status_code=400, detail="Transcript required. Run transcription first.")

    start = time.time()
    entities = extractor.extract(visit.transcript_text)
    elapsed = time.time() - start

    visit.entities_json = entities.model_dump()
    visit.processing_time_seconds = (visit.processing_time_seconds or 0) + round(elapsed, 2)
    db.commit()

    return entities
