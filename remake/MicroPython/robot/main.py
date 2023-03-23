# main.py
print('-------start main script-------')



# compass = StuduinoBitCompass ()
# compassReading = compass.heading()
# if(button_b.is_pressed):
#     compass.calibrate()

#-----------------------------IMPORTS----------------------------#
from pystubit.image import StuduinoBitImage
from pystubit.sensor import StuduinoBitCompass
from pystubit.button import StuduinoBitButton
from pystubit.dsply import StuduinoBitDisplay
from pyatcrobo2.parts import DCMotor

import time
import _thread
import json
import socket
import network
import utime
import os

import machine
import pyatcrobo2


#-----------------------------IMPORTS------------------------------------------#

# ----------------------------CONSTANTS-----------------------#
HEADER = 64
PORT = 1000
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
# SERVER = "192.168.1.17"
# SERVER = "10.22.1.126"
SERVER = "192.168.31.36" #Xiaomi
# Server = "127.0.0.1"
# SERVER = "192.168.1.83"  # home wifi
# SERVER = "192.168.1.12"  # home desktop
f = open('config.json')
config = json.load(f)
ROBOTID = config['arID']
ADDR = (SERVER, PORT)
# SSID = 'NETGEAR76'
# WIFIPW = 'quiettulip014'

SSID = 'Test'
WIFIPW = '12345678'
#ADDR = ('192.168.1.83', 6000)

# ----------------------------CONSTANTS-----------------------#

#-----------------------------ARTEC HARDWARE CONFIG----------------------------#
try:
    L = DCMotor('M1')
    R = DCMotor('M2')
    L.power(0)
    R.power(0)
    L.stop()
    R.stop()
except:
    print('motor is not installed on M1 and M2!')

display = StuduinoBitDisplay()
display.on()

button_a = StuduinoBitButton('A')
button_b = StuduinoBitButton('B')
#-----------------------------ARTEC HARDWARE CONFIG----------------------------#



#-----------------------------DEFIND CLASS------------------------------#
class msg:
    def __init__(self, cmd, data):
        self.cmd = cmd
        self.data = data
        
#-----------------------------DEFIND CLASS------------------------------#



# -------------------------------CMD Action-------------------#
#pass in a socket and msg(not byte)
def sendBytes(socket:socket.socket,msg):
    """
    Description:Send twice, first is msglength(str) second a string in UTF-8
    
    Args:
        socket (socket): _description_
        msg (_type_): _description_
    """    
    
    print('[Function sendBytes]send msg: ',msg)    
    
    #send message length
    msg = str(msg)
    msg_length = len(msg)#get msg length
    print('[Function sendBytes]send meg_length: ',msg_length)
    # print('msg length: ',msg_length) # number of char
    send_length = str(msg_length).encode(FORMAT) #turn int length to bin
    send_length += b' ' * (HEADER - len(send_length)) #put space at the end space 
    try:
        socket.send(send_length)
    except OSError() as error:
        print(error)
        socket.close()
        print('[ERROR]failed to send msg length, closed socket')
        
    #send data    
    try:
        message = msg.encode(FORMAT) #turn into binary
        print('[Function sendBytes] send message:',message)
        socket.send(message)
    except OSError() as error:
        print(error)
        print('[ERROR]failed to send msg, closed socket ')
        socket.close()
        
    # print(logg(),"sent")
def sendLine(socket:socket.socket,msg):
    """
    Description:Send twice, first is msglength(str) second is msg object in JSON text , with eol char
    
    Args:
        socket (socket): _description_
        msg (_type_): _description_
    """    
    msg=msg+"\n"
    message = msg.encode(FORMAT) #turn into binary
    
    try:
        socket.send(message)
    except socket.error as error:
        print(error)
    # print(logg(),"sent")
    
