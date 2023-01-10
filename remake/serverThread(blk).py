import time
import sys
sys.path.append('./')
import lib
import socket
import threading
import json

class ServerThread(): #blocking vesion
    def __init__(self,s:socket.socket):
        self.s=s
        print("Thread Created")
    def __call__(self):
        print(self.s)
        self.s.setblocking(True)
        print(lib.logg(),"set to blocking mode")
        print(lib.logg(),"Running in thread!",threading.get_ident())
        
        
        id = lib.recv(self.s)
        print(lib.logg(),"Connceted id: ",id)
        
        print(lib.logg(),"Waiting msg....")
        while(True):
            msg = lib.recv(self.s)
            # print(type(msg))
            print('msg: ',msg)
            # if(msg):
            #     print('msg: ',msg)
            #     print(lib.logg(),"Waiting msg....")
            
# def run(s:socket.socket):
#     s.setblocking(True)
#     print(lib.logg(),"set to blocking mode")
#     print(lib.logg(),"Running in thread!",threading.get_ident())
    
    
#     id = lib.recv(s)
#     print(lib.logg(),"Connceted id: ",id)
    
#     print(lib.logg(),"Waiting msg....")
#     while(True):
#         msg = lib.recv(s)
#         # print(type(msg))
#         print('msg: ',msg)
#         # if(msg):
#         #     print('msg: ',msg)
#         #     print(lib.logg(),"Waiting msg....")
        
#     print(lib.logg(),"Received all msg")
     
