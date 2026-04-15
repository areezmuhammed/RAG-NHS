import os
import logging
from pathlib import Path
from langchain_ollama import OllamaLLM
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.storage import LocalFileStore
from langchain_classic.storage._lc_store import create_kv_docstore
from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
INDEX_DIR = BASE_DIR / "data" / "indexes" / "faiss"

def get_clinical_brain():
    """
    Initializes and returns the Agentic RAG Brain for NHS Drug Interactions.
    Uses Gemma 4's native Thinking Mode to reason through retrieved clinical context.
    """
    
    # 1. Initialize Embeddings (Must match Ingestion)
    logger.info("Loading Embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")
    
    # 2. Load the FAISS Index
    logger.info(f"Loading FAISS Index from {INDEX_DIR}...")
    if not (INDEX_DIR / "index.faiss").exists():
        raise FileNotFoundError("FAISS index not found. Please run scripts/ingest.py first.")
    
    vectorstore = FAISS.load_local(
        str(INDEX_DIR), 
        embeddings, 
        allow_dangerous_deserialization=True
    )
    
    # 3. Load the Parent Document Store
    # This stores the full 2000-token paragraphs for high-context thinking
    fs = LocalFileStore(str(INDEX_DIR / "parent_store"))
    store = create_kv_docstore(fs)
    
    # 4. Reconstruct the Surgical Retriever
    # Note: 2026 update requires splitters for validation even during retrieval.
    child_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    
    retriever = ParentDocumentRetriever(
        vectorstore=vectorstore,
        docstore=store,
        child_splitter=child_splitter, 
        parent_splitter=parent_splitter,
    )

    # 5. Initialize Gemma 4 via Ollama
    # 2026 Feature: 'reasoning=True' extracts the thinking process into metadata.
    logger.info("Connecting to Gemma 4 (Ollama)...")
    llm = OllamaLLM(
        model="gemma4:26b",
        temperature=0.0,  # Zero temperature for deterministic clinical safety
        extra_kwargs={"reasoning": True} # Integrated Thinking Mode
    )

    # 6. Clinical Safety Prompt
    # This prompt instructs the model to use its 'Thinking Channel' to 
    # verify interactions before generating a final response.
    prompt = ChatPromptTemplate.from_template("""
    You are an NHS Clinical Safety Assistant specializing in Drug-Drug Interactions (DDI).
    Your primary goal is to provide evidence-based, educational information grounded IN THE PROVIDED SmPC CONTEXT.

    CONTEXT FROM OFFICIAL SmPC DOCUMENTS:
    {context}

    USER QUERY:
    {question}

    INSTRUCTIONS:
    1. THINK: First, analyze the context for mentions of BOTH drugs or their classes (e.g., Anticoagulants, NSAIDs).
    2. SAFETY: If a major interaction is found, state it clearly at the beginning.
    3. CITATION: Explicitly name which drug monograph the information is coming from.
    4. CAVEAT: Always end with: "This information is for educational purposes and does not replace clinical judgment or official NHS guidelines."

    ASSISTANT RESPONSE:
    """)

    # 7. Assemble the RAG Chain
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain

if __name__ == "__main__":
    # Internal Test
    try:
        brain = get_clinical_brain()
        test_query = "Can a patient on Warfarin take Aspirin?"
        logger.info(f"Running test query: {test_query}")
        
        # In a real app, we would also log 'response.additional_kwargs.get("reasoning_content")'
        # to show the thinking process in the UI.
        response = brain.invoke(test_query)
        
        print("\n" + "="*50)
        print("GENERIC CLINICAL BRAIN OUTPUT")
        print("="*50)
        print(response)
        print("="*50 + "\n")
        
    except Exception as e:
        logger.error(f"Brain failure: {str(e)}")
