-- =====================================================
-- Minimal Supabase Setup for Vector RAG Backend
-- This version creates only the essentials.
-- You can extend it later with indexes, RLS, and helpers.
-- =====================================================

-- -----------------------------------------------------
-- 1. Enable pgvector extension
-- -----------------------------------------------------

CREATE EXTENSION IF NOT EXISTS vector;

-- -----------------------------------------------------
-- 2. Create table for document chunks
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS rag_chunks (
    id BIGSERIAL PRIMARY KEY,
    chunk_id TEXT UNIQUE NOT NULL,
    source TEXT NOT NULL,
    text TEXT NOT NULL,
    embedding VECTOR(1536),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- -----------------------------------------------------
-- 3. Create vector similarity search function
-- -----------------------------------------------------

CREATE OR REPLACE FUNCTION match_chunks(
    query_embedding VECTOR(1536),
    match_count INT DEFAULT 6
)
RETURNS TABLE (
    chunk_id TEXT,
    source TEXT,
    text TEXT,
    similarity FLOAT
)
LANGUAGE SQL
AS $$
    SELECT
        rag_chunks.chunk_id,
        rag_chunks.source,
        rag_chunks.text,
        1 - (rag_chunks.embedding <=> query_embedding) AS similarity
    FROM rag_chunks
    ORDER BY rag_chunks.embedding <=> query_embedding
    LIMIT match_count;
$$;