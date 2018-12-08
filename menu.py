import threading
import time

class menuThread(threading.Thread):
    def __init__(self,command,timeout):
        threading.Thread.__init__(self)
        #self.name=name
        #self.t_id=t_id
        self.command=command
        self.timeout=timeout
        self.running=True
    def run(self):
       while True:
            self.command= input("urcommand ")
            if self.command=='1':
                print('cmd1\n')
                
            elif self.command=='0':
                print('cmd0\n')