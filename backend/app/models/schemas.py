"""Pydantic schemas for API request/response."""

from datetime import date, datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class VisitCreate(BaseModel):
    patient_name: str = Field(..., min_length=1, max_length=255)
    clinician_name: str = Field(..., min_length=1, max_length=255)
    visit_date: date
    visit_reason: str | None = None
    use_sample_transcript: bool = False


class TranscriptSegment(BaseModel):
    start: float
    end: float
    text: str
    speaker: str | None = None
    confidence: float | None = None


class TranscriptionResult(BaseModel):
    transcript_text: str
    segments: list[TranscriptSegment]
    formatted_transcript: str
    provider: str
    processing_time_seconds: float
    speaker_labels_estimated: bool = True
    confidence: float | None = None


class MedicalEntities(BaseModel):
    symptoms: list[str] = []
    medications: list[str] = []
    allergies: list[str] = []
    conditions: list[str] = []
    duration: list[str] = []
    tests_labs: list[str] = []
    diagnosis: list[str] = []
    treatment_plan: list[str] = []
    follow_up: list[str] = []


class SoapNote(BaseModel):
    subjective: str = ""
    objective: str = ""
    assessment: str = ""
    plan: str = ""
    generator: str = "template"


class SoapNoteUpdate(BaseModel):
    subjective: str = ""
    objective: str = ""
    assessment: str = ""
    plan: str = ""


class StatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(draft|reviewed|approved)$")


class ActionItem(BaseModel):
    id: str
    text: str
    category: str
    completed: bool = False


class VisitResponse(BaseModel):
    id: UUID
    patient_name: str
    clinician_name: str
    visit_date: date
    visit_reason: str | None
    audio_filename: str | None
    audio_storage_uri: str | None
    audio_duration_seconds: float | None
    transcript_text: str | None
    transcript_segments: dict | None
    entities_json: dict | None
    soap_note_json: dict | None
    visit_summary: str | None
    action_items_json: list | None
    transcription_provider: str | None
    storage_provider: str | None
    status: str
    processing_time_seconds: float | None
    speaker_labels_estimated: bool = False
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class VisitListItem(BaseModel):
    id: UUID
    patient_name: str
    clinician_name: str
    visit_date: date
    visit_reason: str | None
    status: str
    transcription_provider: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class UploadResponse(BaseModel):
    visit_id: UUID
    audio_filename: str | None
    audio_storage_uri: str | None
    audio_duration_seconds: float | None
    file_size_bytes: int | None
    storage_provider: str
    message: str


class AnalyticsResponse(BaseModel):
    total_visits: int
    soap_notes_generated: int
    average_processing_time_seconds: float
    total_symptoms_extracted: int
    most_common_symptoms: list[dict[str, Any]]
    transcription_provider: str
    files_processed_this_week: int
    provider_status: dict[str, Any]


class WerRequest(BaseModel):
    reference: str
    hypothesis: str


class WerResponse(BaseModel):
    wer: float
    substitutions: int
    deletions: int
    insertions: int
    reference_word_count: int
    hypothesis_word_count: int
    details: dict[str, Any]


class HealthResponse(BaseModel):
    status: str
    version: str
    providers: dict[str, Any]
