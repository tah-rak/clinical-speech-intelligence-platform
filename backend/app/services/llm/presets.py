"""
Plug-and-play LLM provider presets.

To add a new provider, add one entry below. Users then set:
  LLM_ENABLED=true
  LLM_PROVIDER=<preset_name>
  LLM_API_KEY=<their-key>

For fully custom endpoints:
  LLM_PROVIDER=custom
  LLM_BASE_URL=https://api.example.com/v1
  LLM_MODEL=their-model-name
  LLM_API_KEY=their-key
"""

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class ProviderPreset:
    base_url: str
    default_model: str
    api_style: Literal["openai", "anthropic", "ollama_native"] = "openai"
    # Some local servers accept any non-empty key
    default_api_key: str = ""


# ---------------------------------------------------------------------------
# ADD NEW PROVIDERS HERE — one block per service
# ---------------------------------------------------------------------------
PROVIDER_PRESETS: dict[str, ProviderPreset] = {
    "openai": ProviderPreset(
        base_url="https://api.openai.com/v1",
        default_model="gpt-4o-mini",
    ),
    "groq": ProviderPreset(
        base_url="https://api.groq.com/openai/v1",
        default_model="llama-3.3-70b-versatile",
    ),
    "together": ProviderPreset(
        base_url="https://api.together.xyz/v1",
        default_model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    ),
    "deepseek": ProviderPreset(
        base_url="https://api.deepseek.com/v1",
        default_model="deepseek-chat",
    ),
    "mistral": ProviderPreset(
        base_url="https://api.mistral.ai/v1",
        default_model="mistral-small-latest",
    ),
    "openrouter": ProviderPreset(
        base_url="https://openrouter.ai/api/v1",
        default_model="meta-llama/llama-3.3-70b-instruct",
    ),
    "gemini": ProviderPreset(
        base_url="https://generativelanguage.googleapis.com/v1beta/openai",
        default_model="gemini-2.0-flash",
    ),
    "ollama": ProviderPreset(
        base_url="http://host.docker.internal:11434/v1",
        default_model="llama3.2",
        api_style="openai",
        default_api_key="ollama",
    ),
    "lmstudio": ProviderPreset(
        base_url="http://host.docker.internal:1234/v1",
        default_model="local-model",
        default_api_key="lmstudio",
    ),
    "anthropic": ProviderPreset(
        base_url="https://api.anthropic.com",
        default_model="claude-3-5-haiku-20241022",
        api_style="anthropic",
    ),
    "custom": ProviderPreset(
        base_url="",
        default_model="",
        api_style="openai",
    ),
}


def list_preset_names() -> list[str]:
    return sorted(PROVIDER_PRESETS.keys())
