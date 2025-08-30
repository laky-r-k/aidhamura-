from datetime import datetime

class msg:
    def __init__(self,to:str,from_:str,message:str,datetime:datetime):
        self.to=str
        self.from_=from_
        self.message=message
        self.seen=False
        self.time=datetime
    
class user:
    def __init__(self,username,inbox):
        self.username=username
        self.inbox=inbox

class inbox:
    def __init__(self):
        self.box=[]

    def add_msg(self,msg:msg):
        self.box.append(msg)
    def sort(self):
        pass


    