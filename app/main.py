import os
import sys
import subprocess

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field

from app.rag_local import (
    search_documents,
    generate_answer
)


# --------------------------------
# CONFIGURATION
# --------------------------------

DOCUMENTS_FOLDER = "documents"


# --------------------------------
# CREATE FASTAPI APP
# --------------------------------

app = FastAPI(
    title="AI Document Intelligence API",
    description="RAG-based AI Document Question Answering API",
    version="1.0.0"
)


# --------------------------------
# REQUEST MODEL
# --------------------------------

class QuestionRequest(BaseModel):

    question: str

    history: list[dict] = Field(
        default_factory=list
    )

    selected_documents: list[str] = Field(
        default_factory=list
    )


# --------------------------------
# HOME
# --------------------------------

@app.get("/")
def home():

    return {
        "message": "AI Document Intelligence API is running!"
    }


# --------------------------------
# HEALTH CHECK
# --------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "AI Document Intelligence"
    }


# --------------------------------
# GET DOCUMENTS
# --------------------------------

@app.get("/documents")
def get_documents():

    documents = []

    if not os.path.exists(DOCUMENTS_FOLDER):

        return {
            "documents": []
        }

    for filename in os.listdir(
        DOCUMENTS_FOLDER
    ):

        if filename.lower().endswith(".pdf"):

            documents.append(filename)

    documents.sort()

    return {
        "documents": documents
    }


# --------------------------------
# UPLOAD PDF
# --------------------------------

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    # Check file extension
    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # Get safe filename
    filename = os.path.basename(
        file.filename
    )

    file_path = os.path.join(
        DOCUMENTS_FOLDER,
        filename
    )

    # Create documents folder if needed
    os.makedirs(
        DOCUMENTS_FOLDER,
        exist_ok=True
    )

    # Save uploaded PDF
    try:

        with open(
            file_path,
            "wb"
        ) as buffer:

            content = await file.read()

            buffer.write(content)

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to save file: {error}"
        )

    # Rebuild vector database
    try:

        subprocess.run(
            [
                sys.executable,
                "app/ingest.py"
            ],
            check=True
        )

    except subprocess.CalledProcessError as error:

        raise HTTPException(
            status_code=500,
            detail=f"Document ingestion failed: {error}"
        )

    return {
        "message": "Document uploaded and processed successfully.",
        "filename": filename
    }


# --------------------------------
# ASK QUESTION
# --------------------------------

@app.post("/ask")
def ask_question(
    request: QuestionRequest
):

    question = request.question.strip()

    # Validate question
    if not question:

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    # Search relevant chunks
    results = search_documents(
        question,
        top_k=3,
        selected_documents=request.selected_documents
    )

    # Combine retrieved chunks
    documents = results["documents"][0]

    context = "\n\n".join(
        documents
    )

    # Generate answer
    answer = generate_answer(
        question,
        context,
        request.history
    )

    # --------------------------------
    # CREATE SOURCES
    # --------------------------------

    sources = []

    seen_sources = set()

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    distances = results.get(
        "distances",
        [[]]
    )[0]

    for i, metadata in enumerate(
        metadatas
    ):

        document_name = metadata.get(
            "document_name",
            "Unknown document"
        )

        page_number = metadata.get(
            "page_number",
            "Unknown"
        )

        # Remove duplicate document + page
        source_key = (
            document_name,
            page_number
        )

        if source_key in seen_sources:

            continue

        seen_sources.add(
            source_key
        )

        # Get distance if available
        distance = None

        if i < len(distances):

            distance = distances[i]

        # Convert distance to simple relevance score
        if distance is not None:

            relevance = max(
                0,
                min(
                    100,
                    round(
                        (1 - distance) * 100,
                        1
                    )
                )
            )

        else:

            relevance = None

        sources.append({

            "document": document_name,

            "page": page_number,

            "relevance": relevance

        })

    # --------------------------------
    # RETURN RESPONSE
    # --------------------------------

    return {

        "question": question,

        "answer": answer,

        "sources": sources

    }