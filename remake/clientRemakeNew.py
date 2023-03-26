import socket
import sys
sys.path.append('./')
import lib
import random

print("This is terminal for CLI.....")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Try connection to",lib.CLI_ADDR)
s.connect(lib.CLI_ADDR)
connectionState=True
# msg = lib.msg("20",'a').toJSON()

# print(msg)
# lib.send(s,msg)

# lib.send(s,msg)
counter = 0
while(True):
    #normal
    command = input("Waiting New input: ")
    print(command)
    # msg = lib.msg(command,'None').toJSON()

    
    #random test
    # if (counter%2):
    #     msg = 'red'
    # else:
    #     msg = 'green'
    
    # lib.send(s,msg) #random
    connectionState = lib.send(s,command)
    if connectionState:
        print('sent')
    else:
        try:
            print(lib.logg(),"Connection failed, try reconnect..")
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(lib.CLI_ADDR)
        except:
            pass
    
    # except:
    #     print(lib.logg(),"Connection failed, try reconnect..")
    #     connectionState = False
    #     while(not connectionState):
    #         try:
    #             s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #             s.connect(lib.CLI_ADDR)
    #             # lib.send(s,'8')
    #             connectionState = True
    #         except:
    #             print("Failed to reconnect")
    #             pass
    # counter+=1
        

    