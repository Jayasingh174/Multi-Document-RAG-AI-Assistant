from sentence_transformers import SentenceTransformer
import torch
import numpy as np
from app.config import EMBEDDING_MODEL

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

model = SentenceTransformer(EMBEDDING_MODEL, device=DEVICE)


def embed_texts(texts: list[str], batch_size: int = 32) -> np.ndarray:
    # Clean texts
    texts = [t.strip() for t in texts if t.strip()]

    if not texts:
        return np.array([], dtype="float32")

    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=False,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings.astype("float32")


def embed_query(text: str) -> np.ndarray:
    text = text.strip()

    if not text:
        raise ValueError("Query text cannot be empty.")

    embedding = model.encode(
        text,
        show_progress_bar=False,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embedding.astype("float32")