uvicorn app.main:app --reload"# multi-doc-rag" 
What this endpoint does
Accepts file uploads.
Saves the file to UPLOAD_DIR.
Extracts text from:
PDF
DOCX
XLSX
CSV
DWG/DXF (CAD)
Chunks the text.
Generates embeddings.
Stores vectors in your vector database/index.
Returns a success message.