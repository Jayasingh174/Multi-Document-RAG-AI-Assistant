# 🚀 Multi-Doc RAG AI Agent

An intelligent Retrieval-Augmented Generation (RAG) system built with FastAPI that allows users to upload multiple document formats, extract content, generate embeddings, store vectors, and perform AI-powered question answering.

## 📌 Features

* Upload and process multiple file formats:

  * PDF
  * DOCX
  * XLSX
  * CSV
  * DWG / DXF (CAD files)

* Automatic text extraction

* Intelligent text chunking

* Embedding generation

* Vector database storage

* Semantic search and retrieval

* FastAPI REST API

* Modular architecture for easy scalability

---

## 🏗️ Project Structure

```text
multi-doc-rag/
│
├── app/
│   ├── routers/
│   │   ├── upload.py
│   │   └── query.py
│   │
│   ├── services/
│   │   ├── pdf_service.py
│   │   ├── docx_service.py
│   │   ├── csv_service.py
│   │   ├── excel_service.py
│   │   ├── cad_ai_service.py
│   │   ├── chunk_service.py
│   │   ├── embedding_service.py
│   │   └── vector_service.py
│   │
│   ├── config.py
│   └── main.py
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Jayasingh174/multi-doc-rag.git
cd multi-doc-rag
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key
UPLOAD_DIR=uploads
VECTOR_DB_PATH=vectorstore
```

---

## ▶️ Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

API Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 📤 Upload Endpoint

### Upload Documents

```http
POST /upload
```

Supported file types:

* PDF
* DOCX
* XLSX
* CSV
* DWG
* DXF

Response:

```json
{
  "message": "file processed successfully"
}
```

---

## 🔍 Query Endpoint

### Ask Questions

```http
POST /query
```

Example Request:

```json
{
  "question": "What are the key requirements mentioned in the uploaded documents?"
}
```

---

## 🧠 Workflow

1. Upload document
2. Extract text
3. Chunk content
4. Generate embeddings
5. Store vectors
6. Retrieve relevant chunks
7. Generate AI response

---

## 🛠 Tech Stack

* FastAPI
* Python
* OpenAI
* Vector Database
* Pandas
* PyMuPDF
* python-docx
* OpenPyXL
* CAD Processing Libraries

---

## 🚀 Future Improvements

* Multi-agent orchestration
* Hybrid search (Vector + Keyword)
* User authentication
* Document versioning
* Cloud deployment
* Conversation memory

---

## 👨‍💻 Author

**Jaya Singh**

GitHub: https://github.com/Jayasingh174

```
```
