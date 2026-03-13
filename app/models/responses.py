from pydantic import BaseModel


class Citation(BaseModel):
    index: int
    chunk_id: str | None
    source: str | None
    similarity: float | None
    snippet: str


class RAGQueryResponse(BaseModel):
    answer: str
    citations: list[Citation]
    retrieved_chunks: int