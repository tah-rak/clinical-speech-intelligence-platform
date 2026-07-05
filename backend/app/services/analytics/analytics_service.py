"""Analytics dashboard service."""

from collections import Counter
from datetime import datetime, timedelta, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.schemas import AnalyticsResponse
from app.models.visit import Visit

settings = get_settings()


class AnalyticsService:
    def get_analytics(self, db: Session) -> AnalyticsResponse:
        total_visits = db.query(func.count(Visit.id)).scalar() or 0

        soap_count = (
            db.query(func.count(Visit.id))
            .filter(Visit.soap_note_json.isnot(None))
            .scalar()
            or 0
        )

        avg_time = (
            db.query(func.avg(Visit.processing_time_seconds))
            .filter(Visit.processing_time_seconds.isnot(None))
            .scalar()
            or 0.0
        )

        week_ago = datetime.now(timezone.utc) - timedelta(days=7)
        files_this_week = (
            db.query(func.count(Visit.id))
            .filter(Visit.created_at >= week_ago)
            .scalar()
            or 0
        )

        visits_with_entities = (
            db.query(Visit).filter(Visit.entities_json.isnot(None)).all()
        )

        symptom_counter: Counter = Counter()
        total_symptoms = 0

        for visit in visits_with_entities:
            if visit.entities_json and "symptoms" in visit.entities_json:
                symptoms = visit.entities_json["symptoms"]
                total_symptoms += len(symptoms)
                symptom_counter.update(symptoms)

        most_common = [
            {"symptom": s, "count": c}
            for s, c in symptom_counter.most_common(5)
        ]

        return AnalyticsResponse(
            total_visits=total_visits,
            soap_notes_generated=soap_count,
            average_processing_time_seconds=round(float(avg_time), 2),
            total_symptoms_extracted=total_symptoms,
            most_common_symptoms=most_common,
            transcription_provider=settings.effective_stt_provider,
            files_processed_this_week=files_this_week,
            provider_status=settings.provider_status(),
        )
