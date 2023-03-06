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


# fold/wrap function Press Ctrl + K + S for All Settings. Assign a key which you want for Fold All. By default it's Ctrl + K + 0 .


# global robotConnectionList
# robotConnectionList = []


# global camSocketList
global camConnection

#------------------------------Exit Handler------------------------------#
def exit_killSocket(s:socket):
    print('Exit,closing the socket')
    s.close()
#------------------------------CAM Part-----------------------------------#
def acceptCam():
    CAMserver = socket.create_server(lib.CAM_ADDR,family=socket.AF_INET,dualstack_ipv6=False)
    atexit.register(exit_killSocket,s=CAMserver)
    CAMserver.listen()
    print(lib.logg(), "CAM Server Listening at ",lib.CAM_ADDR)
    while(True):
        s = CAMserver.accept()
        
        s = lib.connection(s)
        
        t = Thread(target=updateloc, args=(s,))
        t.start()

def acceptCamOnce():
    CAMserver = socket.create_server(lib.CAM_ADDR,family=socket.AF_INET,dualstack_ipv6=False)

    CAMserver.listen()
    print(lib.logg(), "CAM Server Listening at ",lib.CAM_ADDR)
    
    
    s = CAMserver.accept()
    s = lib.connection(s)
    # camhandshake = False
    
    # while not camhandshake :
    #     try:
    #         handshakeID = lib.recv(camConnection.s)
    #         camhandshake = True
    #     except:
    #         print(lib.logg(),"Cam cannot receive handshake")
    t = Thread(target=updateloc, args=(s,))
    t.start()
        
            
def updateloc(c:lib.connection):
    global camConnection
    camConnection =c
    
    camhandshake = False
    while not camhandshake :
        try:
            handshakeID = lib.recvCAM(camConnection.s)
            camhandshake = True
        except:
            print(lib.logg(),"[updateloc] ","Cam Disconnected") 
    print(lib.logg(), "[updateloc] ","Camera is Connected on port ",camConnection.port)
    
       
    
    while(True):
        listForUpdate = []
        # try: #get data part and create list for update
        #     empty = False
        #     counter = 0
        #     camdata = lib.recvdata(camConnection.s)
            
                
        # except:
        #     pass
        #     # print("No data")
        #     camdata = None
        try:
            camdata = lib.recvdata(camConnection.s)
            
        except:
            print("[updateloc] ","CAM disconnected")
        
        try:# put list of robot to be update into list and execute updates
            recvLocJson = json.loads(camdata.data['data'])
        
        except:
            print(lib.logg(),"No robot exits yet")
            pass
        print(lib.fnlogg(),"[updateloc] ","Parsed cam data")
        # print(recvLocJson)
        for i in range(len(recvLocJson)): 
            listForUpdate.append(recvLocJson[i]['index'][0])
        # print("captured robots'ID",listForUpdate)
        if len(listForUpdate)>0:
            for i in range(len(listForUpdate)): #for # of detected robot
                # print("captured robots'ID",i)
                for robot in robotlist:
                    if int(robot.arindex) == int(listForUpdate[i]):
                        robot.setloc(recvLocJson[i]['coordination'][0],recvLocJson[i]['orientation'])
                        # print(robot.orientation)
        
#------------------------------CAM Part-----------------------------------#


#--------------------------------CLI interface--------------------------------#
def acceptCLI():
    """_summary_
        Create a socket keep looking for cli in thread using function lib.updateCommand \n
        if second cli then close old socket and open new\n
        Global var: cliConnection
    """
    CLIserver = socket.create_server(lib.CLI_ADDR,family=socket.AF_INET,dualstack_ipv6=False)
    atexit.register(exit_killSocket,s=CLIserver)
    CLIserver.listen()
    
    print(lib.logg(),'[acceptCLI]', "CLI Server Listening at ",lib.CLI_ADDR)
    while(True): 
        
        s = CLIserver.accept()
        try:
            conn.s.close()
            del conn
            print('[acceptCLI]','Updated CLI socket')
        except:
            print('[acceptCLI]','Fisrt CLI connection')
            
        conn = lib.connection(s)
        try:
            lib.recv(conn.s) #delete this when no handshake
            print('[acceptCLI]','recv handshake')
        except:
            print('[acceptCLI]','no handshake, disconnected')
            break
        global cliConnection
        cliConnection = conn 
        cliConnection.s.setblocking(True)        
        t = Thread(target=updateCommand, args=(cliConnection,))
        t.start()
        
