def generator(t_q):
    theory_text = "\n".join(t_q.get('theory', [])).strip()
    question_text = "\n".join(t_q.get('question', [])).strip()

    instruction = (
        "Твоя задача — решить задание кодом на Python.\n"
        "Используй теорию ниже, если она помогает решить задачу.\n"
        "Если информации недостаточно, так и напиши: "
        "'Недостаточно данных для точного решения'.\n"
        "Ничего не выдумывай."
    )

    answer_format = (
        "Формат ответа:\n"
        "Задание 1:\n"
        "<решение на Python>"
    )

    full_input = (
        f"{instruction}\n\n"
        f"Теория:\n{theory_text}\n\n"
        f"Задание:\n{question_text}\n\n"
        f"{answer_format}"
    )

    return full_input