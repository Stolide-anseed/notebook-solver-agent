from src.preprocessing import preprocess_text
from src.ingestion import extract_text_from_pdf
from src.Text-splitter import splitter_text

raw_text = extract_text_from_pdf("data/raw/3_BASIC_ML.pdf")
clean_text = preprocess_text(raw_text)

print(clean_text)