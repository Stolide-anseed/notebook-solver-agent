from src.preprocessing import preprocess_text
from src.ingestion import extract_text_from_pdf
from src.text_splitter import splitter_text
from src.generator import generator

raw_text = extract_text_from_pdf("data/raw/3_BASIC_ML.pdf")
clean_text = preprocess_text(raw_text).lower()

split_text = splitter_text(clean_text)
print(generator(split_text))