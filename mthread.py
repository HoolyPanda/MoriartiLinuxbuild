import threading
import chat
import time
import menu
import signal

class refreshingThread(threading.Thread):
    def __init__(self,chat_to_refresh,timeout):
        threading.Thread.__init__(self)
        self.chat_to_refresh=chat_to_refresh
        self.timeout=timeout
        self.running=True
    def run(self):
        while self.running:
            self.chat_to_refresh.refreshChat()
            time.sleep(self.timeout)
    def _get_chat_name(self):
        return self.chat_to_refresh.chat_name
    def _get_chat_id(self):
        return self.chat_to_refresh.raw_id
    def stop(self):
        print("chat "+str(self.chat_to_refresh.raw_id)+' paused')
        self.running=False
    def unpause(self):
        self.running=True
        print("chat "+str(self.chat_to_refresh.raw_id)+' unpaused')
