# NHS Drug Interaction RAG

An educational Retrieval-Augmented Generation (RAG) system for checking drug-drug interactions based on NHS guidelines and clinical data.

## Project Structure

- `data/`: Knowledge base and processed artifacts.
  - `raw/`: Original source documents (dm+d, SmPCs, NHS SPS guidance, etc.).
  - `processed/`: Text extractions, chunks, and metadata.
  - `indexes/`: Vector store indexes (FAISS, pgvector, BM25).
- `src/`: Core logic for the RAG pipeline.
  - `ingest/`: Data loading and processing scripts.
  - `rag/`: Retrieval and generation logic.
  - `api/`: FastAPI web server.
  - `utils/`: Shared helper functions.
- `scripts/`: One-off maintenance or task scripts.
- `AGENTS.md`: System-level instructions for AI collaboration.

## Getting Started

1. Place source PDFs in `data/raw/`.
2. Run ingestion scripts to process and index data.
3. Start the API server for chat interactions.

---
*Educational use only. Not for clinical decision making.*
