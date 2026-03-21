from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

def generator():
    class ResearchRespons(BaseModel):
        question: str
        summary: str
        sources: list[str]
        tools_used: list[str]

    parser = PydanticOutputParser(pydantic_object=ResearchRespons)


    prompt = ChatPromptTemplate.from_messages(
        [
            f"""
            Ты AI-agent, который решает учебные задания кодом на Python.

            Верни ответ СТРОГО в формате JSON:

            {{
              "status": "solved" | "search_needed" | "ask_user",
              "python_solution": "",
              "explanation": "",
              "search_query": "",
              "question_for_user": ""
            }}

            Правила:
            1. Если задачу можно решить:
               - status = "solved"
               - заполни python_solution
               - кратко заполни explanation
               - search_query и question_for_user оставь пустыми

            2. Если нужна теория, алгоритм или другая внешняя информация:
               - status = "search_needed"
               - explanation = чего не хватает
               - search_query = что искать в интернете
               - python_solution и question_for_user оставь пустыми

            3. Если не хватает данных из условия, и это надо уточнить у пользователя:
               - status = "ask_user"
               - explanation = чего именно не хватает
               - question_for_user = что нужно уточнить
               - python_solution и search_query оставь пустыми

            4. Не выдумывай факты.
            5. Не добавляй никакого текста вне JSON.
            6. Если можешь решить задачу, выдай полный код на Python.
            7. Делай одно задание = одно решение
            8. Делай решения максимально короткими

            Задание:
                Решение
            Ответ:            
            """
        ]
    ).partial(format_instructions=parser.get_format_instructions())

    return prompt



