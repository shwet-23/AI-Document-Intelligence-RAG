# 🤖 AI Document Intelligence & RAG Automation

AI-powered document question-answering system that allows users to upload PDF documents and interact with them using Retrieval-Augmented Generation (RAG).

The system extracts text from PDF documents, cleans and chunks the content, creates semantic embeddings, stores them in ChromaDB, retrieves relevant document sections, and generates answers using Llama 3.2 through Ollama.

---

## 🚀 Features

- 📄 PDF document processing
- 🧹 Text extraction and cleaning
- ✂️ Intelligent text chunking
- 🧠 Semantic embeddings
- 🗄️ ChromaDB vector database
- 🔎 Semantic document search
- 🤖 Llama 3.2 local LLM
- 🔗 Retrieval-Augmented Generation (RAG)
- 💬 Conversational document chat
- 📚 Multiple document selection
- 📌 Source document and page references
- 📊 Relevance indicators
- ⚡ FastAPI backend
- 🎨 Streamlit frontend
- 📤 PDF upload and automatic ingestion

---

## 🏗️ Architecture

```text
                    ┌───────────────────┐
                    │     User / UI     │
                    │    Streamlit      │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │     FastAPI       │
                    │      Backend      │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   User Question   │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Embedding Model   │
                    │ all-MiniLM-L6-v2  │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │    ChromaDB       │
                    │ Vector Database   │
                    └─────────┬─────────┘
                              │
                         Relevant Chunks
                              │
                              ▼
                    ┌───────────────────┐
                    │   RAG Context     │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │    Llama 3.2      │
                    │      Ollama       │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Answer + Sources  │
                    └───────────────────┘

🔄 RAG Pipeline

PDF Document
     ↓
Text Extraction
     ↓
Text Cleaning
     ↓
Text Chunking
     ↓
Embedding Generation
     ↓
ChromaDB Vector Storage
     ↓
Semantic Search
     ↓
Relevant Document Chunks
     ↓
RAG Context
     ↓
Llama 3.2
     ↓
AI Generated Answer
     ↓
Source + Page References


🛠️ Tech Stack

Programming
- Python

AI / Machine Learning
- Sentence Transformers
- all-MiniLM-L6-v2
- Retrieval-Augmented Generation (RAG)
- Llama 3.2

Vector Database
- ChromaDB

Backend
- FastAPI
- Uvicorn

Frontend
- Streamlit

Document Processing
- PyMuPDF

Local AI
- Ollama

Development Tools
- Git
- GitHub
- VS Code
- PowerShell

📁 Project Structure

AI-Document-Intelligence-RAG/
│
├── app/
│   ├── __init__.py
│   ├── chunker.py
│   ├── embedder.py
│   ├── ingest.py
│   ├── main.py
│   ├── ollama_test.py
│   ├── pdf_reader.py
│   ├── rag.py
│   ├── rag_local.py
│   ├── search.py
│   ├── text_processor.py
│   └── vector_store.py
│
├── frontend/
│   └── app.py
│
├── documents/
│
├── screenshots/
│   ├── dashboard.png
│   ├── chat.png
│   ├── multiple-documents.png
│   └── api.png
│
├── requirements.txt
├── .gitignore
└── README.md
