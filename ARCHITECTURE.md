# NHS Drug Interaction RAG: System Architecture (2026 Edition)

This document outlines the high-performance, safety-critical architecture of the NHS Drug Interaction RAG system, leveraging the **Gemma 4** model family and state-of-the-art retrieval patterns for clinical data.

---

## 1. Core Model: Gemma 4 26B-A4B (MoE)
Chosen for its optimal balance of deep reasoning and local efficiency.

- **Architecture**: Mixture of Experts (MoE) with ~3.8B active parameters per token.
- **Context Window**: **256K Tokens**. This allows for the ingestion of entire SmPC (Summary of Product Characteristics) booklets without losing narrative context.
- **Thinking Mode**: Native support for internal reasoning via the `<|think|>` channel.
- **Privacy**: Deployed locally via **Ollama**, ensuring 100% compliance with data privacy standards (GDPR/DTAC) as no medical queries leave the local environment.

---

## 2. Ingestion Pipeline: "Surgical" RAG
Following 2026 best practices, we use **Hierarchical Chunking** to solve the "Lost in the Middle" syndrome.

### Hierarchical Processing
1.  **Child Chunks (~200 tokens)**: Optimized for semantic retrieval. These pinpoint specific technical terms (e.g., "CYP3A4 inhibition").
2.  **Parent Chunks (~2000 tokens)**: The context actually fed to the model. This preserves the surrounding clinical warnings and management sections.
3.  **ASTRID Alignment**: We ensure high-precision retrieval to avoid confusing similar-sounding drugs (look-alike/sound-alike errors).

---

## 3. Retrieval Strategy: Hybrid Search
Simple vector search is insufficient for medical precision. Our system uses a multi-stage retrieval flow:

1.  **Stage 1: Hybrid Retrieval**:
    - **Dense (Vector)**: Captures semantic meaning and intent.
    - **Sparse (Keyword/BM25)**: Ensures exact matches for drug names (e.g., "Metformin") and clinical codes.
2.  **Stage 2: Metadata Filtering**: Restricting searches by drug class or severity markers stored in the vector metadata.
3.  **Stage 3: Cross-Encoder Re-ranking**: (Planned) Using a secondary model to score the top-20 retrieved snippets for relevance before passing them to Gemma 4.

---

## 4. Reasoning & Generation: The "Thinking Gate"
We utilize Gemma 4's reasoning channel as a clinical safety gate.

### The Reasoning Loop
1.  **Retrieve**: Fetch the most relevant parent chunks.
2.  **Think**: The model uses `<|channel>thought` to:
    - Compare findings across multiple documents.
    - Identify conflicting advice (e.g., different severity for the same interaction).
    - Double-check drug names against the retrieved context.
3.  **Answer**: Provide a concise, cited response with clear **Risk/Severity** and **Management** categories.

---

## 5. Safety & Refusal Logic
- **Safety Benchmarks**: Evaluating against ASTRID and MedRGB safety datasets.
- **Educational Boundary**: The system explicitly refuses to provide definitve "prescribing instructions," instead providing "clinical considerations" grounded in NHS documentation.
- **Citations**: Native parsing of document IDs to ensure every claim maps back to a specific section of a drug monograph.

---
*Architecture authored on April 12, 2026, for the NHS-RAG Educational Project.*
