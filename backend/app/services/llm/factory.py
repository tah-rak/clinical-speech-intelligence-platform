"""LLM provider factory."""

import logging

from app.services.llm.anthropic_provider import AnthropicProvider
from app.services.llm.base import LLMProvider
from app.services.llm.config import resolve_llm_config
from app.services.llm.openai_compatible import OpenAICompatibleProvider
from app.services.llm.presets import list_preset_names

logger = logging.getLogger(__name__)


def get_llm_provider() -> LLMProvider | None:
    try:
        config = resolve_llm_config()
    except ValueError as e:
        logger.warning("LLM config error: %s", e)
        return None

    if not config.enabled:
        return None

    if config.api_style == "anthropic":
        return AnthropicProvider(config)

    return OpenAICompatibleProvider(config)


def get_available_providers() -> list[str]:
    return list_preset_names()
