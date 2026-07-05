"""Visit SQLAlchemy model."""

import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.database import Base


class Visit(Base):
    __tablename__ = "visits"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    patient_name: Mapped[str] = mapped_column(String(255), nullable=False)
    clinician_name: Mapped[str] = mapped_column(String(255), nullable=False)
    visit_date: Mapped[date] = mapped_column(Date, nullable=False)
    visit_reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
    audio_filename: Mapped[str | None] = mapped_column(String(500), nullable=True)
    audio_storage_uri: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    audio_duration_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)
    transcript_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    transcript_segments: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    entities_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    soap_note_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    visit_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    action_items_json: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    transcription_provider: Mapped[str | None] = mapped_column(String(50), nullable=True)
    storage_provider: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False)
    processing_time_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)
    speaker_labels_estimated: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
