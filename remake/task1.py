import socket
import sys
sys.path.append('./')
import lib
import time
print("This is terminal for CLI.....")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Try connection to",lib.CLI_ADDR)
s.connect(lib.CLI_ADDR)
connectionState=True
6
# msg = lib.msg("20",'a').toJSON()

# print(msg)
# lib.send(s,msg)

# lib.send(s,msg)
numberOfDevices : int
numberOfDevices = input('please enter number of device')
color = ['red','orange','yellow','green','lb','blue','purple']
taskList = ['red','green','1,3,5,7,green','2,4,6,8,red',]
counter = 0
while(True):
    #normal
    # command = input("Waiting New input: ")
    
        
    # print(command)
    # msg = lib.msg(command,'None').toJSON()

    
    #random test
    # if (counter%2):
    #     msg = 'red'
    # else:
    #     msg = 'green'
    
    # lib.send(s,msg) #random
    # for i in range(int(numberOfDevices)):
    #     command = str(i+1)+','+color[counter%7]
    #     print('send: ',command)
    #     connectionState = lib.send(s,command)
    #     counter+=1
    #     if(not connectionState):
    #         break
    
    
    for i in range(int(numberOfDevices)):
        command = color[counter%7]
        print('send: ',command)
        connectionState = lib.send(s,command)
        counter+=1
        if(not connectionState):
            break
        time.sleep(1)
    if connectionState:
        print('sent')
        
    else:
        try:
            print(lib.logg(),"Connection failed, try reconnect..")
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(lib.CLI_ADDR)
            connectionState = True
            numberOfDevices = input('please enter number of device')
        except:
            pass
    
    # time.sleep(1)

    