def acceptCLIOnce():
    #Objective: Create a socket keep looking for cli
    CLIserver = socket.create_server(lib.CLI_ADDR,family=socket.AF_INET,dualstack_ipv6=False)
    CLIserver.listen()
    
    print(lib.logg(), "CLI Server Listening at ",lib.CLI_ADDR)
    (s,ipv4) = CLIserver.accept()
    print(s,ipv4)
    s = lib.connection(s)
    lib.recv(s.s) #delet this when no handshake
    global cliConnection
    cliConnection = s  
    global cliState
    cliState = True
    t = Thread(target=updateCommand, args=(cliConnection,))
    t.start()
        
def updateCommand(c:lib.connection):
    """_summary_\n
    
    Description:recv msg and update global cmd\n
    Global var: general_cmd\n
    Args:\n
        c (lib.connection): _description_\n
    """
    global cliState
    cliState = True
    while(True):
        try:
            #receive cli cmd
            # tmp =lib.recvdata(cliConnection.s)
            # access the global CLI_cmd variable
            print("waiting msg...")
            tmp =lib.recvdata(c.s)
            # try:
            #     tmp =lib.recvdata(c.s)
            # except:
            #     print('CLI disconnected')
            #     break
            
            
            # try:
            #     print("tmp =", tmp.cmd)
            #     print("tmp =", tmp.getCMD())
            # except:
            #     pass
            global general_cmd
            general_cmd = tmp
            print(lib.logg(), "New Command: ", general_cmd.getCMD(),general_cmd.getData())
            
        except:
            print(lib.logg(), "sth goes wrong,close connection")
            c.s.close()
            cliState = False
            break
        try:
            if(tmp):
                analyzeCMD(general_cmd)
        except:
            print('fail to analyze')
        
def analyzeSpecificCMD(command:str,robot:lib.Robot):
    
    # for robot in robotlist:
    #     if robot 
    start = time.time()
    print(lib.logg(),"calling analyzeSpecificCMD")
    print(lib.logg(),"command",command) #command 'dir:90'
    commandA = command.split(':') #commandA ['dir', '90']
    print(lib.logg(),"commandA",command)
    param = commandA[1].split('-')
    if (commandA[0]=='dir'):
        direction = int(param[0])
        robot.startContAction(command)
        ori = int(robot.orientation)
        print('Orientation: ',ori)
        if(ori<direction):
            robot.action = 'cw' 
        elif(ori>direction):
            robot.action = 'ccw'
        if abs(direction - ori) < 15 or abs(ori - direction)<15:
            robot.action = 'stop'
            print(direction,' Degree!')
            robot.endContAction()    
    elif (commandA[0]=='move to'):
        robot.startContAction(command)
        x,y = param[0],param[1] #x,y is coor of destination
        x = int(x)
        y = int(y)
        s = str(robot.location[0])+' '+str(robot.location[1])
        direction = lib.vectorAngle(robot.location,(x,y))  #y need to revert becoz of coordination is not same as classic 
        robot.remark=s+' '+str(direction)
        ori = int(robot.orientation)

        if abs(direction - ori) < 10 or abs(ori - direction)<10:
            if(abs(robot.location[0] - x) < 100 or abs(x-robot.location[0]) < 100) and ((abs(robot.location[1] - y) < 100 or abs(y-robot.location[1]) < 100)):
                robot.action = 'stop'
                robot.endContAction()
            else:
                robot.action = 'fw'
            # robot.action = 'stop'
            # print(direction,' Degree!')
            # robot.endContAction()
        elif(ori<direction):
            robot.action = 'cw' 
        elif(ori>direction):
            robot.action = 'ccw'
    end = time.time()- start
    print('[analyzeSpecificCMD] analyzeTime;',end)
            
def analyzeCMD(message:lib.msg):
    
    start = time.time()
    targets = []
    command = ''
    print(lib.fnlogg(),"calling analyze cmd")
    #CMD type: onee-time, continue, mass,specific
    try: #if mass
        cmdstr = message.getCMD()
        cmdstr = cmdstr.split(",")
    except: #otherwise
        pass
    # classify it is mass/specific command or to server
    if(len(cmdstr)==1):
        
        if(cmdstr[0]=="display"):
            print(lib.fnlogg(),"teminal cmd!")
            for robot in robotlist:
                robot.displayInfo()
            
        else:
            print(lib.fnlogg(),"Mass Command")
            for robot in robotlist:
                targets.append(robot.arindex)
            command=cmdstr[0] #cmdstr = cmdstr.split(",")
            print(lib.fnlogg(),"targets ",targets)

            # for robot in robotlist:
            #     robot.action = cmdstr
            #     print(lib.fnlogg(),"updated action of all")
    else:
        print(lib.fnlogg(),"specific cmd")
        command = cmdstr[len(cmdstr)-1]
        print(lib.fnlogg(),"command: ",command)
        for ID in cmdstr:
            targets.append(ID)
    
    #update command to target
    for target in targets:
        for robot in robotlist:
            if(robot.arindex==target):
                #determine if command need further analyze using analyzeSpecificCMD()
                #find-grained control
                # later change to command in command list
                print(lib.fnlogg(),"Determine if cmd need further analyze")
                specific = False
                for k in lib.cmdlist.keys() :
                    if (k in command):
                        print(lib.fnlogg(),"specific")
                        specific = True
                        analyzeSpecificCMD(command,robot)

                #for consistent action like lighting or cw              
                print(lib.fnlogg(),"specific",specific)
                if not specific:
                    robot.action = command
                    print(lib.logg(),"updated action of",robot.arindex)
    print('[analyzeCMD]analyzed in %d second' %(time.time()-start))
    # command = cmdstr[len(cmdstr)-1]
        
    # print(lib.fnlogg(),"popped")
    # for target in cmdstr:
    #     print(lib.fnlogg(),"target: ",target)
    #     for robot in robotlist:
    #         if(robot.arindex==target):
    #             robot.action = command
    #             print(lib.logg(),"updated action of",robot.arindex)
    
            
