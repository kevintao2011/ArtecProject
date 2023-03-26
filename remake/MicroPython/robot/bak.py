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
import pickle

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
    while True: # server main loop
        start = time.time()
        # print(len(serverSockets))
        rsockets = [] #rosckets includes server sockets and robot socket in robots dictionary
        #d
        rsockets.extend(serverSockets)
        # print(robots.values(),len(robots.values()))
        if robots:
            rsockets.extend([s for s in robots]) #why this stacks?
        try:
            rsockets.append(camSocket)
        except:
            pass #no CAM
        try:
            rsockets.append(cliSocket)
        except:
            pass # no cli
        try:
            rsockets.append(guiSocket)
        except:
            pass # no gui
        
        # print("rsocks:",rsockets)
        read_sockets, write_sockets, error_sockets = select.select(rsockets, [s for s in robots], [],0)
       
            
        sock:socket.socket
        readTime = time.time()
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
                    print("GUI Connected")
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
                            # write_sockets.append(lib.Robot.robo
                            #                      tIDdict[id])
                        for id in robotActionsDict:
                            robots[lib.Robot.robotIDdict[id]].action=robotActionsDict.get(id)
                        print('clicmd:',robotActionsDict)
                        
                            
                        
                if (online["CAM"]):
                    found = True
                    if sock == camSocket:
                        recvCAMTime=time.time()
                        camdata = lib.recvCAM(sock) #return plain jsontext
                        if (time.time()-recvCAMTime>0.01):
                            print('read in ',time.time()-recvCAMTime) 
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
                                    print('No such robot' , i)
               
                # print('From robots',robots[sock])

                if(sock in robots): #all robots
                    # print("Get Request from robot",robots[sock].arindex)
                    recvTime=time.time()
                    # sock.recv(1024) #disable coz robot no longer send thngs
                    # if(robots[sock].continuousActionFlag): #not actually receive new command , just doing reapeated actiob (now moved ouside coz not trigger by response) 
                    #     a =lib.analyze(robots[sock].contAction,robots[sock].arindex,robots)
                    #     print('[read_s:] reanalyze from cont action:',a)
                    # # print('wait robo response in ',time.time()-recvTime)
                    # if not sock in write_sockets:
                    #     write_sockets.append(sock)
                        
                
               
                # for r in robots:
                #     print(sock,robots[r]["socket"])
                #     if sock == robots[r]["socket"]:
                #         lib.
                #         write_sockets.append(robots[r]["socket"])
                #         print(robots[r]["socket"], "is add to write")
        if (time.time()-readTime>0.01):
            print('read in ',time.time()-readTime)            
        # try:         
        #     if lib.Robot.robotSockDict.keys:
        #         write_sockets.append(guiSocket)
        # except:
        #     pass
        
        #update continuous actio
        for r in robots:
            if(robots[r].continuousActionFlag): #not actually receive new command , just doing reapeated actiob
                a =lib.analyze(robots[r].contAction,robots[r].arindex,robots) #update action attribute
                print('[read_s:] reanalyze from cont action:',a)
            # print('wait robo response in ',time.time()-recvTime)
                # write_sockets.append(r)
        
        
        writeTime=time.time()
        for sock in write_sockets: #how to access robot socket asap
            if sock in lib.Robot.robotSockDict.keys():
                if robots[sock] and robots[sock].action!='': #hv sth to send
                    try:
                        print(command)
                        lib.sendline(sock,robots[sock].action)
                        print("sent to ",robots[sock].arindex)
                        robots[sock].action = '' # cleared action should be recovered in write
                    except:
                        print('fail to send')
            else:#GUI
                # r = [robots[sock] for sock in lib.Robot.robotSockDict.keys()]
                # r =pickle.dumps(r)
                # sock.send(r)
                pass
        if write_sockets:        
            # print('writesockets',write_sockets) 
            if (time.time()-writeTime>0):
                print('write in ',time.time()-writeTime)
            # try:
            #     command
            #     lib.sendline(sock,command)
            #     print("sent to ",robots[sock].arindex)
            # except:
            #     pass #no command to send yet
        # write_sockets.append
        # for 
        # print('Select cycle is:',time.time()-start)
        if time.time()-start > 0.1:
            print('server cycle time:',time.time()-start)
            
            
            
            
            
            











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
import pickle

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
    while True: # server main loop
        start = time.time()
        # print(len(serverSockets))
        rsockets = [] #rosckets includes server sockets and robot socket in robots dictionary
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
        readTime = time.time()
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
                    print("GUI Connected")
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
                        recvCAMTime=time.time()
                        camdata = lib.recvCAM(sock) #return plain jsontext
                        if (time.time()-recvCAMTime>0.01):
                            print('read in ',time.time()-recvCAMTime) 
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

                    if(robots[sock]): #all robots
                        # print("Get Request from robot",robots[sock].arindex)
                        recvTime=time.time()
                        sock.recv(1024) #disable coz robot no longer send thngs
                        if(robots[sock].continuousActionFlag): #not actually receive new command , just doing reapeated actiob
                            a =lib.analyze(robots[sock].contAction,robots[sock].arindex,robots)
                            print('[read_s:] reanalyze from cont action:',a)
                        # print('wait robo response in ',time.time()-recvTime)
                        if not sock in write_sockets:
                            write_sockets.append(sock)
                        
                except:
                    print('robot socket has no response msg')
               
                # for r in robots:
                #     print(sock,robots[r]["socket"])
                #     if sock == robots[r]["socket"]:
                #         lib.
                #         write_sockets.append(robots[r]["socket"])
                #         print(robots[r]["socket"], "is add to write")
        if (time.time()-readTime>0.01):
            print('read in ',time.time()-readTime)            
        # try:         
        #     if lib.Robot.robotSockDict.keys:
        #         write_sockets.append(guiSocket)
        # except:
        #     pass
        writeTime=time.time()
        for sock in write_sockets: #how to access robot socket asap
            if sock in lib.Robot.robotSockDict.keys():
                if robots[sock] and robots[sock].action!='':
                    try:
                        print(command)
                        lib.sendline(sock,robots[sock].action)
                        print("sent to ",robots[sock].arindex)
                        robots[sock].action = ''
                    except:
                        pass
            else:#GUI
                # r = [robots[sock] for sock in lib.Robot.robotSockDict.keys()]
                # r =pickle.dumps(r)
                # sock.send(r)
                pass
        if len(write_sockets)>0:        
            print(write_sockets) 
            print('write in ',time.time()-writeTime)
            # try:
            #     command
            #     lib.sendline(sock,command)
            #     print("sent to ",robots[sock].arindex)
            # except:
            #     pass #no command to send yet
        # write_sockets.append
        # for 
        # print('Select cycle is:',time.time()-start)
        if time.time()-start > 0.1:
            print('server cycle time:',time.time()-start)