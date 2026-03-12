"""
Configuration management for the RAG application.
Handles environment variables and application settings.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # ------------------------------------------------
    # Supabase Configuration
    # ------------------------------------------------
    supabase_url: str = Field(..., env="SUPABASE_URL")
    supabase_anon_key: str = Field(..., env="SUPABASE_ANON_KEY")
    supabase_service_role_key: str = Field(..., env="SUPABASE_SERVICE_ROLE_KEY")

    # ------------------------------------------------
    # AI Provider Configuration
    # ------------------------------------------------
    ai_provider: Literal["openai", "anthropic"] = Field(
        default="openai", env="AI_PROVIDER"
    )

    # ------------------------------------------------
    # OpenAI Configuration
    # ------------------------------------------------
    openai_api_key: str | None = Field(default=None, env="OPENAI_API_KEY")
    openai_embed_model: str = Field(
        default="text-embedding-3-small", env="OPENAI_EMBED_MODEL"
    )
    openai_chat_model: str = Field(
        default="gpt-4o", env="OPENAI_CHAT_MODEL"
    )

    # ------------------------------------------------
    # Anthropic Configuration
    # ------------------------------------------------
    anthropic_api_key: str | None = Field(default=None, env="ANTHROPIC_API_KEY")
    anthropic_chat_model: str = Field(
        default="claude-3-5-sonnet-20240620", env="ANTHROPIC_CHAT_MODEL"
    )

    # ------------------------------------------------
    # Application Configuration
    # ------------------------------------------------
    environment: str = Field(default="development", env="ENVIRONMENT")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    # ------------------------------------------------
    # RAG Configuration
    # ------------------------------------------------
    default_top_k: int = Field(default=6)
    chunk_size: int = Field(default=400)       # approximate tokens
    chunk_overlap: int = Field(default=60)     # ~15% overlap
    temperature: float = Field(default=0.1)
    embedding_dimensions: int = Field(default=1536)

    # ------------------------------------------------
    # Pydantic Settings Configuration
    # ------------------------------------------------
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance.

    Ensures settings are only loaded once per application
    lifecycle and improves performance for dependency injection.
    """
    return Settings()


# Global settings instance
settings = get_settings()