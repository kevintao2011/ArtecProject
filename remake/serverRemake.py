import socket
import sys
sys.path.append('./')
import lib
import serverThread
from threading import Thread
import select
    
# def __main__():

TCPserver = socket.create_server(lib.CLI_ADDR, 
family=socket.AF_INET,dualstack_ipv6=False)
TCPserver.listen()

clientsocketlist = []
clientaddrlist = []
print(lib.logg(), "Server Listening at ",lib.CLI_ADDR)


print(lib.logg(),'waiting a new connection .........')
tmp = (TCPserver.accept()) #return a tuple with socket obj and addr
clientsocketlist.append(tmp[0])# list socket 
clientaddrlist.append(tmp[1])# list addr (tuple with ip and port)
print("1: ",type(tmp[0]), tmp[0])
print("2: ",type(tmp[1][0]), tmp[1][0],type(tmp[1][1]), tmp[1][1])
print(lib.logg(),"New connection: ",clientaddrlist[len(clientaddrlist)-1])

t = Thread(target=serverThread.ServerThread(tmp[0]))
t.start()

# while(True):
#     CLI_Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     CLI_Server.bind(lib.CLI_ADDR)
#     CLI_State = False
#     print(lib.logg(), "Waiting CLI connect to ",lib.SERVER , ",",lib.CLI_PORT)
#     while(1):
#         print(lib.logg(),'waiting a CLI connection .........')
#         tmp = (CLI_Server.accept()) #return a tuple with socket obj and addr
#         CLI_State = True
#         print('CLI_Connected')
#         t = Thread(target=serverThread.run(tmp[0]),args=(1)) #pass socket into thread
#         t.start()
#         print('Created a new thread')

#     # UDPserver = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)



    
