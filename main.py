from src.ingestion.load_document import extract_text_from_pdf
from src.preprocessing.clean_text import preprocess_text

raw_text = extract_text_from_pdf("data/sample.pdf")
clean_text = preprocess_text(raw_text)

print(clean_text[:1000])