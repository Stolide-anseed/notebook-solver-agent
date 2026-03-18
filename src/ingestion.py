import pymupdf
# изменяет текст из pdf в txt и сохраняет его
def extract_text_from_pdf(pdf_file: str) -> str:
    doc = pymupdf.open(pdf_file)
    pages = []

    for page in doc:
        pages.append(page.get_text())

    doc.close()
    return "\n\n".join(pages)