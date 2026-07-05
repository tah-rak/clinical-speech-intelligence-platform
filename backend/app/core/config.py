"""Application configuration loaded from environment variables."""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    APP_NAME: str = "Clinical Speech Intelligence Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_PREFIX: str = "/api"
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000,http://localhost:80"

    # Database
    DATABASE_PROVIDER: Literal["local", "firestore"] = "local"
    DATABASE_URL: str = "postgresql://csip:csip@localhost:5432/csip"
    FIRESTORE_PROJECT_ID: str = ""

    # Storage
    STORAGE_PROVIDER: Literal["local", "s3"] = "local"
    UPLOAD_DIR: str = "uploads"

    # AWS
    AWS_ENABLED: bool = False
    AWS_REGION: str = "us-east-1"
    AWS_S3_BUCKET: str = ""
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""

    # Speech-to-Text
    STT_PROVIDER: Literal["local", "azure", "gcp"] = "local"
    WHISPER_MODEL: str = "base"
    WHISPER_DEVICE: str = "cpu"
    WHISPER_COMPUTE_TYPE: str = "int8"

    # Azure Speech
    AZURE_SPEECH_ENABLED: bool = False
    AZURE_SPEECH_KEY: str = ""
    AZURE_SPEECH_REGION: str = ""

    # GCP
    GCP_ENABLED: bool = False
    GOOGLE_APPLICATION_CREDENTIALS: str = ""

    # LLM (plug-and-play — see app/services/llm/presets.py)
    LLM_ENABLED: bool = False
    LLM_PROVIDER: str = "openai"  # preset name: openai, groq, anthropic, ollama, custom, ...
    LLM_API_KEY: str = ""
    LLM_BASE_URL: str = ""  # required when LLM_PROVIDER=custom
    LLM_MODEL: str = ""  # optional override; uses preset default if empty
    LLM_API_STYLE: str = ""  # optional override: openai | anthropic
    LLM_TIMEOUT_SECONDS: int = 90

    # Legacy Ollama flags (mapped to LLM_PROVIDER=ollama when LLM_ENABLED is false)
    OLLAMA_ENABLED: bool = False
    OLLAMA_BASE_URL: str = "http://host.docker.internal:11434"
    OLLAMA_MODEL: str = "llama3.2"

    @property
    def llm_enabled(self) -> bool:
        return self.LLM_ENABLED or self.OLLAMA_ENABLED

    @property
    def effective_llm_provider(self) -> str:
        if self.LLM_ENABLED:
            return self.LLM_PROVIDER.lower()
        if self.OLLAMA_ENABLED:
            return "ollama"
        return self.LLM_PROVIDER.lower()

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    @property
    def effective_storage_provider(self) -> str:
        if self.AWS_ENABLED and self.STORAGE_PROVIDER == "s3":
            return "s3"
        return "local"

    @property
    def effective_stt_provider(self) -> str:
        if self.STT_PROVIDER == "azure" and self.AZURE_SPEECH_ENABLED and self.AZURE_SPEECH_KEY:
            return "azure"
        if self.STT_PROVIDER == "gcp" and self.GCP_ENABLED:
            return "gcp"
        return "local"

    def provider_status(self) -> dict:
        llm_configured = self.llm_enabled and (
            self.effective_llm_provider == "ollama" or bool(self.LLM_API_KEY)
        )
        return {
            "stt_provider": self.effective_stt_provider,
            "storage_provider": self.effective_storage_provider,
            "database_provider": self.DATABASE_PROVIDER,
            "aws_enabled": self.AWS_ENABLED and bool(self.AWS_S3_BUCKET),
            "azure_speech_enabled": self.AZURE_SPEECH_ENABLED and bool(self.AZURE_SPEECH_KEY),
            "gcp_enabled": self.GCP_ENABLED,
            "llm_enabled": llm_configured,
            "llm_provider": self.effective_llm_provider if llm_configured else None,
            "ollama_enabled": self.OLLAMA_ENABLED,
            "whisper_model": self.WHISPER_MODEL,
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()
