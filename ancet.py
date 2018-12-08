"""Ancet class."""
import keyboards


ancetQuestions = {
                1: "Вопрос 1",
                2: "Вопрос 2",
                3: "Вопрос 3",
                4: "Вопрос 4",
                5: "Вопрос 5",
                6: "Вопрос 6",
                7: "Вопрос 7",
                8: "Вопрос 8",
                9: "Вопрос 9",
                10: "Вопрос 10"
            }

class Ancet():
    def __init__(self, usrId: int):
        self.usr_id = usrId
        self.isGettingData = False
        self.curQuestion = 0
        self.aData = [''] * 10
        self.waitingForConferming = False
        self.prevText = ''
        self.isOnVoting = False
        self.votedIds = []
        self.votedYes = 0
        self.votedNo = 0
        self.congratulations = "Поздравляю со вступлением! Краткие ориентиры - Читайте закрепы в беседах. Правила сообщества - https://vk.com/topic-171435747_41710157 .Архив всех анкет - https://vk.com/topic-171435747_41722112 Тематические беседы размещаются в сообществе на стене. https://m.vk.com/c_athenaeum . Беседа Тупичок Цензора создана исключительно для решения кадровых вопросов. Для всех остальных вопросов есть беседа Экклесиастерий.Право голоса у вас есть сразу по вступлению.Если есть вопросы, можно задавать)"
        self.apolodgise = "Ваша анкета была отклонена. Если вы счиатете, что вас оценили некорректно, то вы можете пройти повтороное испытание, написав короткое эссе на заданную тему. за подробностями пишите https://vk.com/id507494079"
    def AppendNData(self, data: str):
        if self.aData[self.curQuestion - 1] == "":
            self.aData[self.curQuestion -1 ] = data
            self.isGettingData = False
            return True
        else:
            self.prevText = data
            return False

    def Conferm(self):
        self.aData[self.curQuestion] = self.prevText
        self.waitingForConferming = False
        self.isGettingData = False

    def CheckIfQuestionEmpty(self, text: str):
        if self.aData[self.curQuestion - 1] != "" and self.isGettingData:
            self.prevText = text
            return False
        else:
            return True

    def GetCurrData(self):
        return self.aData[self.curQuestion]


    def enoughVotes(self, cup: int):
        if self.votedYes + self.votedNo >= cup:
            return True
        else:
            return False

    def checkVoter(self, voterId: int):
        if len(self.votedIds) > 0:
            for votersId in self.votedIds:
                if votersId != voterId:
                    pass
                else:
                    return False
        return True

    def Vote(self, voterId: int, vote: bool):
        self.votedIds.append(voterId)
        if vote:
            self.votedYes += 1
        else:
            self.votedNo += 1
        pass

    def GetAncet(self):
        """Return sting compiled of ancetquestions."""
        a = ''
        for question in self.aData:
            if question != '':# если все ответы оджинаковые, возвращает первое вхождение, пофиксить
                a += "Вопрос " + str(self.aData.index(question) + 1) + " :" + '\n' + question + '\n'
        if a != '':
            return a
