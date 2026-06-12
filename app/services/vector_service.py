import faiss
import numpy as np
import os
import pickle
from app.config import (
    EMBEDDING_DIMENSION,
    INDEX_PATH,
    METADATA_PATH,
    VECTOR_STORE_DIR
)
from app.services.embedding_service import model
EMBEDDING_DIMENSION = model.get_sentence_embedding_dimension()

# Ensure vectorstore directory exists
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

# Global variables
index = None
metadata_store = []


# -------------------------------
# Load or Create FAISS Index
# -------------------------------
def load_index():
    global index, metadata_store

    if os.path.exists(INDEX_PATH):
        try:
            index = faiss.read_index(INDEX_PATH)
            print("✅ FAISS index loaded.")
        except Exception:
            print("⚠ Corrupted index. Creating new one.")
            index = faiss.IndexFlatL2(EMBEDDING_DIMENSION)
    else:
        index = faiss.IndexFlatL2(EMBEDDING_DIMENSION)
        print("🆕 New FAISS index created.")

    # Load metadata
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "rb") as f:
            metadata_store = pickle.load(f)
    else:
        metadata_store = []

# -------------------------------
# Save Index + Metadata
# -------------------------------
def save_index():
    global index, metadata_store

    if index is not None:
        faiss.write_index(index, INDEX_PATH)

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata_store, f)


# -------------------------------
# Add Embeddings to Index
# -------------------------------
def add_to_index(embeddings, chunks, filename):
    global index, metadata_store

    if index is None:
        load_index()

    if embeddings is None or embeddings.size == 0:
        return

    embeddings = np.array(embeddings).astype("float32")

    if embeddings.shape[1] != EMBEDDING_DIMENSION:
        raise ValueError("Embedding dimension mismatch")

    faiss.normalize_L2(embeddings)
    index.add(embeddings)

    for chunk in chunks:
        metadata_store.append({
            "text": chunk,
            "source": filename
        })

    save_index()
    print(f"✅ Added {len(chunks)} chunks from {filename}")


# -------------------------------
# Search Similar Chunks
# -------------------------------
def search(query_embedding, k=5):
    global index

    if index is None:
        load_index()

    if index.ntotal == 0:
        return []

    query_embedding = np.array([query_embedding]).astype("float32")

    if query_embedding.shape[1] != EMBEDDING_DIMENSION:
        raise ValueError("Query embedding dimension mismatch")

    faiss.normalize_L2(query_embedding)

    D, I = index.search(query_embedding, k)

    results = []
    for idx in I[0]:
        if 0 <= idx < len(metadata_store):
            results.append(metadata_store[idx])

    return results


# -------------------------------
# High-Level RAG Retrieval Helper
# -------------------------------
def retrieve_from_faiss(question, embedding_function, k=5):
    """
    Full retrieval pipeline:
    1. Convert question -> embedding
    2. Search FAISS
    3. Return combined context string
    """

    query_embedding = embedding_function(question)

    results = search(query_embedding, k=k)

    if not results:
        return ""

    context = "\n\n".join([r["text"] for r in results])
    return context


# Initialize on import
load_index()