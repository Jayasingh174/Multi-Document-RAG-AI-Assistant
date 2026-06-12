from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import CHUNK_SIZE, CHUNK_OVERLAP


splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=[
        "\n\n",
        "\n",
        ". ",
        "; ",
        ", ",
        " "
    ],
)


def chunk_text(text: str) -> list[str]:
    """
    Split text into chunks suitable for embeddings.
    Works well for documents, tables, and CAD outputs.
    """

    if not text or not text.strip():
        return []

    chunks = splitter.split_text(text)

    cleaned_chunks = []

    for chunk in chunks:

        chunk = chunk.strip()

        if not chunk:
            continue

        # Allow CAD-style structured chunks
        if len(chunk) < 30 and ":" not in chunk:
            continue

        cleaned_chunks.append(chunk)

    return cleaned_chunks