import json


INPUT_PATH = "data/extracted_pages.json"
OUTPUT_PATH = "data/chunks.json"


CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def create_chunks(text, chunk_size=500, chunk_overlap=100):
    """
    Split text into overlapping chunks.
    """

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start += chunk_size - chunk_overlap

    return chunks


def process_pages(input_path):

    with open(input_path, "r", encoding="utf-8") as file:
        pages = json.load(file)

    all_chunks = []

    chunk_id = 1

    for page in pages:

        page_number = page["page_number"]
        text = page["text"]

        chunks = create_chunks(
            text,
            CHUNK_SIZE,
            CHUNK_OVERLAP
        )

        for chunk in chunks:

            all_chunks.append({
                "chunk_id": chunk_id,
                "page_number": page_number,
                "text": chunk
            })

            chunk_id += 1

    return all_chunks


def save_chunks(chunks, output_path):

    with open(output_path, "w", encoding="utf-8") as file:

        json.dump(
            chunks,
            file,
            indent=4,
            ensure_ascii=False
        )


if __name__ == "__main__":

    chunks = process_pages(INPUT_PATH)

    save_chunks(chunks, OUTPUT_PATH)

    print("✅ Chunking completed!")
    print(f"✅ Total chunks: {len(chunks)}")
    print(f"✅ Saved to: {OUTPUT_PATH}")