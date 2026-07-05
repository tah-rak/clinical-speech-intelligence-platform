"""Anthropic Messages API client."""

import logging

import httpx

from app.services.llm.base import LLMProvider, LLMResponse
from app.services.llm.config import ResolvedLLMConfig

logger = logging.getLogger(__name__)


class AnthropicProvider(LLMProvider):
    def __init__(self, config: ResolvedLLMConfig) -> None:
        self.config = config

    async def complete(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        url = f"{self.config.base_url}/v1/messages"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.config.api_key,
            "anthropic-version": "2023-06-01",
        }
        payload = {
            "model": self.config.model,
            "max_tokens": 2048,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}],
        }

        async with httpx.AsyncClient(timeout=self.config.timeout_seconds) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

        content = data["content"][0]["text"]
        return LLMResponse(
            content=content,
            provider=self.config.provider_name,
            model=self.config.model,
        )

    def get_provider_name(self) -> str:
        return self.config.provider_name
