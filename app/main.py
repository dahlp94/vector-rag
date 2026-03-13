from fastapi import FastAPI

from app.core.database import db

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


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Vector RAG backend is running"}