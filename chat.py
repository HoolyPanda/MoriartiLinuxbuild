# !/usr/bin/python 
# coding: utf-8
import vk_api
import time
import calc
class Chat:
    def __init__(self, chat_id, session, ids_to_aware=[160500068,415107757,489188026]):
        self.users_last_msg_id = []
        self.session = session
        self.ids_to_aware = ids_to_aware
        self.length=3
        self.raw_chat = session.method('messages.getChat',
                                       {
                                           'chat_id': chat_id
                                       })
        self.chat_users = self.raw_chat.get('users')
        self.chat_name = self.raw_chat.get('title')
        self.users_msg_ids = dict.fromkeys(self.chat_users, None)
        self.raw_id = chat_id
        self.chat_id = 2000000000+chat_id
        self.Judge = calc.IndexCalc(self.chat_name)
        self.last_message_id = 0
        self.last_message_author = 0
        self.ladder_length = 1
        self.running = True
        self.ladder_msgs_ids = ''
        self.bg_id = 0
        self.gettingBG = False

    def getCurrentTime(self):
        return (time.ctime(time.time()))

    def getBadGuyPage(self, bad_guy_id):
        conversation_members_profiles = self.session.method("messages.getConversationMembers", {
            'peer_id': self.chat_id,
            'fields': "domain"
        }).get('profiles')
        print("ready to get bg")
        for member in conversation_members_profiles:
            if member.get('id') == bad_guy_id:
                print('updating text')
                text = '*' 
                text+= member.get('domain')
                a=' подозревается в незаконном использовании лестниц '  
                text+=a#.decode('utf-8')
                a="вот здесь: "
                text+=a#.decode('utf-8')
                text=text+self.chat_name
                text=text+'\n' 
                a="Соотношение знаков препинания к буквам="
                text+=a#.decode('utf-8')
                text=text+self.Judge.analize1()
                #print(text)
                print("sending messages")
                self.sendAllMessages(text)
                print("going offline")
                self.session.method('account.setOffline')
                self.ladder_msgs_ids = ''
                self.bg_id = 0
                print('Bad guy detected '+self.getCurrentTime())

    def sendAllMessages(self, text):
        for id_to_aware in self.ids_to_aware:
            try:
                self.sendMessage(id_to_aware, text, self.ladder_msgs_ids)
            except:
                print("woops")

    def get_ids_to_aware(self):
        print(self.ids_to_aware)

    def add_id_to_aware(self):
        try:
            print("Input id to further sending messages:")
            self.ids_to_aware.append(
                int(input()))
            print("Id was added")
        except:
            print("Something whent wrong")

    def remove_id_to_aware(self):
        try:
            print("Input id to remove:")
            self.ids_to_aware.remove(int(input()))
            print("Id was removed")
        except:
            print("Something whent wrong")

    def getAuthorsLastChatMsg(self, user_id, chat_id):
        self.chat_users_data[user_id] = session.method('messages.getHistory',
                                                       {
                                                           'count': 1,
                                                           "peer_id": chat_id,
                                                           'user_id': user_id
                                                       }).get('items')[0].get('id')

    def getChatMsgAuthor(self, msg_id, chat_id):
        return(self.session.method('messages.getHistory',
                                   {
                                       'count': 1,
                                       "peer_id": chat_id,
                                       'user_id': '',
                                       "start_message_id": msg_id
                                   }).get('items')[0].get('from_id'))

    def getLastChatMsgId(self, chat_id):
        return (self.session.method('messages.getHistory',
                                    {
                                        'count': 1,
                                        "peer_id": chat_id
                                    }).get('items')[0])

    def getLastChatMsgId(self, chat_id,message_id):
        return (self.session.method('messages.getHistory',
                                    {
                                        'count': 1,
                                        "peer_id": chat_id,
                                        "start_messge_id":message_id
                                    }).get('items')[0])

    def sendMessage(self, peer_id, text, forward_msg=''):
        self.session.method('messages.send',
                            {
                                'user_id': peer_id,
                                'message': text,
                                'forward_messages': forward_msg
                            })

    def getId(self):
        return self.raw_id

    def addladder_msg_id(self, id, msg):
        if self.ladder_msgs_ids != '':
            self.ladder_msgs_ids += ','
            self.ladder_msgs_ids += str(id)
            self.Judge.updateLog(msg.get('text'))
        else:
            self.ladder_msgs_ids += str(id)
            self.Judge.updateLog(msg.get('text'))

    def getBigLog(self, msg, bg):
        if not self.gettingBG:
            self.bg_id = bg
        if self.ladder_length > self.length:
            self.updateData(msg, bg)
            self.gettingBG = True
            print("You can run, but you cant hide!")
        elif self.ladder_length <= 1 and self.gettingBG:
            self.getBadGuyPage(self.bg_id)
            print('Gotcha!')
            self.gettingBG = False
        else:
            self.updateData(msg, bg)

    def updateData(self, msg, author):
        self.last_message_id = msg.get('id')
        self.last_message_author = author
        self.users_msg_ids[self.last_message_author] = self.last_message_id
        self.addladder_msg_id(self.last_message_id, msg)

    def CheckUsers(self,author:int):
        for user in self.chat_users:
            if user == author:
                return True
        self.users_msg_ids.update({author:None})
        print('Found someone new!')
        return False

    def refreshChat1(self):
        self.last_msg = self.getLastChatMsgId(self.chat_id)
        msg_id = self.last_msg.get('id')
        author = self.last_msg.get('from_id')
        if self.CheckUsers(author):
            if self.last_message_id != msg_id:
                try:
                    if self.users_msg_ids[author] == self.last_message_id:
                        if self.ladder_length > self.length:
                            self.getBigLog(self.last_msg, author)
                        else:
                            log =open('mainlog.log','a',1)
                            self.ladder_length += 1
                            print('current ladder length '+"in chat:" +self.chat_name+" "+str(self.ladder_length))
                            log.write(self.getCurrentTime()+"\n"+'current ladder length '+"in chat:" +self.chat_name+" "+str(self.ladder_length)+"\n")
                            log.close()
                            if self.ladder_length > self.length:
                                self.getBigLog(self.last_msg, author)
                            else:
                                self.getBigLog(self.last_msg, author)
                    else:
                        log =open('mainlog.log','a',1)
                        print("ladder refreshed in chat:"+self.chat_name+'\n'+self.getCurrentTime())
                        log.write(self.getCurrentTime()+"\n"+"ladder refreshed in chat:"+self.chat_name+"\n")
                        log.close()
                        self.ladder_length = 1
                        if not self.gettingBG:
                            self.ladder_msgs_ids = ''
                            self.Judge.clrLog()
                        self.getBigLog(self.last_msg, author)
                except Exception as e:
                    print(e)
                    log =open('mainlog.log','a',1)
                    log.write(self.getCurrentTime()+"\n"+e+"\n")
                    log.close()
        self.session.method('account.setOffline')

    def refreshChat(self,msg_id):
        self.last_msg = self.getLastChatMsgId(self.chat_id,msg_id)
        msg_id = self.last_msg.get('id')
        author = self.last_msg.get('from_id')
        if self.CheckUsers(author):
            if self.last_message_id != msg_id:
                try:
                    if self.users_msg_ids[author] == self.last_message_id:
                        if self.ladder_length > self.length:
                            self.getBigLog(self.last_msg, author)
                        else:
                            log =open('mainlog.log','a',1)
                            self.ladder_length += 1
                            print('current ladder length '+"in chat:" +self.chat_name+" "+str(self.ladder_length))
                            log.write(self.getCurrentTime()+"\n"+'current ladder length '+"in chat:" +self.chat_name+" "+str(self.ladder_length)+"\n")
                            log.close()
                            if self.ladder_length > self.length:
                                self.getBigLog(self.last_msg, author)
                            else:
                                self.getBigLog(self.last_msg, author)
                    else:
                        log =open('mainlog.log','a',1)
                        print("ladder refreshed in chat:"+self.chat_name+'\n'+self.getCurrentTime())
                        log.write(self.getCurrentTime()+"\n"+"ladder refreshed in chat:"+self.chat_name+"\n")
                        log.close()
                        self.ladder_length = 1
                        if not self.gettingBG:
                            self.ladder_msgs_ids = ''
                            self.Judge.clrLog()
                        self.getBigLog(self.last_msg, author)
                except Exception as e:
                    print(e)
                    log =open('mainlog.log','a',1)
                    log.write(self.getCurrentTime()+"\n"+e+"\n")
                    log.close()
        self.session.method('account.setOffline')