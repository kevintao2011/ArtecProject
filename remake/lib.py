from datetime import datetime
import threading
import json
import socket
from typing import Union
import numpy as np
# SERVER = "127.0.0.1"
# SERVER = "192.168.1.83" #home wifi
SERVER = "192.168.1.12" #PC WIFI
# SERVER = "172.20.10.3" #iphone
# SERVER = "192.168.31.36" #XiaoMi
PORT = 5050
ARTEC_PORT = 1000
# CLI_PORT = 7000
CLI_PORT = 2000
CAM_PORT = 3000
GUI_PORT = 4000
ADDR = (SERVER,PORT)
CLI_ADDR = (SERVER,CLI_PORT)
CAM_ADDR = (SERVER,CAM_PORT)
ROBOT_ADDR = (SERVER,ARTEC_PORT)
FORMAT = 'utf-8'
# BUFFER = 2048
HEADER = 64
funlog=True

# key - cmd str , value , #args after : , args seperated by '-'
# Avoid key is substring of other key
cmdlist ={
"dir": 1,
"move to": 2,

}
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
    Description: Inlcude socket obj , ip and port\n
    socket is a tuple of (socket,ip)
    Args: socket (socket,(ip,ADDR))
    
    """    
    # 1:  <class 'socket.socket'> <socket.socket fd=372, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 7000), raddr=('127.0.0.1', 58839)>
    # 2:  <class 'str'> 127.0.0.1 <class 'int'> 58839
    def __init__(self,s:socket):
        self.s:socket=s[0]
        self.ip:str = s[1][0]
        self.port:str = s[1][1]
        self.ping:str = 999
        print(s)
        print('[connection: ]',logg(),"New Connction from",self.ip,self.port)
    def update(self,ns:socket):
        self.s = ns[0]
        self.ip = ns[1][0]
        self.port = ns[1][1]
        print('[connection: ]',logg(),"Updated Connection with",self.ip)
        

class Robot(object):
    """
        
    """   
    robotIDdict = {}
    robotSockDict ={}
    def __init__(self, id:str,conn:connection):
        
        self.conn:connection = conn
        self.location = (0,0)
        self.orientation = 0
        self.arindex = id
        self.action:str = ''
        self.contAction:str = ''
        self.remark:str = ''
        self.handshake:bool = False
        self.continuousActionFlag:bool = False
        # sequence -> lt , rt , rb, lb
        self.p1 = (0,0)
        self.p2 = (0,0)
        self.p3 = (0,0)
        self.p4 = (0,0)
        self.CLI_cmd = "Keep Standby"
        print('[ROBOT: ]',"Added new Robot")
        self.robotIDdict[self.arindex]=self.conn.s
        self.robotSockDict[self.conn.s]=self.arindex
        
    def setloc(self,locations,orientation): 
    #self = robotobj , locations = list of list , orientation = number
        self.p1 = (locations[0][0],locations[0][1])
        self.p2 = (locations[1][0],locations[1][1])
        self.p3 = (locations[2][0],locations[2][1])
        self.p4 = (locations[3][0],locations[3][1])
        self.location = ((self.p1[0]+self.p3[0])/2,(self.p1[1]+self.p3[1])/2)
        self.orientation = orientation
        # print("Loc updated")
    def displayInfo(self):
        print('[ROBOT: ]',"**********Information**********")
        print('[ROBOT: ]',"Ar Tag index:     ",self.arindex)
        print('[ROBOT: ]',"IP address:       ",self.conn.ip,self.conn.port)
        print('[ROBOT: ]',"Action:           ",self.action)
        print('[ROBOT: ]',"location:         ",self.location)
        print('[ROBOT: ]',"orientation:      ",self.orientation)
        
        print('[ROBOT: ]',"**********Information**********")
    def __del__(self):
        self.conn.s.close()
        del self.robotIDdict[self.arindex]
        del self.robotSockDict[self.conn.s]
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
        self.handshake = False #make sure recv new cmd after first handshake
        self.conn= connection(s)
    def startContAction(self,action:str):
        print("changed to cont mode")
        self.contAction = action
        self.continuousActionFlag=True
    def endContAction(self):
        self.contAction = ''
        self.continuousActionFlag=False
    def getContFlag(self):
        return self.continuousActionFlag
    def contAction(self):
        self.action = self.contAction
    
        

        
class locInfo(object):
    def __init__(self,index,coordination:list[list],orientation:int):
        self.index = index
        self.coordination = coordination
        self.orientation = orientation
        self.p1 = (0,0)
        self.p2 = (0,0)
        self.p3 = (0,0)
        self.p4 = (0,0)
        

#------------------SEND FUNCTION--------------#         

#pass in a socket and msg(not byte)
def send(socket:socket.socket,msg):
    """
    Description:Send twice, first is msglength(str) second is bytes
    
    Args:
        socket (socket): _description_
        msg (_type_): _description_
    """    
    message = msg.encode(FORMAT) #turn into binary
    msg_length = len(message)#get msg length
    # print('msg length: ',msg_length) # number of char
    send_length = str(msg_length).encode(FORMAT) #turn int length to bin
    send_length += b' ' * (HEADER - len(send_length)) #put space at the end space 
    try:
        socket.send(send_length)
        socket.send(message)
    except socket.error as error:
        print('[send]',error)
    # print(logg(),"sent")
    
def sendline(socket:socket.socket,msg):
    """
    Description:Send a string with eol char (for handling robot communication)
    
    Args:
        socket (socket): _description_
        msg (_type_): _description_
    """    
    msg=str(msg)+"\n"
    message = msg.encode(FORMAT) #turn into binary
    
    try:
        socket.send(message)
    except socket.error as error:
        print(error)
    # print(logg(),"sent")

def jsonSend(socket,text): # send JSON with  cmd:host data:unify action
    #print("sent request")
    print()
    print('[Jsonsend]','Execting function: jsonSend.........')
    print('[Jsonsend]','Dumping into JSON text.........')
    mymsg = json.dumps(msg("Host",text).__dict__) #_dict_ send in plaint json text
    print('[Jsonsend]','Sending JSON text.........')
    send(socket,mymsg)
    
def isJson(msg):
    if(json.detect_encoding(msg)):
        data = json.loads(msg)
        return data
    else:
        return msg
    
#------------------SEND FUNCTION--------------#  

#------------------RECV FUNCTION--------------#  
#get socket received , return string

def nonblkingRecv(s:socket):
    try:
        data = s.recv(HEADER).decode(FORMAT)
        
    except:
        print('OS error')
    return data

            
def recv(socket:socket.socket):
    """_summary_
    Description:
        Read msg length and msg,handle raw byte income,return UTF-8 string or False (if failed -> should disconnect), with specified msg legth, overread can be eliminated
    Args:
        socket (socket): _description_

    Returns:
        _type_: Return in string
    """    
    # socket.settimeout(0.5)
    print('[lib.recv] timeout ',socket.gettimeout())
    print('[lib.recv] blocking ',socket.getblocking())
    msg_length = socket.recv(HEADER).decode(FORMAT) 
    
    if msg_length:
        
        print(socket.getpeername(),'[lib.recv]message length:', msg_length)
        try:
            msg_length = int(msg_length)
        except:
            print('[lib.recv]no msg length got')
            return msg_length
        try:
            print('[lib.recv]waiting msg')
            msg = socket.recv(msg_length).decode(FORMAT)
            print('[lib.recv]msg: ', msg)
        except:
            print('[lib.recv]no msg got')
            raise OSError
        return msg
    else:
        raise OSError
def recvBytes(socket:socket.socket):
    """_summary_
    Description:
        Read msg length and msg,handle raw byte income,return UTF-8 string or False (if failed -> should disconnect), with specified msg legth, overread can be eliminated
    Args:
        socket (socket): _description_

    Returns:
        _type_: Return in string
    """    
    socket.settimeout(0.5)
    print('[lib.recv] timeout ',socket.gettimeout())
    print('[lib.recv] blocking ',socket.getblocking())
    msg_length = socket.recv(HEADER).decode(FORMAT) 
    
    if msg_length:
        
        print(socket.getpeername(),'[lib.recv]message length:', msg_length)
        try:
            msg_length = int(msg_length)
        except:
            print('[lib.recvBytes]no msg length got')
            return msg_length
        try:
            print('[lib.recvBytes]waiting msg')
            msg = socket.recv(msg_length).decode(FORMAT)
            print('[lib.recvBytes]msg: ', msg)
        except:
            print('[lib.recvBytes]no msg got')
            raise OSError
        return msg
    else:
        raise OSError
def recvForGUI(socket:socket.socket):
    """_summary_
    Description:
        Read msg length and msg,handle raw byte income,return UTF-8 string or False (if failed -> should disconnect), with specified msg legth, overread can be eliminated
    Args:
        socket (socket): _description_

    Returns:
        _type_: Return in string
    """    
    socket.settimeout(0.5)
    print('[lib.recv] timeout ',socket.gettimeout())
    print('[lib.recv] blocking ',socket.getblocking())
    msg_length = socket.recv(HEADER).decode(FORMAT) 
    
    if msg_length:
        
        print(socket.getpeername(),'[lib.recv]message length:', msg_length)
        try:
            msg_length = int(msg_length)
        except:
            print('[lib.recvBytes]no msg length got')
            return msg_length
        try:
            print('[lib.recvBytes]waiting msg')
            msg = socket.recv(msg_length).decode(FORMAT)
            print('[lib.recvBytes]msg: ', msg)
        except:
            print('[lib.recvBytes]no msg got')
            raise OSError
        return msg
    else:
        raise OSError
def recvCAM(socket:socket.socket):
    """_summary_
    Description:
        Read msg length and msg,handle raw byte income,return UTF-8 string or False (if failed -> should disconnect), with specified msg legth, overread can be eliminated
    Args:
        socket (socket): _description_

    Returns:
        _type_: Return in string
    """    
    # socket.settimeout(0.5)
    print('[lib.recvCAM] timeout ',socket.gettimeout())
    print('[lib.recvCAM] blocking ',socket.getblocking())
    msg_length = socket.recv(HEADER).decode(FORMAT) 
    
    if msg_length:
        
        print(socket.getpeername(),'[lib.recvCAM]message length:', msg_length)
        try:
            msg_length = int(msg_length)
        except:
            print('[lib.recvCAM]no msg length got')
            return msg_length
        try:
            print('[lib.recvCAM]waiting msg')
            msg = socket.recv(msg_length).decode(FORMAT)
            print('[lib.recvCAM]msg: ', msg)
        except:
            print('[lib.recvCAM]no msg got')
            raise OSError
        return msg
    else:
        raise OSError
def recvThenAck(s:socket.socket):
    """_summary_
    Description:
        Recv a string and return b'ACK'
    Args:
        socket (socket): _description_

    Returns:
        _type_: Return in string
    """    
    try: 
        print('waiting return ACK')
        data =  s.recv(1024).decode(FORMAT) 
        # print('Send ACK')
        s.send(b'ACK')
        return data
    except:
        print('couldnt decode msg')
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
    msg_length = socket.recv(HEADER).decode(FORMAT)
    # print(fnlogg(),"read msg_length: ",msg_length)
    if msg_length:
        message = socket.recv(int(msg_length)).decode(FORMAT)
        # print(fnlogg(),"read msg: ",message)
        data = json.loads(message)
        print(fnlogg(),data)
        # print(fnlogg(),'Receiving cmd:',data['cmd'])
        # print(logg(),'Receiving data:',data['data'])
        # print(fnlogg(),"Type",type(data))
        data = msg(data['cmd'],data['data'])
        return data
    else:
        return False
    
#------------------RECV FUNCTION--------------#        

def updateLocation(rID,camdata):
    locDict = {}
    
    return locDict

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

# def vectorAngle(p1,p2): #ee 2104
#     p1 = [p1[0]- 1j*(p1[1])]
#     p2 = [p2[0]- 1j*(p2[1])]
#     vector1 = np.array(p1)
#     vector2 = np.array(p2)
#     r = -vector1 - vector2 #from p1 to p2
#     if (int(np.angle(r,True))<0):
#         return 360+int(np.angle(r,True))
#     else:
#         return int(np.angle(r,True))

def vectorAngle(p1,p2): #ee 2104
    # print('p1[0]',p1[0])
    # print('p1[1]',p1[1])
    # print('p2[0]',p2[0])
    # print('p2[1]',p2[1])
    p1 = [p1[0]+ 1j*p1[1]]
    p2 = [p2[0]+ 1j*p2[1]]
    vector1 = np.array(p1)
    vector2 = np.array(p2)
    # r = -vector1 + vector2 #from p1 to p2
    r =  -vector1+vector2 
    # r = np.conjugate(r)
    print(r[0])
    #np angle return The counterclockwise angle from the positive real axis on the complex plane 
    # return int(np.angle(r,True))
    if (int(np.angle(r,True))<0):
        return (450+int(np.angle(r,True)))%360
    else:
        return (90+int(np.angle(r,True)))%360
    
# def handleRobot():
    