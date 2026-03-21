def splitter_text(text):
    t_q = {
    'question':[]
    }
    quest_o_n = ''
    for indent in text.splitlines():
            if indent.split()[-1] == 'задание':
                quest_o_n = 'question'
            if indent.split()[-1] == 'ответ:':
                quest_o_n = ''
            if quest_o_n != '':
                t_q[quest_o_n].append(indent)
    question_text = "\n".join(t_q.get("question", [])).strip()
    return  question_text