def recvdata(socket: socket):
    """
    Description:
        handle raw byte income, reuturn lib.msg object
    Args:
        socket (socket): _description_

    Returns:
        Union[msg,bool]: Return in format of {'cmd':str,'data',str}
    """
    msg_length = socket.recv(HEADER).decode(FORMAT)
    #print("read msg_length: ",msg_length)

    if msg_length:
        message = socket.recv(int(msg_length)).decode(FORMAT)
        #data = json.loads(message)
        print('message',message)
        return message
    else:
        #print("Fail to recv data")
        return False
#get socket received , return string
def recv(socket:socket.socket):
    """_summary_
    Description:
        handle raw byte income,return UTF-8 string or False (if failed -> should disconnect), with specified msg legth, overread can be eliminated
    Args:
        socket (socket): _description_
    Returns:
        _type_: Return in string
    """    
    
    msg_length = socket.recv(HEADER).decode(FORMAT) 
    
    if msg_length:
        try:
            msg_length = int(msg_length)
        except:
            return msg_length
        msg = socket.recv(msg_length).decode(FORMAT)
        msg.strip()
        # msg.lstrip(' ')
        print('msg: ', msg)
        return msg
    else:
        return False
    
def nonblkingRecv(s:socket):
    try:
        data = s.recv(HEADER).decode(FORMAT)
        response = data
    except:
        print('OS error')
    return data

def ServerConnection():
    """_summary_
    Use as Thread fucntion , a foreverloop
    """
    global online
    while(True):
        online = False
        try:
            s = connectServer()
            online = True
        except:
            pass
        if online:
            try:
                sendBytes(s,ROBOTID)
            except :
                online = False
                print('[ServerConnection]:cannot HS, Disconnected from server')
                
            try:
                updateCMD(s) #forever loop
            except:
                online = False
                print('[ServerConnection]:fail to update, Disconnected from server')
                
                command = False
        
def updateCMD(s: socket.socket):
    """_summary_
    Description: 
        FOR Blocking, 
    Args:
        s (socket.socket): _description_
    Return:
        Bool : False if fail, should reconnect
    """
    global command
    command = ''
    print("Started updateCMD loop function with socket", s)
    
    while True:
        start = time.ticks_ms()
        # print("waitng msg...")
        #able when use select
        try:
            sendLine(s,ROBOTID) # for select
        except:
            raise OSError
        #able when use select
        print("waiting respon")
        data = s.readline().decode(FORMAT).strip()
        print('[update CMD]recved:',data)
        # data = recvdata(s)
        print("-Interval : " + (str((time.ticks_ms() - start)/1000)))
        if data:
            command = data
            print('[update CMD]updated global:',data)
        else:
            command = ''
        # return data
        


def executeCMD(received_action:command):
    """_summary_
    Description: Execute Artec Robot's command according to string, text will be generated if mismatch
    Args:
        received_action (command): _string_
    """

    print("[executeCMD]Executing action:",'*',received_action)
    if received_action == "green":
        ok_logo(display)
        received_action = ""

    elif received_action == "red":
        print("Execute red")
        redCross_logo(display)
        received_action = ""
  
    elif received_action == "fw":
        L.power(50)
        R.power(50)
        L.ccw()
        R.ccw()
        
    elif received_action == "bk":
        L.power(50)
        R.power(50)
        L.cw()
        R.cw()
    elif received_action == "cw":
        L.power(50)
        R.power(50)
        L.cw()
        R.ccw()
        # dcmotor.rotate(m2="cw")
        # dcmotor.set_power(m1=30)
        # dcmotor.rotate(m1="ccw")
        # dcmotor.set_power(m2=30)
    elif received_action == "ccw":
        L.power(50)
        R.power(50)
        L.ccw()
        R.cw()
        # dcmotor.rotate(m2="ccw")
        # dcmotor.set_power(m1=30)
        # dcmotor.rotate(m1="cw")
        # dcmotor.set_power(m2=30)
    elif received_action == "stop":
        L.power(0)
        R.power(0)
        L.stop()
        R.stop()
    else:
        print("No registered command matched")

# -------------------------------CMD Action-------------------#

# ------------------------WIFI & SERVER connection-------------------#

