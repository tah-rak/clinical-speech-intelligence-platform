"""Template-based SOAP note generator (no LLM required)."""

from app.models.schemas import MedicalEntities, SoapNote


def generate_template_soap(
    transcript: str,
    entities: MedicalEntities,
    patient_name: str = "Patient",
    visit_reason: str | None = None,
) -> SoapNote:
    subjective_parts = [
        f"{patient_name} presents for evaluation.",
    ]
    if visit_reason:
        subjective_parts.append(f"Chief complaint: {visit_reason}.")
    if entities.symptoms:
        subjective_parts.append(
            f"Reports: {', '.join(entities.symptoms[:5])}."
        )
    if entities.duration:
        subjective_parts.append(
            f"Duration: {', '.join(entities.duration[:3])}."
        )
    if entities.medications:
        subjective_parts.append(
            f"Current medications: {', '.join(entities.medications[:5])}."
        )
    if entities.allergies:
        subjective_parts.append(
            f"Allergies: {', '.join(entities.allergies[:3])}."
        )

    objective_parts = [
        "Vital signs: Not documented in transcript.",
        "Physical examination findings not available from audio transcript.",
    ]
    if entities.tests_labs:
        objective_parts.append(
            f"Labs/tests discussed: {', '.join(entities.tests_labs[:5])}."
        )

    assessment_parts = []
    if entities.diagnosis:
        assessment_parts.append(
            f"Impression: {', '.join(entities.diagnosis[:3])}."
        )
    elif entities.conditions:
        assessment_parts.append(
            f"Known conditions: {', '.join(entities.conditions[:3])}."
        )
    elif entities.symptoms:
        assessment_parts.append(
            f"Clinical presentation consistent with {entities.symptoms[0].lower()}."
        )
    else:
        assessment_parts.append("Assessment pending further evaluation.")

    plan_parts = []
    if entities.treatment_plan:
        plan_parts.extend(entities.treatment_plan[:5])
    if entities.medications:
        plan_parts.append(f"Continue/adjust medications as discussed.")
    if entities.follow_up:
        plan_parts.extend(entities.follow_up[:3])
    if entities.tests_labs:
        plan_parts.append(f"Order: {', '.join(entities.tests_labs[:3])}.")
    if not plan_parts:
        plan_parts.append("Follow up as clinically indicated.")

    return SoapNote(
        subjective=" ".join(subjective_parts),
        objective=" ".join(objective_parts),
        assessment=" ".join(assessment_parts),
        plan=" ".join(plan_parts),
        generator="template",
    )
