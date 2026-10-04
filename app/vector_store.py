import json
import chromadb


EMBEDDINGS_PATH = "data/embeddings.json"
DB_PATH = "data/chroma_db"


def load_embeddings():

    with open(EMBEDDINGS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def create_vector_database(data):

    client = chromadb.PersistentClient(
        path=DB_PATH
    )

    collection = client.get_or_create_collection(
        name="documents"
    )

    ids = []
    embeddings = []
    documents = []
    metadatas = []

    for item in data:

        ids.append(str(item["chunk_id"]))

        embeddings.append(item["embedding"])

        documents.append(item["text"])

        metadatas.append({
            "page_number": item["page_number"]
        })

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )

    return collection


if __name__ == "__main__":

    print("📚 Loading embeddings...")

    data = load_embeddings()

    print(f"✅ Loaded {len(data)} embeddings")

    print("🗄️ Creating vector database...")

    collection = create_vector_database(data)

    print("✅ Vector database created!")

    print(
        f"✅ Total documents stored: {collection.count()}"
    )