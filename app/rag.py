import os
import chromadb

from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

DB_PATH = "data/chroma_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)


def search_documents(question, top_k=3):

    chroma_client = chromadb.PersistentClient(
        path=DB_PATH
    )

    collection = chroma_client.get_collection(
        name="documents"
    )

    question_embedding = embedding_model.encode(
        [question]
    )[0].tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
    )

    return results


def generate_answer(question, context):

    prompt = f"""
You are an AI assistant that answers questions
using the provided document context.

Rules:
1. Answer only using the provided context.
2. Do not make up information.
3. If the answer is not available in the context,
   say: "The information is not available in the document."
4. Give a clear and concise answer.

Context:
{context}

Question:
{question}
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text


def main():

    question = input(
        "\n🔎 Enter your question: "
    )

    results = search_documents(question)

    documents = results["documents"][0]

    context = "\n\n".join(documents)

    answer = generate_answer(
        question,
        context
    )

    print("\n" + "=" * 60)
    print("🤖 AI ANSWER")
    print("=" * 60)

    print(answer)

    print("\n📚 SOURCES")

    for i, metadata in enumerate(
        results["metadatas"][0]
    ):
        print(
            f"- Result {i + 1}: "
            f"Page {metadata['page_number']}"
        )


if __name__ == "__main__":
    main()