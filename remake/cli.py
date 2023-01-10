import socket
import sys
sys.path.append('./')
import lib

def run():
    print("Running cli.py")
    # set up cli server port
    CLIserver = socket.create_server(lib.CLI_ADDR, 
    family=socket.AF_INET,dualstack_ipv6=False) # TCP
    CLIserver.listen()
    # accept connection and run 
    while(1):
        print(lib.logg(),'waiting cli connect .........')
        tmp = (CLIserver.accept()) #return a tuple with socket obj and addr
        # clientsocketlist.append(tmp[0])# list socket 
        # clientaddrlist.append(tmp[1])# list addr (tuple with ip and port)
        print(lib.logg(),"Now System is controlled by: ",tmp)
        t = Thread(target=serverThread.run(tmp[0]),args=(1)) #pass socket into thread
        t.start()
        print('Created a new thread')