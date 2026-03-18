import re
# preprocessing текста
def preprocess_text(text: str) -> str:
    text = text.replace("\x0c", "\n")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\t", " ")

    lines = [line.rstrip() for line in text.split("\n")]

    cleaned_lines = []
    for line in lines:
        line = re.sub(r"[ ]{2,}", " ", line.strip())
        cleaned_lines.append(line)

    text = "\n".join(cleaned_lines)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()