"""Deprecated: use app.services.llm instead."""

from app.services.llm.soap import generate_soap_with_llm as generate_ollama_soap

__all__ = ["generate_ollama_soap"]
