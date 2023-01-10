import socket
import json


class msg:
    def __init__(self,cmd,data):
        self.cmd = cmd
        self.data = data
        
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
# SERVER = "192.168.1.17"
# SERVER = "10.22.1.126"
# SERVER = "172.20.10.12
SERVER = "192.168.31.36" #Xiaomi"
# SERVER = "localhost"
ADDR = (SERVER, PORT)

socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
    
def jsonSend(text): # send JSON with  cmd:host data:unify action
    #print("sent request")
    print()
    print('Execting function: jsonSend.........')
    print('Dumping into JSON text.........')
    mymsg = json.dumps(msg("Host",text).__dict__) #_dict_ send in plaint json text
    print('Sending JSON text.........')
    send(mymsg)
    

    
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print("sent")
    print('Waiting Server Respond.........')
    a = client.recv(2048).decode(FORMAT)
    print("Received msg: ",a)
    a = decode(a)
    print("After Decode: ",a)

    
def decode(msg):
    print('Function: decode')
    if msg[0]=='{':
        print("This is JSON")
        data = json.loads(msg)
        print(json.detect_encoding(msg))
        return data
    else:
        print("This is NOT JSON")
        return msg

send("From CLI")
while(True):
    command = input("Waiting New input: ")
    jsonSend(command)


send(DISCONNECT_MESSAGE)