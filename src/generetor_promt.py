from typing import Literal

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class NotebookSolverResponse(BaseModel):
    status: Literal["solved", "search_needed", "ask_user"] = Field(
        description=(
            "Статус обработки задания: solved, если задачу можно решить прямо сейчас; "
            "search_needed, если для решения критически нужна внешняя теория или поиск; "
            "ask_user, если в условии не хватает данных."
        )
    )
    python_solution: str = Field(
        description=(
            "Полный готовый код на Python без markdown-ограждений. "
            "Заполняется только когда status='solved'."
        )
    )
    explanation: str = Field(
        description=(
            "Краткое и полезное объяснение решения, недостающей теории или причины, "
            "по которой требуется уточнение."
        )
    )
    search_query: str = Field(
        description=(
            "Конкретный поисковый запрос для внешнего поиска. "
            "Заполняется только когда status='search_needed'."
        )
    )
    question_for_user: str = Field(
        description=(
            "Один чёткий вопрос к пользователю для уточнения входных данных. "
            "Заполняется только когда status='ask_user'."
        )
    )

class NotebookSolverBatchResponse(BaseModel):
    results: list[NotebookSolverResponse]


parser = PydanticOutputParser(pydantic_object=NotebookSolverBatchResponse)


def generator() -> str:
    format_instructions = parser.get_format_instructions()

    return f"""
Ты AI-агент, который решает учебные задания из университетской тетрадки.
Твоя задача: по тексту заданий определить, можно ли их решить сразу, и вернуть строго структурированный ответ из всех заданий по очереди.

Контекст работы:
- пользователь отправляет фрагмент задания, извлечённый из PDF;
- если данных достаточно, решай задачу и выдай готовый Python-код;
- если для корректного решения нужна внешняя теория, формула, алгоритм или справочная информация, не выдумывай её;
- если в условии не хватает входных данных или есть неоднозначность, не гадай и запроси одно уточнение.

Формат ответа:
{format_instructions}

Правила:
1. Верни только один JSON-объект без markdown, комментариев и пояснений вне JSON.
2. Всегда заполняй все поля схемы.
3. Для неиспользуемых полей ставь пустую строку "".
4. Если status="solved":
   - python_solution должен содержать полный исполняемый код на Python;
   - explanation должен кратко объяснять идею решения;
   - search_query и question_for_user должны быть пустыми.
5. Если status="search_needed":
   - explanation должен чётко объяснять, какой информации не хватает;
   - search_query должен быть коротким и пригодным для веб-поиска;
   - python_solution и question_for_user должны быть пустыми.
6. Если status="ask_user":
   - explanation должен кратко описывать, каких данных не хватает;
   - question_for_user должен содержать один конкретный вопрос;
   - python_solution и search_query должны быть пустыми.
7. Не добавляй префиксы вроде "Вот JSON:" и не оборачивай код в ```python.
8. Если задачу можно решить на основе школьной/университетской базовой математики и стандартного Python, выбирай status="solved".
9. Делай решение компактным, но корректным.
10. Не выдумывай факты, значения и условия, которых нет во входном тексте.
11. Сделай все задания по порядку(от первого и до последнего)
""".strip()
