# 🏥 NHS Drug Interaction RAG

An advanced, educational **Retrieval-Augmented Generation (RAG)** pipeline designed to check for drug-drug interactions (DDI) based on clinical data and official NHS guidelines. 

This project demonstrates 2026 best practices in high-precision RAG, utilizing agentic reasoning and hierarchical document processing to provide safe, grounded responses.

---

## ⚡ Key Features

*   **Hierarchical (Parent-Child) Chunking**: Optimizes retrieval for high precision by indexing small chunks for search while retrieving large parent contexts for generation.
*   **Gemma 4 Agentic Reasoning**: Leverages Gemma 4's native "Thinking Mode" to clinically verify interactions before generating a response.
*   **Safety-First Design**: Implements query classification and clinical groundedness checks to prevent hallucinations.
*   **Local-First Stack**: Designed for privacy and speed using local LLMs (Ollama) and local embeddings (BGE).

## 🛠️ Technical Stack

*   **Core Logic**: Python 3.11+, LangChain
*   **LLM**: Gemma 4 (via Ollama)
*   **Embeddings**: `BAAI/bge-large-en-v1.5` (HuggingFace)
*   **Vector Store**: FAISS (Local)
*   **Framework**: FastAPI (Backend API)

## 📂 Project Structure

```text
├── data/
│   ├── manifest/       # Drug master lists and source metadata
│   ├── raw/            # Original SmPC/NHS documents (PDF/Text)
│   └── indexes/        # Generated FAISS vector stores
├── src/
│   ├── rag/            # The "Brain": Retrieval and prompt logic
│   ├── ingest/         # Document processing and chunking
│   └── api/            # API endpoints
├── scripts/            # Ingestion and maintenance scripts
└── requirements.txt    # Project dependencies
```

## 🚀 Getting Started

### 1. Prerequisites
*   [Ollama](https://ollama.com/) installed and running.
*   Gemma 4 model pulled: `ollama pull gemma4:26b`.

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/areezmuhammed/RAG-NHS.git
cd RAG-NHS

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Ingest Data
Place your clinical PDFs in `data/raw/smpc/` and run:
```bash
python scripts/seed_sample_data.py  # Create sample data
python scripts/ingest.py           # Generate vector index
```

### 4. Run the Brain
```bash
python src/rag/brain.py
```

## ⚠️ Safety Disclaimer

**For Educational Purposes Only.** 
This application is a technical demonstration of RAG capabilities and should **not** be used for clinical decision-making, prescribing, or diagnosis. Always consult a qualified healthcare professional or official NHS/BNF resources for medical advice.

---
*Developed for learning modern AI engineering and clinical safety in RAG systems.*
