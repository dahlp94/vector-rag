"""
Embedding service for generating vector representations of text.
"""

from typing import List
from openai import OpenAI
from app.core.config import get_settings

settings = get_settings()

class EmbeddingService:
    """Service for generating embeddings using the configured AI provider."""

    def __init__(self) -> None:
        self.provider = settings.ai_provider

        if self.provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required when AI_PROVIDER='openai'")
            self.client = OpenAI(api_key=settings.openai_api_key)
        else:
            raise ValueError(f"Unsupported embedding provider: {self.provider}")

    async def embed_text(self, text: str) -> List[float]:
        """
        Generate an embedding vector for a single text input.

        Args:
            text: Input text to embed.

        Returns:
            A list of floats representing the embedding vector.
        """
        cleaned_text = text.strip()
        if not cleaned_text:
            raise ValueError("Input text for embedding must not be empty.")

        if self.provider == "openai":
            response = self.client.embeddings.create(
                model=settings.openai_embed_model,
                input=cleaned_text,
            )
            return response.data[0].embedding

        raise ValueError(f"Unsupported embedding provider: {self.provider}")

embedding_service = EmbeddingService()