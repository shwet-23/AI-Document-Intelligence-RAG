import os
import fitz
import chromadb

from sentence_transformers import SentenceTransformer


# --------------------------------
# CONFIGURATION
# --------------------------------

DOCUMENTS_FOLDER = "documents"

DB_PATH = "data/chroma_db"

COLLECTION_NAME = "documents"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

CHUNK_SIZE = 500

CHUNK_OVERLAP = 100


# --------------------------------
# LOAD EMBEDDING MODEL
# --------------------------------

print("🧠 Loading embedding model...")

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)


# --------------------------------
# CLEAN TEXT
# --------------------------------

def clean_text(text):

    text = " ".join(text.split())

    return text.strip()


# --------------------------------
# CHUNK TEXT
# --------------------------------

def create_chunks(
    text,
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - chunk_overlap

    return chunks


# --------------------------------
# PROCESS ONE PDF
# --------------------------------

def process_pdf(pdf_path):

    document = fitz.open(pdf_path)

    pdf_name = os.path.basename(pdf_path)

    all_chunks = []

    for page_number, page in enumerate(
        document,
        start=1
    ):

        raw_text = page.get_text()

        cleaned_text = clean_text(raw_text)

        if not cleaned_text:
            continue

        chunks = create_chunks(
            cleaned_text
        )

        for chunk in chunks:

            all_chunks.append({
                "document_name": pdf_name,
                "page_number": page_number,
                "text": chunk
            })

    document.close()

    return all_chunks


# --------------------------------
# LOAD ALL PDFS
# --------------------------------

def process_all_pdfs():

    all_chunks = []

    for filename in os.listdir(
        DOCUMENTS_FOLDER
    ):

        if filename.lower().endswith(".pdf"):

            pdf_path = os.path.join(
                DOCUMENTS_FOLDER,
                filename
            )

            print(
                f"\n📄 Processing: {filename}"
            )

            chunks = process_pdf(
                pdf_path
            )

            print(
                f"✅ Created {len(chunks)} chunks"
            )

            all_chunks.extend(chunks)

    return all_chunks


# --------------------------------
# CREATE VECTOR DATABASE
# --------------------------------

def create_vector_database(chunks):

    client = chromadb.PersistentClient(
        path=DB_PATH
    )

    # Delete old collection
    try:

        client.delete_collection(
            name=COLLECTION_NAME
        )

        print("🗑️ Old collection removed.")

    except Exception:

        pass

    collection = client.create_collection(
        name=COLLECTION_NAME
    )

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    print("\n🧠 Creating embeddings...")

    embeddings = embedding_model.encode(
        texts,
        show_progress_bar=True
    )

    ids = []

    metadatas = []

    for index, chunk in enumerate(chunks):

        ids.append(
            f"chunk_{index + 1}"
        )

        metadatas.append({
            "document_name":
                chunk["document_name"],

            "page_number":
                chunk["page_number"]
        })

    collection.add(

        ids=ids,

        embeddings=[
            embedding.tolist()
            for embedding in embeddings
        ],

        documents=texts,

        metadatas=metadatas
    )

    return collection

def ingest_documents():
    """
    Process all PDFs inside the documents folder
    and rebuild the ChromaDB collection.
    """

    print("\n🚀 Starting document ingestion...")

    chunks = process_all_pdfs()

    if not chunks:
        raise ValueError(
            "No PDF files found inside documents folder."
        )

    print(
        f"\n📚 Total chunks: {len(chunks)}"
    )

    collection = create_vector_database(
        chunks
    )

    print("\n🎉 DOCUMENT INGESTION COMPLETE!")

    return {
        "documents_processed": len(
            set(
                chunk["document_name"]
                for chunk in chunks
            )
        ),
        "total_chunks": collection.count()
    }
# --------------------------------
# MAIN
# --------------------------------

if __name__ == "__main__":

    result = ingest_documents()

    print("\n" + "=" * 60)
    print("📊 INGESTION SUMMARY")
    print("=" * 60)

    print(
        f"📚 Documents: "
        f"{result['documents_processed']}"
    )

    print(
        f"🧩 Chunks: "
        f"{result['total_chunks']}"
    )