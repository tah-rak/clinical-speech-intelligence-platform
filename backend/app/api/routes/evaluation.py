"""Evaluation API routes."""

from fastapi import APIRouter

from app.models.schemas import WerRequest, WerResponse
from app.services.evaluation.wer import calculate_wer

router = APIRouter(prefix="/evaluation", tags=["evaluation"])


@router.post("/wer", response_model=WerResponse)
async def compute_wer(request: WerRequest) -> WerResponse:
    result = calculate_wer(request.reference, request.hypothesis)
    return WerResponse(**result)
