"""SOAP note prompts and LLM-powered generation."""

import logging

from app.models.schemas import MedicalEntities, SoapNote
from app.services.llm.base import LLMProvider
from app.services.llm.config import resolve_llm_config
from app.services.llm.factory import get_llm_provider
from app.services.llm.utils import parse_json_content

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are a clinical documentation assistant. "
    "Generate professional SOAP notes from clinical conversations. "
    "Only include findings supported by the transcript. "
    "Respond with valid JSON only."
)


def build_soap_user_prompt(
    transcript: str,
    entities: MedicalEntities,
    patient_name: str,
) -> str:
    return f"""Generate a SOAP note from this clinical conversation.

Patient: {patient_name}

Transcript:
{transcript[:4000]}

Extracted entities:
- Symptoms: {', '.join(entities.symptoms) or 'none'}
- Medications: {', '.join(entities.medications) or 'none'}
- Conditions: {', '.join(entities.conditions) or 'none'}
- Allergies: {', '.join(entities.allergies) or 'none'}

Return JSON with exactly these keys: subjective, objective, assessment, plan.
Each value should be 2-4 sentences of professional clinical documentation."""


async def generate_soap_with_llm(
    transcript: str,
    entities: MedicalEntities,
    patient_name: str = "Patient",
    provider: LLMProvider | None = None,
) -> SoapNote | None:
    config = resolve_llm_config()
    if not config.enabled:
        return None
    if config.provider_name != "ollama" and not config.api_key:
        logger.warning("LLM enabled but LLM_API_KEY is missing")
        return None

    llm = provider or get_llm_provider()
    if llm is None:
        return None

    try:
        response = await llm.complete(
            SYSTEM_PROMPT,
            build_soap_user_prompt(transcript, entities, patient_name),
        )
        result = parse_json_content(response.content)
        return SoapNote(
            subjective=result.get("subjective", ""),
            objective=result.get("objective", ""),
            assessment=result.get("assessment", ""),
            plan=result.get("plan", ""),
            generator=response.provider,
        )
    except Exception as e:
        logger.warning("LLM SOAP generation failed (%s): %s", config.provider_name, e)
        return None
