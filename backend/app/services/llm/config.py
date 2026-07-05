"""Resolve LLM configuration from settings and presets."""

from dataclasses import dataclass

from app.core.config import Settings, get_settings
from app.services.llm.presets import PROVIDER_PRESETS


@dataclass
class ResolvedLLMConfig:
    enabled: bool
    provider_name: str
    base_url: str
    model: str
    api_key: str
    api_style: str
    timeout_seconds: int


def resolve_llm_config(settings: Settings | None = None) -> ResolvedLLMConfig:
    settings = settings or get_settings()
    provider_name = settings.effective_llm_provider
    preset = PROVIDER_PRESETS.get(provider_name, PROVIDER_PRESETS["custom"])

    base_url = settings.LLM_BASE_URL or preset.base_url
    model = settings.LLM_MODEL or preset.default_model
    api_key = settings.LLM_API_KEY or preset.default_api_key
    api_style = settings.LLM_API_STYLE or preset.api_style

    # Legacy Ollama env vars
    if provider_name == "ollama" and settings.OLLAMA_ENABLED and not settings.LLM_ENABLED:
        if settings.OLLAMA_BASE_URL:
            base_url = settings.OLLAMA_BASE_URL.rstrip("/")
            if not base_url.endswith("/v1"):
                base_url = f"{base_url}/v1"
        if settings.OLLAMA_MODEL:
            model = settings.OLLAMA_MODEL

    if provider_name == "custom" and not base_url:
        raise ValueError("LLM_PROVIDER=custom requires LLM_BASE_URL")

    return ResolvedLLMConfig(
        enabled=settings.llm_enabled,
        provider_name=provider_name,
        base_url=base_url.rstrip("/"),
        model=model,
        api_key=api_key,
        api_style=api_style,
        timeout_seconds=settings.LLM_TIMEOUT_SECONDS,
    )
