import os
from dotenv import load_dotenv

load_dotenv()

# Base Directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# App Settings
APP_NAME = os.getenv("APP_NAME", "Local Entrepreneur RAG")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# File Uploads
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

temp_dir = os.path.join(BASE_DIR, "tmp_convert")
os.makedirs(temp_dir, exist_ok=True)

# Embedding (Ollama)
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", 768))

# Retrieval
TOP_K = int(os.getenv("TOP_K", 5))

# Chunking
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 800))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 150))
MIN_CHUNK_LENGTH = int(os.getenv("MIN_CHUNK_LENGTH", 50))

# LLM Settings (Ollama)
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b-instruct-q4_K_M")
OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", 0.7))
OLLAMA_MAX_TOKENS = int(os.getenv("OLLAMA_MAX_TOKENS", 512))

# Vector Store Paths
VECTOR_STORE_DIR = os.path.join(BASE_DIR, "vectorstore")
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

INDEX_PATH = os.path.join(VECTOR_STORE_DIR, "faiss.index")
METADATA_PATH = os.path.join(VECTOR_STORE_DIR, "metadata.pkl")