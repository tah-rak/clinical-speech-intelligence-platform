"""OpenAI-compatible chat completions client (works with most API providers)."""

import logging

import httpx

from app.services.llm.base import LLMProvider, LLMResponse
from app.services.llm.config import ResolvedLLMConfig

logger = logging.getLogger(__name__)


class OpenAICompatibleProvider(LLMProvider):
    """Works with OpenAI, Groq, Together, DeepSeek, Mistral, Ollama /v1, LM Studio, etc."""

    def __init__(self, config: ResolvedLLMConfig) -> None:
        self.config = config

    async def complete(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        url = f"{self.config.base_url}/chat/completions"
        headers = {"Content-Type": "application/json"}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        async with httpx.AsyncClient(timeout=self.config.timeout_seconds) as client:
            try:
                response = await client.post(
                    url,
                    headers=headers,
                    json={
                        "model": self.config.model,
                        "messages": messages,
                        "temperature": 0.2,
                        "response_format": {"type": "json_object"},
                    },
                )
                response.raise_for_status()
            except httpx.HTTPStatusError:
                # Some providers don't support response_format — retry without it
                response = await client.post(
                    url,
                    headers=headers,
                    json={
                        "model": self.config.model,
                        "messages": messages,
                        "temperature": 0.2,
                    },
                )
                response.raise_for_status()

            data = response.json()

        content = data["choices"][0]["message"]["content"]
        return LLMResponse(
            content=content,
            provider=self.config.provider_name,
            model=self.config.model,
        )

    def get_provider_name(self) -> str:
        return self.config.provider_name
