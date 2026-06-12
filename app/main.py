from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from contextlib import asynccontextmanager
import os

from app.routers import upload, query
from app.config import APP_NAME, DEBUG, UPLOAD_DIR, VECTOR_STORE_DIR


# ----------------------------
# Lifespan Manager
# ----------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

    print("🚀 Application Starting...")
    yield
    print("🛑 Application Shutting Down...")


# ----------------------------
# Create App
# ----------------------------
app = FastAPI(
    title=APP_NAME,
    debug=DEBUG,
    version="1.0.0",
    description="Multi-Document RAG System with FastAPI + FAISS + Ollama",
    lifespan=lifespan
)

# ----------------------------
# Routers
# ----------------------------
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(query.router, prefix="/query", tags=["Query"])


# ----------------------------
# Serve Frontend
# ----------------------------
app.mount("/static", StaticFiles(directory="app/web"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("app/web/index.html")


# ----------------------------
# Redirect /query → /query/
# ----------------------------
@app.get("/query")
def redirect_query():
    return RedirectResponse(url="/query/")


# ----------------------------
# Health Check
# ----------------------------
@app.get("/health")
def health_check():
    return {"status": "healthy"}