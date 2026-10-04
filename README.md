# 🤖 AI Document Intelligence & RAG Automation

AI-powered document question-answering system that allows users to upload PDF documents and interact with them using Retrieval-Augmented Generation (RAG).

The system extracts text from PDF documents, creates semantic embeddings, stores them in ChromaDB, retrieves relevant document sections, and generates answers using Llama 3.2 through Ollama.

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