#--------------------------------CLI interface-------------------------#

#--------------------------------Robt Interface------------------------#
            
    
def acceptRobot():
    """
    1)Create server and port\n
    2)recv str Robot ID with lib.recv function\n
    3)update Robot's socket to robot list \n
    """
    ROBOTserver = socket.create_server(lib.ROBOT_ADDR,family=socket.AF_INET,dualstack_ipv6=False)
    atexit.register(exit_killSocket,s=ROBOTserver)
    ROBOTserver.listen()
    print(lib.logg(), "ROBOT Server Listening at ",lib.ROBOT_ADDR)
    while(True):
        duplicated = False
        # ROBOTserver.setblocking(False)
        
        s = ROBOTserver.accept()
        try:
            print('[acceptrobot]: detected new connection, waiting handshake.....')
            ID = lib.recv(s[0]) # handshake
        except:
            print('[acceptrobot]: cannot receive a handshake')
        print("[acceptrobot]RobotList",len(robotlist))
        for robot in robotlist:
            # s[0] = socket and [1] = ip+port
            if s[1][0] == robot.conn.ip:
                print(lib.logg(),'[acceptrobot]','this ip is duplicated!')
                robot.updateConnection(s)
                print(lib.logg(),'[acceptrobot]','Updated port to ',robot.conn.port)
                robot.handshake = True
                duplicated = True 
        if not duplicated:
            s = lib.connection(s)
            robot=lib.Robot(id=ID,conn=s)
            robot.handshake=True 
            robotlist.append(robot)# list socket 
            robot.displayInfo()
            print(lib.logg(),'[acceptrobot]','New Artec is Registered')
#--------------------------------Robt Interface------------------------#
        
