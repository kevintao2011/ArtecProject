import socket
import sys
sys.path.append('./')
import lib

print("This is terminal for CLI.....")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Try connection to",lib.CLI_ADDR)
s.connect(lib.CLI_ADDR)
connectionState=True
lib.send(s,'8')
# msg = lib.msg("20",'a').toJSON()

# print(msg)
# lib.send(s,msg)

# lib.send(s,msg)

while(True):
    command = input("Waiting New input: ")
    msg = lib.msg('CLI',command).toJSON()
    try:
        lib.send(s,msg)
    except:
        print(lib.logg(),"Connection failed, try reconnect..")
        connectionState = False
        while(not connectionState):
            try:
                s.close()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(lib.CLI_ADDR)
                lib.send(s,'8')
                connectionState = True
            except:
                print("Failed to reconnect")
                pass
        

    