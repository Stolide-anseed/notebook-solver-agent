def splitter_text(text):
    t_q = {
    'theory':[],
    'question':[]
    }
    i = 'theory'
    for indent in text.splitlines():
        if indent != '':
            if indent.split()[-1] == 'задание':
                i = 'question'
            if indent.split()[-1] == 'ответ:' and len(t_q['question']) != 0:
                break
            t_q[i].append(indent)

    return  t_q