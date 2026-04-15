# AGENTS.md – NHS Drug Interaction RAG

You are assisting with a **Retrieval-Augmented Generation (RAG)** project: an NHS-style drug–drug interaction checker for educational use only.

The stack is:
- Backend: Python (FastAPI) + LangChain-style RAG pipeline
- Vector store: FAISS / pgvector / Pinecone (abstracted behind a retriever)
- Frontend: simple chat UI (e.g. Next.js/React or Streamlit)
- Models: embedding model + chat LLM (configurable via environment variables)

## Project goals

- Answer questions about **drug–drug interactions** and related clinical considerations using the project’s knowledge base.
- Always ground answers in retrieved documents and **show citations**.
- Enforce **safety**: this app is for learning, not real-world prescribing or diagnosis.
- **Educational Objective**: This project serves as a practical learning tool for building modern, high-precision RAG systems (using 2026 best practices like Hierarchical Chunking and Agentic Reasoning).

Examples of supported queries:
- "Can a diabetic patient take ibuprofen with metformin?"
- "What are the main interactions between warfarin and amiodarone?"
- "Is sertraline safe with tramadol? What should be monitored?"

## Critical rules

1. Never invent drugs, doses, or guidelines that are not present in the indexed data.
2. Treat all content as **educational only**. Do not give definitive prescribing instructions.
3. If context is missing or unclear, say you **do not know** and suggest consulting official NHS/BNF resources.
4. Prefer concise, structured answers with:
   - Risk / severity
   - Mechanism (if known)
   - Monitoring / management considerations
   - Citations or source IDs

## Code navigation

- `backend/` – FastAPI app and RAG pipeline:
  - `api/` – HTTP endpoints
  - `rag/` – retrieval and generation logic (retriever, prompts, chains)
  - `models/` – pydantic schemas, domain models
- `data/` – input datasets:
  - `drug_monographs.*` – per-drug information
  - `interaction_pairs.*` – drug–drug interaction records
- `scripts/` – one-off scripts:
  - ingestion, indexing, evaluation
- `frontend/` – chat UI and API client

When adding new code, keep RAG logic in `backend/rag/` and avoid mixing it with HTTP handler code.

## How to help with coding

- Prefer small, focused functions and pure logic where possible.
- Keep RAG components modular:
  - **Ingestion**: loading and chunking documents, attaching metadata
  - **Retrieval**: query -> retriever -> ranked documents
  - **Generation**: prompt construction and LLM call
  - **Safety**: query classification and refusal / caution logic
- Make cross-cutting concerns (logging, metrics, config) reusable utilities.

If a function is doing more than one of these steps, consider splitting it.

## RAG behaviour expectations

When editing or creating code that interacts with the model:

- Always pass retrieved documents (or their content + metadata) explicitly into the prompt or chain.
- Ensure prompts:
  - Tell the model to answer **only** from provided context.
  - Tell the model to admit when the answer is not in the context.
  - Require citations mapped back to document IDs / URLs.
- Avoid long chain-of-thought in final responses; keep answers short but clinically sensible.

## Safety and refusal behaviour

Implement and preserve these behaviours:

- Classify queries into:
  - General education (allowed)
  - Prescribing / dosing / urgent triage (respond cautiously, avoid specific instructions)
- For high‑risk queries (e.g. "What dose should I give?"):
  - Decline to provide exact dosing.
  - Encourage consulting official guidelines or a qualified clinician.
- Do not bypass safety checks when adding tools or new endpoints.

## Testing and evaluation

- Maintain tests for:
  - Retrieval quality (e.g. expected interaction documents are in top‑k).
  - Basic safety behaviours (e.g. high‑risk queries trigger a cautious response).
  - API contract (input/output schemas).

When adding new features, add at least one test (unit or integration) that covers the new behaviour.

## Configuration

- Use environment variables for:
  - LLM and embedding model API keys
  - Vector DB connection details
  - Feature flags (e.g. which retriever implementation to use)
- Do not hardcode secrets or endpoints in source files.

---