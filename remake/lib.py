from datetime import datetime
import threading
import json
import socket
from typing import Union
# SERVER = "127.0.0.1"
SERVER = "192.168.1.83" #home wifi
PORT = 5050
ARTEC_PORT = 6000
CLI_PORT = 7000
CAM_PORT = 8000
ADDR = (SERVER,PORT)
CLI_ADDR = (SERVER,CLI_PORT)
CAM_ADDR = (SERVER,CAM_PORT)
ROBOT_ADDR = (SERVER,ARTEC_PORT)
FORMAT = 'utf-8'
# BUFFER = 2048
HEADER = 64
funlog=True

class msg(object):
    """_summary_
    Example:
        tmp =lib.recvdata(socket)
        message = lib.msg(tmp.cmd,tmp.data)
    Format:
        {"cmd":"string","data":"string"}
    Args:
        object (_type_): _description_
    """    
    def __init__(self,cmd:str,data:str):
        self.cmd = cmd
        self.data = data
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=False)
    
    def getCMD(self)->str:
        return self.cmd
    def getData(self)->str:
        return self.data
        
class connection():
    """
    Description: Inlcude socket obj , ip and port
    Args: socket (socket,(ip,ADDR))
    
    """    
    # 1:  <class 'socket.socket'> <socket.socket fd=372, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 7000), raddr=('127.0.0.1', 58839)>
    # 2:  <class 'str'> 127.0.0.1 <class 'int'> 58839
    def __init__(self,s:socket):
        self.s:socket=s[0]
        self.ip:str = s[1][0]
        self.port:str = s[1][1]
        print(logg(),"New Connction from",self.ip,self.port)
    def update(self,ns:socket):
        self.s = ns[0]
        self.ip = ns[1][0]
        self.port = ns[1][1]
        print(logg(),"Updated Connection with",self.ip)
        
class Robot(object):
    """
        
    """   
    
    def __init__(self, id:str,conn:connection):
        
        self.conn:connection = conn
        self.location = (0,0)
        self.orientation = 0
        self.arindex = id
        self.action = ''
        # sequence -> lt , rt , rb, lb
        self.p1 = (0,0)
        self.p2 = (0,0)
        self.p3 = (0,0)
        self.p4 = (0,0)
        self.CLI_cmd = "Keep Standby"
        print("Added new Robot")
    def setloc(self,locations,orientation): 
    #self = robotobj , locations = list of list , orientation = number
        self.p1 = (locations[0][0],locations[0][1])
        self.p2 = (locations[1][0],locations[1][1])
        self.p3 = (locations[2][0],locations[2][1])
        self.p4 = (locations[3][0],locations[3][1])
        self.location = ((self.p1[0]+self.p3[0])/2,(self.p1[1]+self.p3[1])/2)
        self.orientation = orientation
        print("Loc updated")
    def displayInfo(self):
        print("**********Information**********")
        print("Ar Tag index:     ",self.arindex)
        print("IP address:       ",self.conn.ip,self.conn.port)
        print("Action:           ",self.action)
        print("location:         ",self.location)
        print("orientation:      ",self.orientation)
        
        print("**********Information**********")
        
    # def analyzeCMD(self,message:msg):
        
    #     """
    #     Description:
    #     #pass in msg , analyze cmd(targeted device, if have itself, analyze cmd and decide put what action in box to send)
    #     Args:
    #         msg (_type_): _description_
    #     """ 
        
    #     target = message.getCMD.split(",")
    #     if("-1" in target):
    #         for robot in self.robotlist:
    #             robot.action = message.getData
    #     else:
    #         for id in target:
    #             for robot in self.robotlist:
    #                 if(int(id)==robot.arindex):
    #                     #will change later
    #                     robot.action = message.getData
    # def getRobotList(self):
    #     return self.robotlist
    def clearAction(self):
        self.action=''
    def updateConnection(self,s:socket):
        self.conn= connection(s)
        self.action=''

        
class locInfo(object):
    def __init__(self,index,coordination:list[list],orientation:int):
        self.index = index
        self.coordination = coordination
        self.orientation = orientation
        self.p1 = (0,0)
        self.p2 = (0,0)
        self.p3 = (0,0)
        self.p4 = (0,0)
        

         

#pass in a socket and msg(not byte)
def send(socket:socket,msg):
    """
    Description:Send twice, first is str second is msg object in JSON text
    
    Args:
        socket (socket): _description_
        msg (_type_): _description_
    """    
    message = msg.encode(FORMAT) #turn into binary
    msg_length = len(message)#get msg length
    print('msg length: ',msg_length) # number of char
    send_length = str(msg_length).encode(FORMAT) #turn int length to bin
    send_length += b' ' * (HEADER - len(send_length)) #put space at the end space 
    socket.send(send_length)
    socket.send(message)
    print(logg(),"sent")

    
#get socket received , return string
def recv(socket:socket):
    """_summary_
    Description:
        handle raw byte income
    Args:
        socket (socket): _description_

    Returns:
        _type_: Return in string
    """    
    
    msg_length = socket.recv(HEADER).decode(FORMAT) 
    if msg_length:
        print()
        msg_length = int(msg_length)
        msg = socket.recv(msg_length).decode(FORMAT)
        return msg
    else:
        return False
  

def recvdata(socket:socket)->Union[msg,bool]:
    """
    Description:
        handle raw byte income, reuturn lib.msg object
    Args:
        socket (socket): _description_

    Returns:
        Union[msg,bool]: Return in format of {'cmd':str,'data',str}
    """    
    msg_length = int(socket.recv(HEADER).decode(FORMAT))
    # print(fnlogg(),"read msg_length: ",msg_length)
    if msg_length:
        message = socket.recv(msg_length).decode(FORMAT)
        # print(fnlogg(),"read msg: ",message)
        data = json.loads(message)
        # print(fnlogg(),data)
        print(fnlogg(),'Receiving cmd:',data['cmd'])
        print(logg(),'Receiving data:',data['data'])
        # print(fnlogg(),"Type",type(data))
        data = msg(data['cmd'],data['data'])
        return data
    else:
        return False
    
        
def jsonSend(socket,text): # send JSON with  cmd:host data:unify action
    #print("sent request")
    print()
    print('Execting function: jsonSend.........')
    print('Dumping into JSON text.........')
    mymsg = json.dumps(msg("Host",text).__dict__) #_dict_ send in plaint json text
    print('Sending JSON text.........')
    send(socket,mymsg)
    
def isJson(msg):
    if(json.detect_encoding(msg)):
        data = json.loads(msg)
        return data
    else:
        return msg
        

def showtime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S") + ': '
    return current_time

def showthreadnum():
    return threading.current_thread().ident

def logg():
    s = "%d , %s"%(showthreadnum(), showtime())
    return s

def fnlogg():
    if funlog:
        s = "function log: "
        return s

