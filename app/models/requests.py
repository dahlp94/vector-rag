from pydantic import BaseModel, Field


class RAGQueryRequest(BaseModel):
    """Request payload for RAG queries."""

    question: str = Field(..., min_length=1)
    top_k: int | None = Field(default=None, ge=1, le=20)