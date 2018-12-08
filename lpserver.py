import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
import chat
import time

class LongPollServer():
    def __init__(self,session,chats):
        self.longpollserver=vk_api.longpoll.VkLongPoll(session)
        self.chats_list=chats
        self.main_log=None
        self.session = session
        a=open("log.log","w+",1)
        a.close()

    def LPListen(self):
        try:
            for event in vk_api.longpoll.VkLongPoll.listen(self.longpollserver):
                if True:
                    f=open("log.log","a",1)
                    f.write(time.ctime(time.time())+str(event.raw)+'\n')
                    f.close()
                    if event.raw[0]==4:
                        c=False
                        if event.attachments=={}:
                            event.attachments=event.raw[6]#you should suffer just because ur sutting on Linux
                        if event.attachments.get("source_act")=="chat_invite_user" and c==False:
                            self.AddNewUser(event.chat_id,int(event.attachments.get("source_mid")))
                            c=True
                            pass
                        if event.attachments.get("source_act")=="chat_invite_user_by_link" and c==False:
                            self.AddNewUser(event.chat_id,int(event.attachments.get("from")))
                            c=True
                            pass
                        if event.attachments.get("source_act")=="chat_kick_user" and c==False:
                            self.DelUser(event.chat_id,int(event.attachments.get("source_mid")))
                            c=True
                            pass
                        if event.text != '' and hasattr(event,"chat_id") and c==False:
                            self.AddMessage(event.chat_id,event.user_id,event.message_id,event.text)
                            pass
                        c = False
                time.sleep(0.1)
        except requests.ReadTimeout:
            self.longpollserver.update_longpoll_server()
        except Exception as e:
            self.longpollserver.update_longpoll_server()
            text = "Кажется, я упал"+"\n"+time.ctime(time.time())+"\n"+str(e)
            self.session.method('messages.send',
                            {
                                'user_id': 160500068,
                                'message': text
                            })
    def AddNewUser(self, chat_id,new_user_id):
        for chat in self.chats_list:
            if chat.raw_id==chat_id:
                chat.users_msg_ids.update({new_user_id: None})
                self.main_log = open("mainlog.log", "a", 1)
                self.main_log.write(time.ctime(time.time())+"\n"+'User was added in '+chat.chat_name+"\n")
                self.main_log.close()
                print(time.ctime(time.time()) + "\n" + 'User was added in '+ chat.chat_name)

    def DelUser(self, chat_id: int, user_id: str):
        for chat in self.chats_list:
            if chat.raw_id == chat_id:
                del chat.users_msg_ids[user_id]
                self.main_log = open("mainlog.log","a",1)
                self.main_log.write(time.ctime(time.time())+"\n"+'User was removed in '+chat.chat_name+"\n")
                self.main_log.close()
                print(time.ctime(time.time())+"\n"+'User was removed in '+chat.chat_name)

    def AddMessage(self, chat_id: int, user_id: str, message_id, message):
        for chat in self.chats_list:
            if chat.raw_id == chat_id:
                chat.refreshChat(message_id)
