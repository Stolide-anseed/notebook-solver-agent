import os
import json

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import search_tool

from src.generetor_promt import generator, parser
from src.ingestion import extract_text_from_pdf
from src.preprocessing import preprocess_text
from src.text_splitter import splitter_text

from pathlib import Path

load_dotenv()


def _extract_text_from_content(content) -> str:
    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        text_parts = []
        for part in content:
            if isinstance(part, str):
                text_parts.append(part)
                continue

            if isinstance(part, dict) and part.get("type") == "text":
                text_parts.append(part.get("text", ""))

        return "\n".join(part for part in text_parts if part).strip()

    return str(content).strip()


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key='Твой ключ API'
)

raw_text = extract_text_from_pdf("data/raw/3_BASIC_ML.pdf")
clean_text = preprocess_text(raw_text).lower()
question = splitter_text(clean_text)


tools = [search_tool]
system_prompt = generator()
agent = create_agent(model=llm,
                     system_prompt=system_prompt,
                     tools=tools)

raw_response = agent.invoke(
    {
        "messages": [
            SystemMessage(content=system_prompt),
            HumanMessage(
                content=(
                    "Ниже текст заданий из учебной тетрадки.\n"
                    "Проанализируй его и верни ответы строго по заданной JSON-схеме.\n\n"
                    f"{question}"
                )
            ),
        ]
    }
)

text = _extract_text_from_content(raw_response["messages"][-1].content)
structured_response = parser.parse(text)
for item in structured_response.results:
    if item.status == 'ask_user':
        user_answer = input(f"{item.question_for_user}\n> ")
        raw_response = agent.invoke(
            {
                "messages": [
                    SystemMessage(content=system_prompt),
                    HumanMessage(
                        content=(
                            "Вот исходное задание:\n"
                            f"{question}\n\n"
                            "Вот уточнение от пользователя:\n"
                            f"{user_answer}\n\n"
                            "Теперь реши задачу и верни ответ строго по JSON-схеме."
                        )
                    ),
                ]
            }
        )

    output_dir = Path("data/answer")
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "result.json", "a", encoding="utf-8") as f:
        json.dump(item.model_dump(), f, ensure_ascii=False, indent=2)
    if item.status == "solved":
        with open(output_dir / "solution.py", "a", encoding="utf-8") as f:
            f.write(item.python_solution)
