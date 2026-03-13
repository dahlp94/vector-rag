"""
Core Retrieval-Augmented Generation pipeline.

This service orchestrates:
1. Query embedding
2. Vector similarity search
3. Context assembly
4. LLM answer generation
"""

from typing import Any

from openai import OpenAI

from app.core.config import get_settings
from app.core.database import db
from app.services.embedding import embedding_service

settings = get_settings()


class RAGService:
    """Service for retrieval-augmented generation."""

    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required for answer generation.")
        self.client = OpenAI(api_key=settings.openai_api_key)

    def _build_context(self, chunks: list[dict[str, Any]]) -> str:
        """
        Convert retrieved chunks into a prompt-ready context block.
        Each chunk is labeled so the model can cite sources clearly.
        """
        if not chunks:
            return ""

        context_blocks = []
        for idx, chunk in enumerate(chunks, start=1):
            source = chunk.get("source", "unknown")
            text = chunk.get("text", "")
            chunk_id = chunk.get("chunk_id", f"chunk_{idx}")

            block = (
                f"[Source {idx}]\n"
                f"chunk_id: {chunk_id}\n"
                f"source: {source}\n"
                f"text: {text}"
            )
            context_blocks.append(block)

        return "\n\n".join(context_blocks)

    def _build_citations(self, chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Build citation objects for API responses.
        """
        citations = []

        for idx, chunk in enumerate(chunks, start=1):
            text = chunk.get("text", "")
            snippet = text[:220] + "..." if len(text) > 220 else text

            citations.append(
                {
                    "index": idx,
                    "chunk_id": chunk.get("chunk_id"),
                    "source": chunk.get("source"),
                    "similarity": chunk.get("similarity"),
                    "snippet": snippet,
                }
            )

        return citations

    async def query(self, question: str, top_k: int | None = None) -> dict[str, Any]:
        """
        Run the full RAG pipeline for a user question.

        Args:
            question: User query.
            top_k: Number of chunks to retrieve.

        Returns:
            Dictionary containing answer, citations, and retrieval metadata.
        """
        cleaned_question = question.strip()
        if not cleaned_question:
            raise ValueError("Question must not be empty.")

        top_k = top_k or settings.default_top_k

        # 1. Embed the query
        query_embedding = await embedding_service.embed_text(cleaned_question)

        # 2. Retrieve relevant chunks from Supabase/pgvector
        chunks = await db.vector_search(query_embedding=query_embedding, top_k=top_k)

        # 3. Build context for the LLM
        context = self._build_context(chunks)

        # 4. Handle no-retrieval case cleanly
        if not chunks:
            return {
                "answer": "I could not find any relevant context for that question.",
                "citations": [],
                "retrieved_chunks": 0,
            }

        # 5. Generate grounded answer
        prompt = f"""
You are a helpful assistant answering questions using retrieved context.

Use only the provided context to answer the question.
If the answer is not contained in the context, say that clearly.
When relevant, reference sources as [Source 1], [Source 2], etc.

Question:
{cleaned_question}

Context:
{context}
""".strip()

        response = self.client.chat.completions.create(
            model=settings.openai_chat_model,
            messages=[
                {
                    "role": "system",
                    "content": "You answer questions using only the provided retrieved context.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=settings.temperature,
        )

        answer = response.choices[0].message.content or ""

        return {
            "answer": answer,
            "citations": self._build_citations(chunks),
            "retrieved_chunks": len(chunks),
        }


rag_service = RAGService()