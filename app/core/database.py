"""
Database connection layer for Supabase-backed RAG operations.

This module provides a small, production-style database wrapper that can be
extended later with schema checks, ingestion utilities, and richer admin/user
client separation.
"""

import logging
from typing import Any, Optional

from supabase import Client, create_client

from .config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class Database:
    """Small Supabase database manager for RAG functionality."""

    def __init__(self) -> None:
        self._client: Optional[Client] = None

    async def connect(self) -> None:
        """Initialize the Supabase client."""
        try:
            self._client = create_client(
                settings.supabase_url,
                settings.supabase_service_role_key,
            )
            logger.info("Supabase client initialized successfully")
        except Exception:
            logger.exception("Failed to initialize Supabase client")
            raise

    async def disconnect(self) -> None:
        """Placeholder cleanup hook for application shutdown."""
        logger.info("Database shutdown complete")

    def get_client(self) -> Client:
        """Return the initialized Supabase client."""
        if self._client is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self._client

    async def vector_search(
        self,
        query_embedding: list[float],
        top_k: int = 6,
    ) -> list[dict[str, Any]]:
        """
        Run vector similarity search using the `match_chunks` RPC function.

        Expected SQL function signature in Supabase:
            match_chunks(query_embedding vector, match_count int)

        Returns:
            List of matching chunk records with similarity scores.
        """
        client = self.get_client()

        try:
            result = client.rpc(
                "match_chunks",
                {
                    "query_embedding": query_embedding,
                    "match_count": top_k,
                },
            ).execute()

            rows = result.data or []
            logger.info("Vector search returned %d rows", len(rows))
            return rows

        except Exception:
            logger.exception("Vector search failed")
            raise

    async def health_check(self) -> bool:
        """Check whether the database connection is working."""
        try:
            client = self.get_client()
            client.table("rag_chunks").select("id").limit(1).execute()
            return True
        except Exception:
            logger.exception("Database health check failed")
            return False


db = Database()