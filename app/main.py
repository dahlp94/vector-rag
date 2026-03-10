from fastapi import FastAPI

app = FastAPI(title="Vector RAG API", version="0.1")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "Vector RAG backend is running"}