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
                            print('it is a robot reconnect connection , old is deleted')
                            break
                    robots[clientSocket]=lib.Robot(id,lib.connection((clientSocket,clientAddress)))
                    # read_sockets.extend([s["Robot"].conn.s for s in robots.values()])
                    
                    
                    
                elif sock == CLI_server:
                    
                    
                    print('cli connection')
                        
                    cliSocket = clientSocket
                    online["CLI"] = True                
                elif sock == CAM_server:
                        
                    camSocket = clientSocket
                    online["CAM"] = True 
                elif sock == GUI_server:
                    
                    
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
                        except:
                            print('cli disconnected ')
                            cliSocket.close()
                            del cliSocket
                            online["CLI"] = False 
                        targets,command = lib.getTargets(command,robots)
                        robotActionsDict = {}
                        print(targets)
                        for id in targets:
                            robotActionsDict[id] = lib.analyze(command,id,robots)
                            write_sockets.append(lib.Robot.robotIDdict[id])
                        for id in robotActionsDict:
                            robots[lib.Robot.robotIDdict[id]].action=robotActionsDict.get(id)
                        print('clicmd:',robotActionsDict)
                        
                            
                        
                if (online["CAM"]):
                    found = True
                    if sock == camSocket:
                        camdata = lib.recvCAM(sock) #return plain jsontext
                        
                        locDict = lib.processLocation(robots.values(),camdata) #load json and return nested dict {"id"}
                        if locDict:
                            for i in  (locDict.keys()):
                                # if robots:
                                #     robots[lib.Robot.robotIDdict[i]].setloc(locDict[i].coordination,locDict[i].orientation)
                                #     robots[lib.Robot.robotIDdict[i]].orientation = locDict[i].orientation
                                try:
                                    robots[lib.Robot.robotIDdict[i]].setloc(locDict[i].coordination,locDict[i].orientation)
                                    robots[lib.Robot.robotIDdict[i]].orientation = locDict[i].orientation
                                except:
                                    # print(f'robot not yet register! ',i)
                                    pass
                try:
                    # print('From robots',robots[sock])

                    if(robots[sock]):
                        if(robots[sock].continuousActionFlag):
                            a =lib.analyze(robots[sock].contAction,robots[sock].arindex,robots)
                            print('[read_s:] reanalyze from cont action:',a)
                        print("Request from robot",robots[sock].arindex)
                        sock.recv(1024)
                        if not sock in write_sockets:
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
            
            if robots[sock] and robots[sock].action!='':
                try:
                    print(command)
                    lib.sendline(sock,robots[sock].action)
                    print("sent to ",robots[sock].arindex)
                    robots[sock].action = ''
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