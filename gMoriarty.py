"""D."""
import getpass
import io
import json
import os
import select
import sys
import threading
from multiprocessing import Process
import time
import unittest

import vk_api
from requests import exceptions
from vk_api import bot_longpoll
import ancet
import keyboards



my_id = 160500068
groupid = 171435747
main_chat_id = 144
Auts_main_chat_id = 1
in_menu = False
authed = False
chat_id = 151
chat_users = None
threads = {}
chats = []
chats_to_show = 50

ancets = {}

command = ''
main_session = None
session = None
running_menu = True
# main_log = open('mainlog.log', 'w+', 1)
vk = None



class Anceteur():

    def __init__(self):
        self.authed = False
        self.longpollServer = None
        self.cup = 1
        self.token = open('token.token', 'r').readline()
        self.currentAncetOnVoting = None
        self.idToInvite = None
        self.ancetsToSendStack = []


    def auth(self):
        """Authentificate bot as group."""
        try:
            print("You are going to log in as Полигон")
            os.system('clear')
            self.session = vk_api.VkApi(token=self.token)
            self.session._auth_token()
            print("authred")
            vk = self.session.get_api()
            global authed
            self.authed = True
            print('gAut Online')
            self.longpollserver = bot_longpoll.VkBotLongPoll(self.session, 172301854)
            self.gLPS = threading.Thread(target=self.lps, args=(self.session, ), daemon=True)
            return True
        except Exception as e:
            print(e)
            pass


    def lps(self, session):
        for event in bot_longpoll.VkBotLongPoll.listen(self.longpollserver):
            payload = event.raw.get("object").get("payload")
            sender_id = event.raw.get("object").get("from_id")

            if (event.raw.get("object").get("text") == "!ancet" or payload == '{\"command\":\"start\"}'):
                # check if human send an initializing message
                print("Got ank rec")
                ancets.update({sender_id: ancet.Ancet(sender_id)})
                self.Dialog(sender_id, "На какой вопрос анкеты вы хотите ответить?", keybaord=keyboards.ancetKB)
            else:

                if self.CheckQuestion(payload):
                    if keyboards.questions.get(payload) <= 10:
                        ancets.get(sender_id).curQuestion = keyboards.questions.get(payload)
                        ancets.get(sender_id).isGettingData = True
                        self.Dialog(sender_id, ancet.ancetQuestions.get(ancets.get(sender_id).curQuestion), keybaord=keyboards.emptyKb)

                    if self.currentAncetOnVoting is not None:
                        if keyboards.questions.get(payload) == 201:
                            if self.currentAncetOnVoting.checkVoter(sender_id):
                                self.currentAncetOnVoting.Vote(sender_id, True)
                                if not self.currentAncetOnVoting.enoughVotes(self.cup):
                                    print("One voted for YES")
                                else:
                                    self.EndVoting()
                                    print("Voting over")
                            else:
                                self.Dialog(sender_id, "Вы уже голосовали за эту анкету")
                                pass
                        elif keyboards.questions.get(payload) == 200:
                            if self.currentAncetOnVoting.checkVoter(sender_id):
                                self.currentAncetOnVoting.Vote(sender_id, False)
                                if not self.currentAncetOnVoting.enoughVotes(self.cup):
                                    print("One voted for NO")
                                else:
                                    print("Voting over")
                                    self.EndVoting()
                            else:
                                self.Dialog(sender_id, "Вы уже голосовали за эту анкету")
                                pass
                    if self.firstCheck(sender_id, keyboards.questions.get(payload)):  # self.currentAncetOnVoting is None and ancets.get(sender_id).waitingForConferming:
                        if keyboards.questions.get(payload) == 101:
                            ancets.get(sender_id).Conferm()
                            self.Dialog(sender_id, "На какой вопрос анкеты вы хотите ответить?", keybaord=keyboards.ancetKB)
                        elif keyboards.questions.get(payload) == 100:
                            ancets.get(sender_id).waitingForConferming = False
                            ancets.get(sender_id).isGettingData = False
                            self.Dialog(sender_id, "На какой вопрос анкеты вы хотите ответить?", keybaord=keyboards.ancetKB)

                    elif keyboards.questions.get(payload) == 11:
                        if ancets.get(sender_id).GetAncet() is not None:
                            # here should be check if here already onr ancet on voting
                            print(ancets.get(sender_id).GetAncet())
                            ancets.get(sender_id).isOnVoting = True
                            #self.currentAncetOnVoting = ancets.get(sender_id)
                            self.SendAncet(session, ancets.get(sender_id))
                        else:
                            self.Dialog(sender_id, "Кажется, вы не ответили ни на один вопрос. Попробуйте еще раз", keybaord=keyboards.ancetKB)
                        # ancets.pop(sender_id)

                else:
                    if self.currentAncetOnVoting is None or self.currentAncetOnVoting.usr_id != sender_id:
                        if event.chat_id is None and ancets.get(sender_id) is not None:
                            if ancets.get(sender_id).CheckIfQuestionEmpty(event.raw.get("object").get("text")):
                                if ancets.get(sender_id).isGettingData:
                                    ancets.get(sender_id).AppendNData(data=event.raw.get("object").get("text"))
                                self.Dialog(sender_id, "Какой вопрос следующий?", keybaord=keyboards.ancetKB)
                            else:
                                ancets.get(sender_id).waitingForConferming = True
                                self.Dialog(sender_id, "Вы уже отвечали на этот вопрос " + "\n" + ancets.get(sender_id).GetCurrData() + "\n" + "Вы уверены, что хотите перезаписать?", keybaord=keyboards.konfermKb)
            time.sleep(0.1)

    def Dialog(self, usrId: int, message: str, keybaord=None):
        r"""
        Dialog is method to send messges to users.

        usrId: Id to send message
        messge: message to send
        keyboard(not obligatory): keyboard from \'keyboards\' module
        """
        self.session.method("messages.send",
                                            {
                                                "user_id": usrId,
                                                "keyboard": keybaord,
                                                "message": message
                                            })

    def SendAncet(self, session: vk_api.VkApi, ancetToSend):
        self.ancetsToSendStack.append(ancetToSend)
        self.AncetManager()

    def AncetManager(self):
        if len(self.ancetsToSendStack) > 0:
            if self.currentAncetOnVoting is None:
                self.currentAncetOnVoting = self.ancetsToSendStack[0]
                self.session.method("messages.send", {
                                            "chat_id": 1,
                                            "message": self.currentAncetOnVoting.GetAncet(),
                                            "keyboard": keyboards.votingKb
                                        })
                self.ancetsToSendStack.pop(0)
    def CheckQuestion(self, payload: str):
        """Check if this payload compares any of given by keyboard."""
        if keyboards.questions.get(payload) is not None:
            return True
        else:
            return False

    def firstCheck(self, sender_id, payload):
        if (self.currentAncetOnVoting is not None) or payload == 11:
            if ancets.get(sender_id) is not None and ancets.get(sender_id).waitingForConferming:
                return True
            else:
                return False
        else:
            return True

    def EndVoting(self):
        self.session.method("messages.send", {
                                        "chat_id": 1,
                                        "message": "Голосование закончено",
                                        "keyboard": keyboards.emptyKb
                                    })
        if self.currentAncetOnVoting.votedYes >= self.currentAncetOnVoting.votedNo:
            self.idToInvite = self.currentAncetOnVoting.usr_id
            self.session.method("messages.send", {
                                            "user_id": self.currentAncetOnVoting.usr_id,
                                            "message": self.currentAncetOnVoting.congratulations,
                                            "keyboard": keyboards.emptyKb
                                        })
        else:
            self.session.method("messages.send", {
                                            "user_id": self.currentAncetOnVoting.usr_id,
                                            "message": self.currentAncetOnVoting.apolodgise,
                                            "keyboard": keyboards.emptyKb
                                        })
        global ancets
        ancets.pop(self.currentAncetOnVoting.usr_id)
        self.currentAncetOnVoting = None
        self.AncetManager()
        # self.currentAncetOnVoting.isOnVoting = False
