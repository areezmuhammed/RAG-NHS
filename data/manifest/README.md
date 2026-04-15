# Data Manifests

This directory contains metadata and source links for the NHS Drug Interaction RAG knowledge base.

## Files

- `source_links.json`: Base URLs for official medical sources (dm+d, MHRA, SPS, etc.).
- `drugs_master.json`: A master list of drugs to be ingested, including their clinical category and source URLs.

## Data Pipeline Roles

- **manifest/**: Stores configuration, metadata, and download links.
- **raw/**: Stores the original downloaded files (PDFs, JSONs) before any processing.
- **processed/**: Stores the outputs of the ingestion pipeline:
  - `text/`: Cleaned text extracted from PDFs.
  - `chunks/`: Text split into logical chunks for embedding.
  - `metadata/`: Metadata associated with each chunk (source ID, drug name, etc.).
- **indexes/**: Stores the finalized search indexes (FAISS, pgvector, etc.) used by the RAG retriever.