def GUI():
    def set_label():
        currentTime = lib.datetime.now()
        label['text'] = currentTime
        try:
            label_CAMiP['text'] = camConnection.port
            label_CLIIP['text'] = cliConnection.port
        except:
            pass
       
        
        for robot in robotlist:
            oriList[int(robot.arindex)]['text']=str(robot.orientation)
            actionList[int(robot.arindex)]['text']=str(robot.action)
            hsList[int(robot.arindex)]['text']=str(robot.handshake)
            caList[int(robot.arindex)]['text']=str(robot.continuousActionFlag)
            locstr = str(robot.location[0])+" , "+str(robot.location[1])
            locList[int(robot.arindex)]['text']=locstr
            remarkList[int(robot.arindex)]['text']=robot.remark
            portList[int(robot.arindex)]['text']=str(robot.conn.port)
        window.after(1, set_label)
            
    
    def dataupdate():

        # lock.acquire()
        print('dataupdate GUI data')
        for robot in robotlist:
            # print(robot.arindex,' GUI update robot ori ',robot.orientation)
            oriList[robot.arindex]['text']=str(robot.orientation)
            window.after(100, dataupdate)
        # lock.release()
    
    window = tk.Tk()

    # root window
    window.title('GUI')
    # window.geometry("240x100")
    window.resizable(1, 1)

    # configure the grid
    # window.columnconfigure(which col, weight=size)
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=3)
    window.columnconfigure(2, weight=3)
    window.columnconfigure(3, weight=3)
    window.columnconfigure(4, weight=3)
    window.columnconfigure(5, weight=3)
    window.columnconfigure(6, weight=3)
    window.columnconfigure(7, weight=3)

    label = tk.Label(window, text="placeholder")
    label.grid(column=1,row=0)
    label_CAM = tk.Label(window, text="CAM Port")
    label_CAM.grid(column=2,row=0)
    label_CAMiP = tk.Label(window, text="not connected")
    label_CAMiP.grid(column=3,row=0)
    label_CLI = tk.Label(window, text="CLI Port")
    label_CLI.grid(column=4,row=0)
    label_CLIIP = tk.Label(window, text="not connected")
    label_CLIIP.grid(column=5,row=0)
    
    label_id = tk.Label(window, text="ID")
    label_id.grid(column=0,row=1)
    label_Ori = tk.Label(window, text="ori")
    label_Ori.grid(column=1,row=1)
    label_Action = tk.Label(window, text="Action")
    label_Action.grid(column=2,row=1)
    label_hs = tk.Label(window, text="handshake")
    label_hs.grid(column=3,row=1)
    label_ca = tk.Label(window, text="ContinuousAction")
    label_ca.grid(column=4,row=1)
    label_loc = tk.Label(window, text="Location")
    label_loc.grid(column=5,row=1)
    label_remark = tk.Label(window, text="Remark")
    label_remark.grid(column=6,row=1)
    label_port = tk.Label(window, text="Port")
    label_port.grid(column=7,row=1)
    label_port = tk.Label(window, text="Latency")
    label_port.grid(column=8,row=1)
    
    
    
    oriList =[]
    idList = []
    actionList =[]
    hsList = []
    caList = []
    locList = []
    remarkList = []
    portList = []
    latencyList = []
    for i in range (10):
        ID = tk.Label(window, text=str(i))
        Ori = tk.Label(window, text="not connected")
        act = tk.Label(window, text="not connected")
        hs = tk.Label(window, text="not connected")
        ca = tk.Label(window, text="not connected")
        loc = tk.Label(window, text="not connected")
        remark = tk.Label(window, text="not connected")
        port = tk.Label(window, text="not connected")
        latency = tk.Label(window, text="not connected")
        ID.grid(column=0,row=i+3)
        Ori.grid(column=1,row=i+3)
        act.grid(column=2,row=i+3)
        hs.grid(column=3,row=i+3)
        ca.grid(column=4,row=i+3)
        loc.grid(column=5,row=i+3)
        remark.grid(column=6,row=i+3)
        port.grid(column=7,row=i+3)
        latency.grid(column=8,row=i+3)
        idList.append(ID)
        oriList.append(Ori)
        actionList.append(act)
        hsList.append(hs)
        caList.append(ca)
        locList.append(loc)
        remarkList.append(remark)
        portList.append(port)
        latencyList.append(port)
        

    # label.pack()
    dataupdate()
    set_label()
    window.mainloop() #must

def issueCMD():
    while(True):
        time.sleep(0.1)
        for robot in robotlist:
            # print(robot.arindex,robot.action)
            if((robot.action!='')):
                
                if(robot.handshake):
                    print(lib.logg(),"Sending CMD", robot.action,"to ", robot.arindex," using ip ",robot.conn.ip,robot.conn.port)
                    lib.send(robot.conn.s,robot.action)

                
                if(robot.getContFlag()):
                    print(lib.logg(),"doing cont function")
                    robot.action=robot.contAction
                    print(lib.logg(),"Robot.action:",robot.action,robot.orientation)
                    analyzeSpecificCMD(robot.action,robot)
                else:
                    robot.clearAction()
                print(lib.logg(),"Sent CMD to ", robot.arindex)
# --------------------------------Program starts------------------------------------#
if __name__ == '__main__':
    # def __main__() :
    print("Sever Program")
    global cliState
    # global cliConnection
    cliState = False
    global general_cmd
    global robotlist
    l:list[lib.Robot]=[]
    robotlist=l
    t = Thread(target=GUI)
    t.start()
    t = Thread(target=acceptRobot)
    t.start()
    # camProcess = mp.Process(target=acceptCam)
    # camProcess.start()
    t = Thread(target=acceptCam)
    t.start()  
    t = Thread(target=acceptCLI)
    t.start()

    # while(True):
    #     # for robot in robotlist:
    #     #     try:
    #     #         lib.send(robot.conn.s,robot.action)
    #     #     except:
    #     #         print("couldn't send msg")
    while(True):
        start = time.time()
        for robot in robotlist:
            # print(robot.arindex,robot.action)
            if((robot.action!='')):
                
                if(robot.handshake):
                    print(lib.logg(),"Sending CMD", robot.action,"to ", robot.arindex," using ip ",robot.conn.ip,robot.conn.port)
                    lib.sendline(robot.conn.s,robot.action)
                    
                
                
                if(robot.getContFlag()):
                    print(lib.logg(),"doing cont function")
                    robot.action=robot.contAction
                    print(lib.logg(),"Robot.action:",robot.action,robot.orientation)
                    analyzeSpecificCMD(robot.action,robot)
                else:
                    robot.clearAction()
                print(lib.logg(),"Sent CMD to ", robot.arindex)
        print('[main]cycle time: ',time.time()-start)