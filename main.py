import vk_api
import time
import chat
from requests import exceptions
import threading
from multiprocessing import Process
import mthread
import menu
import os
import getpass
import io
import sys
import select
import lpserver
import gMoriarty

# motiarty's data https://vk.com/editapp?id=6714083&section=options
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


aut_ancet_archID = 41722112
testArch = 39146311
command = ''
main_session = None
session = None
running_menu = True
main_log = open('mainlog.log', 'w+', 1)
anceteur = None


def auth():
    try:
        lAnceteur = gMoriarty.Anceteur()
        if lAnceteur.auth():
            lAnceteur.gLPS.start()
            a_thr = threading.Thread(target=SendInvite, args=(lAnceteur, ))
            a_thr.start()
            global anceteur
            anceteur = lAnceteur
            print("starting glps")
        print("You are going to log in as Auth Caesar")
        passw = getpass.unix_getpass()
        os.system('clear')
        s = vk_api.VkApi(
            login="89299169802",
            password=passw,
            app_id=6715195
        )
        s.auth(reauth=True)
        global session
        session = s
        global authed
        authed = True
        print('online')
        return True
    except exceptions.SSLError:
        print('SSLError')
        return False
    except exceptions.ConnectionError:
        print('No Connection')
        return False
    except vk_api.exceptions.Captcha as e:
        print('Capcha')
        print(e)
        return False
    except vk_api.exceptions.BadPassword:
        print("Wrong Login or Password")
        return False
    except Exception as e:
        print(e)
        return False

# fdfd

def getChats(session):
    global chats
    chats = []
    HardStart()
    StartLPS(session, chats)


def hearedEnter():
    i, o, e = select.select([sys.stdin], [], [], 0.1)
    for s in i:
        if s==sys.stdin:
            input = sys.stdin.readline()
        return True
    return False


def getChatUsers(chat_id=144):
    chat_users = session.method(
        'messages.getChat',
        {
            'chat_id': (chat_id)
        }).get('users')
    return chat_users


def getChatHistory(chat_id=144, messages_to_return=1, user_id=''):
    chat_id += 2000000000
    last_message = session.method('messages.getHistory',
                                  {
                                      'count': messages_to_return,
                                      "peer_id": chat_id,
                                      'useer_id': user_id
                                  }).get('items')[0]
    return last_message


def StartLPS(session, chats):
    lp = lpserver.LongPollServer(session, chats)
    Lp = threading.Thread(target=lp.LPListen(), name="LP", daemon=True)
    Lp.start()
    print("started LP")


def setOffline():
    return session.method('account.setOffline')


def setOnline():
    return session.method('account.setOnline')


def addNewChat():
    print("type chat id: ")
    new_chat_id = int(input())
    new_chat = chat.Chat(new_chat_id, session)
    chats.append(new_chat)
    new_cthread = mthread.refreshingThread(new_chat, 0.5)
    threads.update({new_chat_id: new_cthread})
    new_cthread.setName(new_chat.chat_name)
    new_cthread.daemon = True
    new_cthread.start()
    print("Added new Chat: " + new_chat.chat_name)


def addNewChat1(new_chat_id: int):
    new_chat = chat.Chat(new_chat_id, session)
    global chats
    chats.append(new_chat)
    print("Added new Chat: " + new_chat.chat_name)


def UpdateConversations():
    print('Current chats to show amount = ' + str(chats_to_show))
    conversations = session.method('messages.getConversations', {"count": chats_to_show})
    for item in conversations.get('items'):
        if item.get('conversation').get('peer').get('type') == 'chat':
            print(str(item.get('conversation').get('chat_settings').get('title')) + ':' + str(item.get('conversation').get('peer').get('local_id')))


def HardStart():
    print('Current chats to show amount = ' + str(chats_to_show))
    conversations = session.method('messages.getConversations', {"count": chats_to_show})
    for item in conversations.get('items'):
        if item.get('conversation').get('peer').get('type') == 'chat':
            print('Add ' + str(item.get('conversation').get('chat_settings').get('title')) + '?(y/n)')
            print("Ans:")
            ans = str(input())
            if ans == "y":
                addNewChat1(item.get('conversation').get('peer').get('local_id'))
            elif ans == "n":
                print('Skipped '+ str(item.get('conversation').get('chat_settings').get('title')))
            elif ans == "br":
                break


