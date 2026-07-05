"""Visit CRUD API routes."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.schemas import StatusUpdate, VisitListItem, VisitResponse
from app.models.visit import Visit

router = APIRouter(prefix="/visits", tags=["visits"])


@router.get("", response_model=list[VisitListItem])
async def list_visits(
    search: str | None = Query(None),
    status: str | None = Query(None),
    db: Session = Depends(get_db),
) -> list[VisitListItem]:
    query = db.query(Visit).order_by(Visit.created_at.desc())

    if status:
        query = query.filter(Visit.status == status)

    if search:
        pattern = f"%{search}%"
        query = query.filter(
            (Visit.patient_name.ilike(pattern))
            | (Visit.clinician_name.ilike(pattern))
            | (Visit.visit_reason.ilike(pattern))
        )

    return query.all()


@router.get("/{visit_id}", response_model=VisitResponse)
async def get_visit(
    visit_id: UUID,
    db: Session = Depends(get_db),
) -> VisitResponse:
    visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    return visit


@router.patch("/{visit_id}/status", response_model=VisitResponse)
async def update_status(
    visit_id: UUID,
    update: StatusUpdate,
    db: Session = Depends(get_db),
) -> VisitResponse:
    visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")

    visit.status = update.status
    db.commit()
    db.refresh(visit)
    return visit
