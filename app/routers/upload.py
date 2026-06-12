from fastapi import APIRouter, UploadFile, File
import shutil
import os

from app.config import UPLOAD_DIR

from app.services.pdf_service import extract_text as extract_pdf
from app.services.docx_service import extract_text as extract_docx
from app.services.csv_service import extract_text as extract_csv
from app.services.excel_service import extract_text as extract_excel
from app.services.cad_ai_service import CADExtractor

from app.services.chunk_service import chunk_text
from app.services.embedding_service import embed_texts
from app.services.vector_service import add_to_index

router = APIRouter()


@router.post("/")
async def upload_file(file: UploadFile = File(...)):

    if UPLOAD_DIR is None:
        raise ValueError("UPLOAD_DIR must be configured")

    upload_dir = str(UPLOAD_DIR)
    file_path = os.path.join(upload_dir, file.filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Detect file type

    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        text = extract_pdf(file_path)

    elif filename.endswith(".docx"):
        text = extract_docx(file_path)

    elif filename.endswith(".xlsx"):
        text = extract_excel(file_path)

    elif filename.endswith(".csv"):
        text = extract_csv(file_path)

    elif filename.endswith((".dwg", ".dxf")):
        cad = CADExtractor(file_path)
        text = cad.extract_all()

    else:
        return {"error": "Unsupported file format"}
    if not text.strip():
        return {"error": "No text extracted from the file"}

    # Chunk → Embed → Store
    chunks = chunk_text(text)
    embeddings = embed_texts(chunks)

    add_to_index(
        embeddings=embeddings,
        chunks=chunks,
        filename=file.filename
    )

    return {"message": f"{file.filename} processed successfully"}