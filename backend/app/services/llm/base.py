"""LLM provider base interface."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMResponse:
    content: str
    provider: str
    model: str


class LLMProvider(ABC):
    @abstractmethod
    async def complete(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        """Send a prompt and return the model's text response."""

    @abstractmethod
    def get_provider_name(self) -> str:
        """Return provider identifier for logging and SOAP metadata."""
