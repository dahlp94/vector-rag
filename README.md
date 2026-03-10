# Vector RAG Backend

A minimal **production-ready FastAPI backend** implementing **Retrieval-Augmented Generation (RAG)** using vector similarity search.

This project demonstrates how to build a clean, modular RAG service using:

* **FastAPI** for the API layer
* **Supabase + pgvector** for vector search
* **OpenAI / Anthropic** for LLM inference
* **Semantic embeddings** for retrieval
* **Citation-based responses** for explainability

The architecture is designed to integrate easily with **NextJS frontends or other web clients**.

---

# Architecture Overview

```
                ┌───────────────────────┐
                │       Client / UI     │
                │  (NextJS / Web App)   │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │        FastAPI        │
                │        Backend        │
                │                       │
                │   /rag/query endpoint │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │      RAG Pipeline     │
                │                       │
                │ 1. Embed question     │
                │ 2. Vector search      │
                │ 3. Build context      │
                │ 4. Generate answer    │
                └───────────┬───────────┘
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
   ┌───────────────────┐          ┌────────────────────┐
   │  Supabase DB      │          │    LLM Providers   │
   │  + pgvector       │          │                    │
   │                   │          │  OpenAI / Claude   │
   │ document_chunks   │          │                    │
   │ embeddings        │          │ answer generation  │
   └───────────────────┘          └────────────────────┘
```

---

# Project Structure

```
vector-rag/
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── requests.py
│   │   ├── responses.py
│   │   └── entities.py
│   │
│   ├── services/
│   │   ├── embedding.py
│   │   ├── rag.py
│   │   └── chunker.py
│   │
│   └── main.py
│
├── sql/
│   └── init_supabase.sql
│
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

---

# Features

* FastAPI backend with automatic API documentation
* Vector similarity search with **pgvector**
* Multi-provider LLM support (OpenAI & Anthropic)
* Citation-based responses
* Modular RAG pipeline
* Docker-ready deployment
* Frontend-ready API design

---

# Running Locally

Create virtual environment:

```
python3.11 -m venv venv_vector_rag
source venv_vector_rag/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the server:

```
uvicorn app.main:app --reload
```

Open API docs:

```
http://localhost:8000/docs
```

---

# Example API Request

POST `/rag/query`

```
{
  "question": "What is Retrieval-Augmented Generation?",
  "top_k": 5
}
```

Response:

```
{
  "answer": "...",
  "citations": [...],
  "retrieved_chunks": 5
}
```

---

# Future Improvements

* Hybrid search (vector + keyword)
* Reranking models
* Streaming responses
* Document ingestion pipeline
* Evaluation framework for RAG performance
