import socket
import sys
import threading
import time

sys.path.append('./')
import lib
from threading import Thread
import json
import tkinter as tk
import multiprocessing as mp
import atexit
import select


online = {
    "CAM" : False,
    "CLI" : False,
    "GUI" : False,
}
if __name__ == '__main__':
    
    
    serverSockets=[]
    robot_server =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to a specific address and port
    robot_server.bind((lib.SERVER, lib.ARTEC_PORT))
    # listen for incoming connections
    robot_server.listen()
    # list of sockets to monitor
    print('Robot Server started at ',lib.ARTEC_PORT,', waiting for connections...')
    serverSockets.append(robot_server)
    
    CLI_server =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to a specific address and port
    CLI_server.bind((lib.SERVER, lib.CLI_PORT))
    # listen for incoming connections
    CLI_server.listen()
    # list of sockets to monitor
    print('CLI Server started at ',lib.CLI_PORT,', waiting for connections...')
    serverSockets.append(CLI_server)
    
    CAM_server =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to a specific address and port
    CAM_server.bind((lib.SERVER, lib.CAM_PORT))
    # listen for incoming connections
    CAM_server.listen()
    # list of sockets to monitor
    print('CAM Server started at ',lib.CAM_PORT,', waiting for connections...')
    serverSockets.append(CAM_server)
    
    GUI_server =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to a specific address and port
    GUI_server.bind((lib.SERVER, lib.GUI_PORT))
    # listen for incoming connections
    GUI_server.listen()
    # list of sockets to monitor
    print('GUI Server started at ',lib.GUI_PORT,', waiting for connections...')
    serverSockets.append(GUI_server)
    
    robots={}
    cliSocket: socket.socket
    camSocket: socket.socket
    guiSocket: socket.socket
    
    cliConnected:bool
    command:str = ""
    while True:
        start = time.time()
        # print(len(serverSockets))
        rsockets = []
        #d
        rsockets.extend(serverSockets)
        # print(robots.values(),len(robots.values()))
        if robots:
            rsockets.extend([s for s in robots]) #why this stacks?
        try:
            rsockets.append(camSocket)
        except:
            pass
        try:
            rsockets.append(cliSocket)
        except:
            pass
        try:
            rsockets.append(guiSocket)
        except:
            pass
        
        # print("rsocks:",rsockets)
        read_sockets, write_sockets, error_sockets = select.select(rsockets, [], [],0)
       
            
        sock:socket.socket
        for sock in read_sockets:
            # print(sock.getsockname() ,'is readable')
            if sock in serverSockets:
                print('From server')
                clientSocket, clientAddress = sock.accept()
                print(f'New connection from {clientAddress}')
                # get buffer
                # print('buffersize:',client_server.getsockopt(socket.SOL_server,socket.SO_RCVBUF))
                print('****************soocket info****************')
                print('timeout:',sock.gettimeout())
                print('Blocking status:',sock.getblocking())
                
                print('****************soocket info****************')
                #if reconnect at diff ports

                if sock == robot_server:
                    try:
                        id = lib.recv(clientSocket)
                    except:
                        print('Cannot identify Robot ID, will not add this connection')
                    
                    
                    for robotid in robots.keys():
                        if robotid == id:
                            del robots[id]
                            print('it is a reconnect connection , old is deleted')
                            break
                    robots[clientSocket]=lib.Robot(id,lib.connection((clientSocket,clientAddress)))
                    # read_sockets.extend([s["Robot"].conn.s for s in robots.values()])
                    
                    
                    
                elif sock == CLI_server:
                    
                    
                    print('cli connection')
                        
                    cliSocket = clientSocket
                    online["CLI"] = True                
                elif sock == CAM_server:
                    
                    try:
                        isinstance(camSocket,socket.socket)
                        clientSocket.close()
                        print('it is a reconnect connection , old is deleted')
                    except:
                        print('First CAM connection')
                        
                    camSocket = clientSocket
                    online["CAM"] = True 
                elif sock == GUI_server:
                    
                    try:
                        isinstance(guiSocket,socket.socket)
                        guiSocket.close()
                        print('it is a reconnect connection , old is deleted')
                    except:
                        print('First gui connection')
                        
                    guiSocket = clientSocket
                    online["GUI"] = True 
                else:
                    print('Annoymous server, programming mistake')
                    raise RuntimeError
            else: #from clients sockets
                # print('From clients')
                found = False
                if (online["CLI"]):
                    found = True
                    if sock == cliSocket:
                        print('From cli')
                        # command = lib.recvdata(sock)
                        try:
                            # #for JSON
                            # command = lib.recvdata(sock)
                            # command = command.getCMD()
                            command = lib.recvBytes(sock)
                            print('clicmd:')
                            
                        except:
                            print('cli disconnected ')
                            cliSocket.close()
                            del cliSocket
                            online["CLI"] = False 
                if (online["CAM"]):
                    found = True
                    if sock == camSocket:
                        camdata = lib.recvCAM(sock)
                        
                        locDict = lib.updateLocation([r['Robot'].arindex for r in robots.values()],camdata)
                        
                        for i in locDict.keys():
                            robots[i]["Robot"].location = locDict[i]["location"]
                try:
                    # print('From robots',robots[sock])
                    if(robots[sock] and command!=""):
                        print("Request from robot",robots[sock].arindex)
                        sock.recv(1024)
                        write_sockets.append(sock)
                        
                except:
                    pass
               
                # for r in robots:
                #     print(sock,robots[r]["socket"])
                #     if sock == robots[r]["socket"]:
                #         lib.
                #         write_sockets.append(robots[r]["socket"])
                #         print(robots[r]["socket"], "is add to write")
                    
                
                    
        for sock in write_sockets: #how to access robot socket asap
            
            if robots[sock]:
                try:
                    print(command)
                    lib.sendline(sock,command)
                    print("sent to ",robots[sock].arindex)
                    command = ""
                except:
                    pass
          
            # try:
            #     command
            #     lib.sendline(sock,command)
            #     print("sent to ",robots[sock].arindex)
            # except:
            #     pass #no command to send yet
        # write_sockets.append
        # for 
        # print('Select cycle is:',time.time()-start)