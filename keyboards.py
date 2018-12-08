"""Doc string."""

import json
kList = []
questions = {}
for i in range(1, 12):
    questions.update({"{\"button\":\"q" + str(i) + "\"}": i})
questions.update(
                    {
                        "{\"button\":\"conferm\"}": 101,
                        "{\"button\":\"notConferm\"}": 100,
                        "{\"button\":\"voteYes\"}": 201,
                        "{\"button\":\"voteNo\"}": 200
                    })
print(dict(questions))

sAncetKB = {"one_time": True,
            "buttons":
            [
                [{"action": {"type":"text","payload": "{\"button\":\"q1\"}", "label": "На первый вопрос"}, "color": "positive"}, {"action": {"type": "text", "payload": "{\"button\":\"q2\"}", "label": "На второй вопрос"}, "color": "positive"}],
                [{"action":{"type":"text","payload": "{\"button\":\"q3\"}","label": "На третий вопрос"},"color":"positive"},{"action":{"type":"text","payload": "{\"button\":\"q4\"}","label": "На четвертый вопрос"},"color":"positive"}],
                [{"action":{"type":"text","payload": "{\"button\":\"q5\"}","label": "На пятый вопрос"},"color":"positive"},{"action":{"type":"text","payload": "{\"button\":\"q6\"}","label": "На шестой вопрос"},"color":"positive"}],
                [{"action":{"type":"text","payload": "{\"button\":\"q7\"}","label": "На седьмой вопрос"},"color":"positive"},{"action":{"type":"text","payload": "{\"button\":\"q8\"}","label": "На восьмой вопрос"},"color":"positive"}],
                [{"action":{"type":"text","payload": "{\"button\":\"q9\"}","label": "На девятый вопрос"},"color":"positive"},{"action":{"type":"text","payload": "{\"button\":\"q10\"}","label": "На десятый вопрос"},"color":"positive"}],
                [{"action":{"type":"text","payload": "{\"button\":\"q11\"}","label": "Отправить"},"color":"positive"}]
            ]}
sKonfermKb = {"one_time": True,
                "buttons":
                [
                    [{"action": {"type": "text", "payload": "{\"button\":\"conferm\"}", "label": "Да"}, "color": "positive"}, {"action": {"type": "text", "payload": "{\"button\":\"notConferm\"}", "label": "Нет"}, "color": "negative"}]
                ]
    }
sVoitngKb = {"one_time": False,
            "buttons":
            [
                [{"action": {"type": "text", "payload": "{\"button\":\"voteYes\"}", "label": "Да"}, "color": "positive"}, {"action": {"type": "text", "payload": "{\"button\":\"voteNo\"}", "label": "Нет"}, "color": "negative"}]
            ]}
sGKb = {"one_time": True,
        "buttons":
        [
            [{"action":{"type":"text","payload": "{\"button\":\"GreenButton\"}","label": "Red"},"color":"positive"}]
        ]}
sEmptyKb = {"one_time": True,
            "buttons": []
            }

konfermKb = json.dumps(sKonfermKb, ensure_ascii=False)
ancetKB = json.dumps(sAncetKB, ensure_ascii=False)
votingKb = json.dumps(sVoitngKb, ensure_ascii=False)
emptyKb = json.dumps(sEmptyKb, ensure_ascii=False)
GKb = json.dumps(sGKb, ensure_ascii=False)


mainKB = None
