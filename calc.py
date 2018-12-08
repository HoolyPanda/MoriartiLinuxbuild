# !/usr/bin/python
# coding: utf-8

class IndexCalc:
    def __init__(self, chat_name):
        self.text_log = ''
        self.chat_name=chat_name
        a='.log'
        self.text_log_file=open(self.chat_name+'.log','w+',1)
        self.total_caracters=0
        self.total_dots=0
        self.total_commas=0
        self.total_plings=0
        self.total_question_marks=0

    def updateLog(self, text):
        self.text_log_file= open(self.chat_name+'.log','a',1)
        self.text_log_file.write(text+'\n')
        self.text_log_file.close()
    
    def analize1(self):
        self.text_log_file= open(self.chat_name+'.log','r',1)
        for line in self.text_log_file.readlines():
            self.total_caracters+=len(line.replace('\n',''))
            self.total_dots += line.count('.')
            self.total_commas += line.count(',')
            self.total_plings += line.count('!')
            self.total_question_marks += line.count('?')
            print (line,)
        self.total_caracters = self.total_caracters -(self.total_commas+self.total_dots+self.total_plings+self.total_question_marks)
        print("total_letters "+str(self.total_caracters))
        print("total_dots "+str(self.total_dots))
        print("total_commas "+str(self.total_commas))
        print("total_plings "+str(self.total_plings))
        print("total_question_marks "+str(self.total_question_marks))
        self.text_log_file.close()
        if self.total_caracters==0:
            self.total_caracters=1
        return ' %f' % ((self.total_commas+self.total_plings+self.total_question_marks+self.total_dots)/self.total_caracters)

    def analize(self):
        try:
            print("strarted analyse")
            self.text_log = self.text_log.replace('\n','')
            print(self.text_log)
            total_caracters = len(self.text_log)
            total_dots = self.text_log.count('.')
            total_commas = self.text_log.count(',')
            total_plings = self.text_log.count('!')
            total_question_marks = self.text_log.count('?')
            total_caracters = total_caracters - \
                (total_commas+total_dots+total_plings+total_question_marks)
            print("total_letters "+str(total_caracters))
            print("total_dots "+str(total_dots))
            print("total_commas "+str(total_commas))
            print("total_plings "+str(total_plings))
            print("total_question_marks "+str(total_question_marks))
            if total_caracters == 0:
                total_caracters = 1
            return ' %f' % ((total_commas+total_dots+total_plings+total_question_marks+total_dots)/total_caracters)
        except:
            print('woops')

    def clrLog(self):
        self.text_log_file= open(self.chat_name+'.log','w',1)
        self.text_log_file.write('')
        self.text_log_file.close()
        self.total_caracters=self.total_commas=self.total_dots=self.total_plings=self.total_question_marks=0
        self.text_log = ''