def ChangeChatsToShowAmount():
    try:
        print('Current chats to show amount =' + str(chats_to_show))
        print('input new value')
        chats_to_show = int(input())
    except Exception as e:
        print(e)


def mainMenu1():
    while True:
        if hearedEnter():
            command = str(input("type ur command: "))
            if command == 'pauseall':
                for thr in threads.values():
                    thr.stop()
            elif command == 'unpauseall':
                for thr in threads.values():
                    thr.unpause()
            elif command == "addnewchat":
                addNewChat()
            elif command =="updateconversations":
                    UpdateConversations()
            elif command == "stopchat":
                cthread_id = int(input("Enter chat id to stop"))
                try:
                    threads[cthread_id].stop()
                except:
                    print('Woops, something went wrong')
            elif command == "gooffline":
                if setOffline():
                    print("Account is seems like offline")
            elif command == "goonline":
                if setOnline():
                    print("Account is seems like online")
            elif command =='changechatstoshowamount':
                ChangeChatsToShowAmount()
            elif command == "getidlist":
                for thr in threads.values():
                    print("Chat name-"+thr._get_chat_name() +
                          ":id-"+str(thr._get_chat_id()))
            elif command == "getchatidstoaware":
                try:
                    target_chat_id = int(
                        input("Input chat id to add get info:"))
                    threads.get(
                        target_chat_id).chat_to_refresh.get_ids_to_aware()
                except:
                    print("Woops,something goes wrong")
            elif command == "addnewidtosendmessages":
                try:
                    target_chat_id = int(
                        input("Input chat id to add new peer"))
                    threads.get(
                        target_chat_id).chat_to_refresh.add_id_to_aware()
                except:
                    print("Woops,something goes wrong")
            elif command == "removeidtosendmessages":
                try:
                    target_chat_id = int(input("Input chat id to remove peer"))
                    threads.get(
                        target_chat_id).chat_to_refresh.remove_id_to_aware()
                except:
                    print("Woops,something goes wrong")
            elif command == "help":
                print("Here is a list of avalible commands with short discriptions:"+"\n" +
                      "pauseall=>all chat refreshing threads will be paused"+'\n' +
                      "unpauseall=>all chat refreshing threads will be unpaused"+'\n' +
                      'addnewchat=> add new chat to peek at you also will need chat id'+"\n" + '             example:https://vk.com/im?sel=c144 here 144 is chat id it is always goes in the end of URl'+'\n' +
                      "stopchat=> stopps chat. also need chat id"+"\n" +
                      "gooffline=> people will see you offline"+"\n" +
                      "goonline=>people will see you online"+"\n" +
                      "getidlist=>print full list of chats and chat ids bot listening to"
                      )
            else:
                print("invalid command. Type \"help\" to get information about commands")
        time.sleep(0.1)


def main():
    while not authed:
        if auth():
            global anceteur
            print("Aut Online")
            getChats(session)
        else:
            time.sleep(5)


def SendInvite(manceteur):
    print("Readly to invite")
    while True:
        if manceteur.idToInvite is not None:
            try:
                fName = session.method("users.get", {"user_ids":manceteur.idToInvite})[0].get("first_name")
                fName += " "
                fName += session.method("users.get", {"user_ids":manceteur.idToInvite})[0].get("last_name") + '\n'
                session.method("board.createComment", {
                                                        "group_id": 172301854,
                                                        "topic_id": 39146311,
                                                        "message": fName + manceteur.currentAncetOnVoting.GetAncet()
                                                })
                session.method("groups.invite", {
                                                        "group_id": 172301854,
                                                        "user_id": manceteur.idToInvite
                                                })
                manceteur.currentAncetOnVoting = None
                manceteur.isOnVoting = False
                manceteur.idToInvite = None
            except Exception as e:
                print(str(e))
                pass
        else:
            pass
        time.sleep(5)


main()
print("Type \"help\" if you need some")
session.method('account.setOffline')
menuT = threading.Thread(target=mainMenu1(), name="MainMenu", daemon=True)
