import fitz
import re
import json


PDF_PATH = "documents/employee_handbook.pdf"
OUTPUT_PATH = "data/extracted_pages.json"


def clean_text(text):
    """
    Clean extracted PDF text.
    """

    # Remove extra spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove spaces at the beginning and end
    text = text.strip()

    return text


def extract_and_clean_pdf(pdf_path):
    """
    Extract text from every PDF page
    and clean the text.
    """

    document = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document, start=1):

        raw_text = page.get_text()

        cleaned_text = clean_text(raw_text)

        if cleaned_text:
            pages.append({
                "page_number": page_number,
                "text": cleaned_text
            })

    document.close()

    return pages


def save_as_json(data, output_path):
    """
    Save processed data as JSON.
    """

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":

    pages = extract_and_clean_pdf(PDF_PATH)

    save_as_json(pages, OUTPUT_PATH)

    print("✅ PDF processing completed!")
    print(f"✅ Pages extracted: {len(pages)}")
    print(f"✅ Saved to: {OUTPUT_PATH}")