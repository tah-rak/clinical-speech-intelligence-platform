"""SOAP note generation orchestrator."""

import logging
import uuid

from app.models.schemas import ActionItem, MedicalEntities, SoapNote
from app.services.llm import generate_soap_with_llm
from app.services.soap.template_generator import generate_template_soap

logger = logging.getLogger(__name__)


class SoapGenerator:
    async def generate(
        self,
        transcript: str,
        entities: MedicalEntities,
        patient_name: str = "Patient",
        visit_reason: str | None = None,
    ) -> SoapNote:
        llm_note = await generate_soap_with_llm(transcript, entities, patient_name)
        if llm_note:
            return llm_note
        return generate_template_soap(transcript, entities, patient_name, visit_reason)

    def generate_summary(
        self,
        transcript: str,
        entities: MedicalEntities,
        patient_name: str,
    ) -> str:
        symptoms = ", ".join(entities.symptoms[:3]) if entities.symptoms else "unspecified symptoms"
        return (
            f"Visit summary for {patient_name}: Patient presented with {symptoms}. "
            f"Clinical discussion covered assessment and management plan. "
            f"{'Medications discussed: ' + ', '.join(entities.medications[:3]) + '. ' if entities.medications else ''}"
            f"Clinician review required before finalizing documentation."
        )

    def generate_action_items(self, entities: MedicalEntities) -> list[ActionItem]:
        items: list[ActionItem] = []

        for test in entities.tests_labs[:3]:
            items.append(
                ActionItem(
                    id=str(uuid.uuid4()),
                    text=f"Order {test}",
                    category="lab_work",
                )
            )

        for med in entities.medications[:2]:
            items.append(
                ActionItem(
                    id=str(uuid.uuid4()),
                    text=f"Start/continue {med}",
                    category="medication",
                )
            )

        for follow in entities.follow_up[:2]:
            items.append(
                ActionItem(
                    id=str(uuid.uuid4()),
                    text=f"Follow-up: {follow}",
                    category="follow_up",
                )
            )

        if entities.symptoms:
            items.append(
                ActionItem(
                    id=str(uuid.uuid4()),
                    text=f"Monitor symptoms: {', '.join(entities.symptoms[:2])}",
                    category="monitor",
                )
            )

        if not items:
            items.append(
                ActionItem(
                    id=str(uuid.uuid4()),
                    text="Schedule follow-up visit as clinically indicated",
                    category="follow_up",
                )
            )

        return items
