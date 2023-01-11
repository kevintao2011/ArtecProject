# Write your code here :-)
# Write your code here :-)
# Write your code here :-)
import socket
import network
import time
import _thread
import json
from pystubit.board import *
from util import *  # led
import stubitapp.dcmotor as dcmotor


class msg:
    def __init__(self, cmd, data):
        self.cmd = cmd
        self.data = data


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
    print("read msg_length: ",msg_length)

    if msg_length:
        message = socket.recv(int(msg_length)).decode(FORMAT)
        #data = json.loads(message)
        print('message',message)
        try:
            # print(fnlogg(),"read msg: ",message)

            # print(fnlogg(),data)
            # print(fnlogg(),'Receiving cmd:',data['cmd'])
            # print(logg(),'Receiving data:',data['data'])
            # print(fnlogg(),"Type",type(data))
            #data = msg(data["cmd"], data["data"])
            return message
        except:
            print("Fail to recv data")
            return False
    else:
        return False


def updateCMD(s: socket):
    print("Started thread")
    global cmd
    while True:
        print("waitng msg...")
        data = recvdata(s)
        try:
            print(data)
            cmd = data
            print("Received Command: ", cmd)
        except:
            print("Failed in update cmd")
            pass


def executeCMD(received_action):
    if received_action == "green":
        ok_logo()
        received_action = "Keep Standby"
    elif received_action == "red":
        redCross_logo()
        received_action = "Keep Standby"
    elif received_action == "fw":
        dcmotor.rotate(m2="ccw")
        dcmotor.set_power(m1=50)
        dcmotor.rotate(m1="ccw")
        dcmotor.set_power(m2=50)
    elif received_action == "bk":
        dcmotor.rotate(m2="cw")
        dcmotor.set_power(m1=50)
        dcmotor.rotate(m1="cw")
        dcmotor.set_power(m2=50)
    elif received_action == "cw":
        dcmotor.rotate(m2="cw")
        dcmotor.set_power(m1=30)
        dcmotor.rotate(m1="ccw")
        dcmotor.set_power(m2=30)
    elif received_action == "ccw":
        dcmotor.rotate(m2="ccw")
        dcmotor.set_power(m1=30)
        dcmotor.rotate(m1="cw")
        dcmotor.set_power(m2=30)
    elif received_action == "stop":
        dcmotor.stop("brake", "brake")
    else:
        print("No registered command matched")


def jsonSend(socket, text):  # send JSON with  cmd:host data:unify action
    # print("sent request")
    print()
    print("Execting function: jsonSend.........")
    print("Dumping into JSON text.........")
    mymsg = json.dumps(msg("Host", text).__dict__)  # _dict_ send in plaint json text
    print("Sending JSON text.........")
    send(socket, mymsg)




def newSend(msg, received_action):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    rtime = getTimer()
    client.send(message)
    print("received_action", received_action)
    tmp = client.recv(2048).decode(FORMAT)
    rtime = getTimer() - rtime
    if received_action == tmp:  # if cmd doest change
        pass
    else:
        received_action = tmp  # if cmd change, replace the new command
        print(
            "received from host and updated action: ",
            received_action,
            " response time",
            rtime,
        )
    if received_action != "Keep Standby":
        print("New CMD")
        # time.sleep(1)
        if received_action == "green":
            ok_logo()
            received_action = "Keep Standby"
        elif received_action == "red":
            redCross_logo()
            received_action = "Keep Standby"
        elif received_action == "fw":
            dcmotor.rotate(m2="ccw")
            dcmotor.set_power(m1=50)
            dcmotor.rotate(m1="ccw")
            dcmotor.set_power(m2=50)
        elif received_action == "bk":
            dcmotor.rotate(m2="cw")
            dcmotor.set_power(m1=50)
            dcmotor.rotate(m1="cw")
            dcmotor.set_power(m2=50)
        elif received_action == "cw":
            dcmotor.rotate(m2="cw")
            dcmotor.set_power(m1=30)
            dcmotor.rotate(m1="ccw")
            dcmotor.set_power(m2=30)
        elif received_action == "ccw":
            dcmotor.rotate(m2="ccw")
            dcmotor.set_power(m1=30)
            dcmotor.rotate(m1="cw")
            dcmotor.set_power(m2=30)
        elif received_action == "stop":
            dcmotor.stop("brake", "brake")
    return received_action


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))

    client.send(send_length)
    client.send(message)


def ok_logo():
    setImage(
        [
            (0, 0, 0x001F00),
            (1, 0, 0x001F00),
            (2, 0, 0x001F00),
            (3, 0, 0x001F00),
            (4, 0, 0x001F00),
            (0, 1, 0x001F00),
            (4, 1, 0x001F00),
            (0, 2, 0x001F00),
            (4, 2, 0x001F00),
            (0, 3, 0x001F00),
            (4, 3, 0x001F00),
            (0, 4, 0x001F00),
            (1, 4, 0x001F00),
            (2, 4, 0x001F00),
            (3, 4, 0x001F00),
            (4, 4, 0x001F00),
        ]
    )


def redCross_logo():
    setImage(
        [
            (0, 0, 0x1F0000),
            (4, 0, 0x1F0000),
            (1, 1, 0x1F0000),
            (3, 1, 0x1F0000),
            (2, 2, 0x1F0000),
            (1, 3, 0x1F0000),
            (3, 3, 0x1F0000),
            (0, 4, 0x1F0000),
            (4, 4, 0x1F0000),
        ]
    )


def greenCross_logo():
    setImage(
        [
            (0, 0, 0x00001F),
            (4, 0, 0x00001F),
            (1, 1, 0x00001F),
            (3, 1, 0x00001F),
            (2, 2, 0x00001F),
            (1, 3, 0x00001F),
            (3, 3, 0x00001F),
            (0, 4, 0x00001F),
            (4, 4, 0x00001F),
        ]
    )


# WIFI Connection
sta = network.WLAN(network.STA_IF)
sta.active(True)
# sta.connect('Test' , '12345678')
# sta.connect('Kevin (2)' , '12345678')
# sta.connect('WINSTARS' , 'Winstars28092299!#')
sta.connect("NETGEAR76", "quiettulip014")
sta.ifconfig()
print("WIFI Connection state:", sta.isconnected())
while not sta.isconnected():
    print("Failed Connect to WIFI, retrying")
HEADER = 64
PORT = 6000
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
# SERVER = "192.168.1.17"
# SERVER = "10.22.1.126"
# SERVER = "192.168.31.36"
# Server = "127.0.0.1"
SERVER = "192.168.1.83"  # home wifi

ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect(ADDR)
except:
    client.close()
# WIFI Connection

send("0")  # handshake

# init
dcmotor.set_calib(100, 100)
# init

_thread.start_new_thread(updateCMD, (client,))

print("Connected and start Execution")
while True:
    try:
        c = cmd
        executeCMD(c)
    except:
        pass
# send(DISCONNECT_MESSAGE)