def do_connect():
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(SSID, WIFIPW)
        # wlan.connect('Kevin(2)', '12345678')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    
def connectServer()->socket.socket:
    '''
    Description:  Connect to Server , it is deadloop is server is dead \n
    Return: Socket.socket, else raise OS error \n
    upper level is serverConnection
    
    '''
    ADDR = (SERVER, PORT) 

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    b = client.setblocking(1)
    print('[ConnectServer] NOT blking :', b)

    while (True):
        try:
            print('try connect to server')
            client.connect(ADDR)
            print("[Connect server]",client)
            return client
        except:
            print("cannot connect to server")
            raise OSError
    
    
def recvdata(socket: socket.socket):
    """
    Description:
        handle raw byte income, reuturn lib.msg object
    Args:
        socket (socket): _description_

    Returns:
        Union[msg,bool]: Return in format of {'cmd':str,'data',str}
    """
    
    # msg_length = socket.recv(HEADER).decode(FORMAT)
    # msg_length = socket.readline()
    #print("read msg_length: ",msg_length)
    recvTime = time.ticks_ms()
            
    # if msg_length:
    # message = socket.recv(int(msg_length)).decode(FORMAT)
    try:
        message = socket.readline()
        #data = json.loads(message)
        print('message',message)
        recvTime = (time.ticks_ms() -recvTime)/1000
        print("-Received in-- "+ (str(recvTime)))
        
        return message
    except:
        print('[recvdata]:msg not recved')
        return False
        #try:
            # print(fnlogg(),"read msg: ",message)

            # print(fnlogg(),data)
            # print(fnlogg(),'Receiving cmd:',data['cmd'])
            # print(logg(),'Receiving data:',data['data'])
            # print(fnlogg(),"Type",type(data))
            #data = msg(data["cmd"], data["data"])
        #    return message
        #except:
            #print("Fail to recv data")
            #return False
# else:
#     #print("Fail to recv data")
#     # print("-Received in-- "+ (str((time.ticks_ms() -recvTime)/1000)))
#     return False
    

# ------------------------WIFI & SERVER connection-------------------#
    


#-------------------------IMG logo--------------------------------#
def ok_logo(display:StuduinoBitDisplay):
    _thread.start_new_thread(green, [display])
    

def green(display:StuduinoBitDisplay):
    # _thread.start_new_thread(updateCMD, [connectServer()])
    img = StuduinoBitImage( '11111:11111:00000:11111:11111:')
    img.set_base_color((0,10,0))
    display.show(img)
    

def redCross_logo(display:StuduinoBitDisplay):
    _thread.start_new_thread(red, [display])
    
def red(display:StuduinoBitDisplay):
    img = StuduinoBitImage( '11111:11111:00000:11111:11111:')
    img.set_base_color((4,4,4))
    display.show(img)
    
#-------------------------IMG logo--------------------------------#
#------------------------THREAD-------------------------#

    
# -----------------------main------------------------
class Connection():
    def __init__(self):
       
        print('[Connection Class]Empty Connection is Created')
        
    def getSocket(self):
        try:
            return self.socket
        except:
            print('Connection is not yet established!')
    def setSocket(self,s:socket):
        self.socket = s.socket
        
            

if __name__ == '__main__':
    #connect to WIFI 
    do_connect()
    
    #start a thread 
    _thread.start_new_thread(ServerConnection, [])
    
    # s = connectServer()
    
    # ServerConnection()
    global online
    while True:
        
        try:
            # print('why not running?')#dead at first run , name error online
            # print("online?",online)
            # print("command:",command)
            if command :
                exeTime = time.ticks_ms()
                executeCMD(command)
                print(command,"-Executeded in-- " +(str((time.ticks_ms() -exeTime)/1000)))
                #clear command once executed
                command=''
        except:
            command=''
            # pass
            print('[Main Thread]: waiting connecetion established')
        # print("-Reapeated in-- " +(str((time.ticks_ms()-RepeatTime)/1000)))
            pass



    
