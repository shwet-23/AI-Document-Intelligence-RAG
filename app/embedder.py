import json
from sentence_transformers import SentenceTransformer


INPUT_PATH = "data/chunks.json"
OUTPUT_PATH = "data/embeddings.json"


MODEL_NAME = "all-MiniLM-L6-v2"


def load_chunks(input_path):
    with open(input_path, "r", encoding="utf-8") as file:
        return json.load(file)


def create_embeddings(chunks):
    model = SentenceTransformer(MODEL_NAME)

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    return embeddings


def save_embeddings(chunks, embeddings, output_path):

    results = []

    for chunk, embedding in zip(chunks, embeddings):

        results.append({
            "chunk_id": chunk["chunk_id"],
            "page_number": chunk["page_number"],
            "text": chunk["text"],
            "embedding": embedding.tolist()
        })

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False
        )


if __name__ == "__main__":

    print("📚 Loading chunks...")

    chunks = load_chunks(INPUT_PATH)

    print(f"✅ Loaded {len(chunks)} chunks")

    print("🧠 Creating embeddings...")

    embeddings = create_embeddings(chunks)

    save_embeddings(
        chunks,
        embeddings,
        OUTPUT_PATH
    )

    print("✅ Embeddings created successfully!")
    print(f"✅ Saved to: {OUTPUT_PATH}")