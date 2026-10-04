import chromadb
from sentence_transformers import SentenceTransformer


DB_PATH = "data/chroma_db"
MODEL_NAME = "all-MiniLM-L6-v2"


def search_documents(question, top_k=3):

    model = SentenceTransformer(MODEL_NAME)

    client = chromadb.PersistentClient(
        path=DB_PATH
    )

    collection = client.get_collection(
        name="documents"
    )

    question_embedding = model.encode(
        [question]
    )[0].tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
    )

    return results


if __name__ == "__main__":

    question = input(
        "\n🔎 Enter your question: "
    )

    results = search_documents(question)

    print("\n📚 Relevant information:\n")

    for i in range(len(results["documents"][0])):

        document = results["documents"][0][i]

        page_number = results["metadatas"][0][i]["page_number"]

        distance = results["distances"][0][i]

        print("=" * 60)

        print(f"Result {i + 1}")

        print(f"Page: {page_number}")

        print(f"Distance: {distance}")

        print("\nText:")

        print(document)

    print("=" * 60)