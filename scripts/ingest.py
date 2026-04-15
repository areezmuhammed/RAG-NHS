import os
import json
import logging
from typing import List
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.storage import LocalFileStore
from langchain_classic.storage._lc_store import create_kv_docstore
from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_core.documents import Document

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Paths
BASE_DIR = Path(__file__).parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw" / "smpc"
MANIFEST_PATH = BASE_DIR / "data" / "manifest" / "drugs_master.json"
INDEX_DIR = BASE_DIR / "data" / "indexes" / "faiss"

def ingest_documents():
    # 1. Load Manifest
    if not MANIFEST_PATH.exists():
        logger.error(f"Manifest not found at {MANIFEST_PATH}")
        return

    with open(MANIFEST_PATH, 'r') as f:
        drugs_metadata = json.load(f)

    # 2. Setup Splitters (Hierarchical/Surgical Approach)
    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    child_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)

    # 3. Setup Embeddings
    logger.info("Initializing Embeddings (BGE-Large)...")
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")
    
    # 4. Setup Storage for parent documents (Must be wrapped for LocalFileStore to handle Document objects)
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    fs = LocalFileStore(str(INDEX_DIR / "parent_store"))
    store = create_kv_docstore(fs)

    # 5. Initialize FAISS with a dummy document to set dimension
    # This is required because FAISS needs to know the vector dimension before adding documents
    dummy_doc = Document(page_content="initialization", metadata={"id": "dummy"})
    vectorstore = FAISS.from_documents([dummy_doc], embeddings)
    
    # 6. Setup Parent Document Retriever
    retriever = ParentDocumentRetriever(
        vectorstore=vectorstore,
        docstore=store,
        child_splitter=child_splitter,
        parent_splitter=parent_splitter,
    )

    # 7. Process Files (PDF or TXT)
    processed_count = 0
    for drug in drugs_metadata:
        pdf_path = RAW_DATA_DIR / drug['filename']
        txt_path = RAW_DATA_DIR / drug['filename'].replace('.pdf', '.txt')
        
        target_path = pdf_path if pdf_path.exists() else (txt_path if txt_path.exists() else None)
        
        if not target_path:
            # Silent skip for drugs we haven't seeded yet
            continue

        try:
            logger.info(f"Processing {drug['drug_name']} from {target_path.suffix}...")
            if target_path.suffix == '.pdf':
                loader = PyPDFLoader(str(target_path))
            else:
                loader = TextLoader(str(target_path))
                
            docs = loader.load()
            
            # Attach metadata to all docs
            for doc in docs:
                doc.metadata.update({
                    "drug_name": drug['drug_name'],
                    "category": drug['category'],
                    "source_url": drug['source_url']
                })

            # Add documents to the retriever (handles hierarchical splitting)
            retriever.add_documents(docs)
            processed_count += 1
            
        except Exception as e:
            logger.error(f"Error processing {drug['drug_name']}: {str(e)}")

    if processed_count > 0:
        # 8. Save the Index
        logger.info(f"Saving FAISS index to {INDEX_DIR}")
        vectorstore.save_local(str(INDEX_DIR))
        logger.info("Ingestion complete.")
    else:
        logger.info("No seeded documents (Warfarin/Aspirin) were found. Please run seed_sample_data.py first.")

if __name__ == "__main__":
    ingest_documents()
