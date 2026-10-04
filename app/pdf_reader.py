import fitz


pdf_path = "documents/employee_handbook.pdf"

document = fitz.open(pdf_path)

print("Number of pages:", len(document))

for page_number, page in enumerate(document):
    text = page.get_text()

    print("\n" + "=" * 50)
    print(f"PAGE {page_number + 1}")
    print("=" * 50)

    print(text)