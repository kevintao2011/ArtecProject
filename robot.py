# Write your code here :-)
import socket
import network
import time
import socket
import _thread
import json
from pystubit.board import *
from util import * #led
import stubitapp.dcmotor as dcmotor



def request_thread():
    received_action = ""
    while True:
        #send("Request")
        #print("sent request")
        #print('Running RequestCMD')
        mymsg = json.dumps(msg("Request","Idle").__dict__)
        received_action = newSend(mymsg,received_action)

class msg:
    def __init__(self,cmd,data):
        self.cmd = cmd
        self.data = data
def newSend(msg,received_action):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print("received_action",received_action)
    tmp = client.recv(2048).decode(FORMAT)
    if(received_action == tmp):
        pass
    else:
        received_action = tmp
        print("received from host and updated action: ",received_action)

    if(received_action!="Keep Standby"):
        print("New CMD")
        #time.sleep(1)
        if(received_action == "green"):
            ok_logo()
            received_action="Keep Standby"
        elif(received_action == "red"):
            redCross_logo()
            received_action="Keep Standby"
        elif(received_action == "fw"):
            dcmotor.rotate(m1='cw')
            dcmotor.set_power(m1=100)
            dcmotor.rotate(m2='cw')
            dcmotor.set_power(m2=100)
        elif(received_action == "bk"):
            dcmotor.rotate(m1='ccw')
            dcmotor.set_power(m1=100)
            dcmotor.rotate(m2='ccw')
            dcmotor.set_power(m2=100)
        elif(received_action == "stop"):
            dcmotor.stop('brake', 'brake')
    return received_action

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def ok_logo():
    setImage([
    (0, 0, 0x001f00),
    (1, 0, 0x001f00),
    (2, 0, 0x001f00),
    (3, 0, 0x001f00),
    (4, 0, 0x001f00),
    (0, 1, 0x001f00),
    (4, 1, 0x001f00),
    (0, 2, 0x001f00),
    (4, 2, 0x001f00),
    (0, 3, 0x001f00),
    (4, 3, 0x001f00),
    (0, 4, 0x001f00),
    (1, 4, 0x001f00),
    (2, 4, 0x001f00),
    (3, 4, 0x001f00),
    (4, 4, 0x001f00)])


def redCross_logo():
    setImage([
    (0, 0, 0x1f0000),
    (4, 0, 0x1f0000),
    (1, 1, 0x1f0000),
    (3, 1, 0x1f0000),
    (2, 2, 0x1f0000),
    (1, 3, 0x1f0000),
    (3, 3, 0x1f0000),
    (0, 4, 0x1f0000),
    (4, 4, 0x1f0000)])
def greenCross_logo():
    setImage([
    (0, 0, 0x00001f),
    (4, 0, 0x00001f),
    (1, 1, 0x00001f),
    (3, 1, 0x00001f),
    (2, 2, 0x00001f),
    (1, 3, 0x00001f),
    (3, 3, 0x00001f),
    (0, 4, 0x00001f),
    (4, 4, 0x00001f)])

#WIFI Connection
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect('NETGEAR76' , 'quiettulip014')
sta.ifconfig()
print("WIFI Connection state:" ,sta.isconnected())
while(not sta.isconnected()):
    print("Failed Connect to WIFI, retrying")


HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.17"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

#WIFI Connection

send("Connect from Stduino bit")

#init
dcmotor.set_calib(100, 100)
#init

_thread.start_new_thread(request_thread,())
#_thread.start_new_thread(receive_thread,())




#send(DISCONNECT_MESSAGE)
