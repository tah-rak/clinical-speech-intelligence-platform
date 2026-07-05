"""Analytics API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.schemas import AnalyticsResponse
from app.services.analytics.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"])
analytics_service = AnalyticsService()


@router.get("", response_model=AnalyticsResponse)
async def get_analytics(db: Session = Depends(get_db)) -> AnalyticsResponse:
    return analytics_service.get_analytics(db)
