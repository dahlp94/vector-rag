from fastapi import FastAPI

from app.core.database import db
from app.services.rag import rag_service
from app.models.requests import RAGQueryRequest
from app.models.responses import RAGQueryResponse


app = FastAPI(
    title="Vector RAG Backend",
    description="Minimal FastAPI backend demonstrating Retrieval-Augmented Generation",
    version="0.1.0"
)


@app.on_event("startup")
async def startup_event():
    """Initialize application resources."""
    await db.connect()


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up application resources."""
    await db.disconnect()


@app.get("/health")
async def health():
    """Service health check."""
    db_ok = await db.health_check()

    return {
        "status": "ok",
        "database": "connected" if db_ok else "unavailable"
    }


@app.post("/rag/query", response_model=RAGQueryResponse)
async def rag_query(request: RAGQueryRequest):
    """Run a Retrieval-Augmented Generation query."""
    return await rag_service.query(
        question=request.question,
        top_k=request.top_k,
    )


@app.get("/")
async def root():
    return {"message": "Vector RAG backend is running"}