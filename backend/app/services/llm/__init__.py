"""Plug-and-play LLM integration for any API provider."""

from app.services.llm.factory import get_available_providers, get_llm_provider
from app.services.llm.soap import generate_soap_with_llm

__all__ = [
    "generate_soap_with_llm",
    "get_llm_provider",
    "get_available_providers",
]
