import ollama


response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "user",
            "content": "Explain RAG in simple words."
        }
    ]
)


print("\n🤖 AI RESPONSE:")
print(response["message"]["content"])