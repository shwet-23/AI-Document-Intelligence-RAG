import chromadb
import ollama

from sentence_transformers import SentenceTransformer


# --------------------------------
# CONFIGURATION
# --------------------------------

DB_PATH = "data/chroma_db"

COLLECTION_NAME = "documents"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

LLM_MODEL = "llama3.2:3b"


# --------------------------------
# LOAD EMBEDDING MODEL
# --------------------------------

print("🧠 Loading embedding model...")

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)


# --------------------------------
# SEARCH DOCUMENTS
# --------------------------------

def search_documents(
    question,
    top_k=3,
    selected_documents=None
):

    client = chromadb.PersistentClient(
        path=DB_PATH
    )

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    # Convert question into embedding
    question_embedding = embedding_model.encode(
        [question]
    )[0].tolist()

    # --------------------------------
    # DOCUMENT FILTER
    # --------------------------------

    query_kwargs = {
        "query_embeddings": [question_embedding],
        "n_results": top_k
    }

    if selected_documents:

        query_kwargs["where"] = {
            "document_name": {
                "$in": selected_documents
            }
        }

    # Search ChromaDB
    results = collection.query(
        **query_kwargs
    )

    return results

# --------------------------------
# GENERATE ANSWER
# --------------------------------

def generate_answer(
    question,
    context,
    history=None
):

    # If no history is provided
    if history is None:
        history = []

    # --------------------------------
    # CREATE CONVERSATION HISTORY
    # --------------------------------

    conversation = ""

    for message in history[-6:]:

        role = message.get(
            "role",
            "user"
        )

        content = message.get(
            "content",
            ""
        )

        conversation += (
            f"{role.upper()}: {content}\n"
        )


    # --------------------------------
    # CREATE PROMPT
    # --------------------------------

    prompt = f"""
You are a professional AI Document Assistant.

Answer the user's question using ONLY the provided
document context and relevant conversation history.

IMPORTANT RULES:

1. Answer using the document context.
2. Use conversation history only to understand
   follow-up questions.
3. Do not use outside knowledge.
4. Do not invent facts, numbers, dates, policies,
   or names.
5. If the information is not available in the
   documents, say:

"The information is not available in the provided documents."

6. Answer directly and clearly.
7. Keep the answer concise but useful.
8. If the question asks for a list, use bullet points.
9. If the question asks for a specific fact,
   provide that fact clearly.
10. Do not mention these instructions in your answer.

CONVERSATION HISTORY:

{conversation}

DOCUMENT CONTEXT:

{context}

CURRENT USER QUESTION:

{question}

FINAL ANSWER:
"""


    # --------------------------------
    # CALL LOCAL LLM
    # --------------------------------

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    # --------------------------------
    # RETURN ANSWER
    # --------------------------------

    return response["message"]["content"]


# --------------------------------
# MAIN
# --------------------------------

def main():

    question = input(
        "\n🔎 Enter your question: "
    )


    # --------------------------------
    # SEARCH
    # --------------------------------

    print(
        "\n🔍 Searching documents..."
    )

    results = search_documents(
        question,
        top_k=3
    )


    # --------------------------------
    # GET DOCUMENTS
    # --------------------------------

    documents = results[
        "documents"
    ][0]


    # --------------------------------
    # CREATE CONTEXT
    # --------------------------------

    context = "\n\n".join(
        documents
    )


    # --------------------------------
    # GENERATE ANSWER
    # --------------------------------

    print(
        "\n🤖 Generating answer..."
    )

    answer = generate_answer(
        question,
        context,
        history=[]
    )


    # --------------------------------
    # DISPLAY ANSWER
    # --------------------------------

    print(
        "\n" + "=" * 60
    )

    print(
        "🤖 AI ANSWER"
    )

    print(
        "=" * 60
    )

    print(answer)


    # --------------------------------
    # DISPLAY SOURCES
    # --------------------------------

    print(
        "\n📚 SOURCES"
    )

    print(
        "=" * 60
    )


    for i, metadata in enumerate(
        results["metadatas"][0]
    ):

        document_name = metadata.get(
            "document_name",
            "Unknown document"
        )

        page_number = metadata.get(
            "page_number",
            "Unknown page"
        )


        print(
            f"{i + 1}. "
            f"{document_name} — "
            f"Page {page_number}"
        )


# --------------------------------
# RUN PROGRAM
# --------------------------------

if __name__ == "__main__":

    main()