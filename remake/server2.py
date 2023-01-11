import socket
import sys
import threading
import time

from anyio import Lock
sys.path.append('./')
import lib
import serverThread
from threading import Thread
import json
import tkinter as tk

# global robotConnectionList
# robotConnectionList = []


# global camSocketList
global camConnection


#------------------------------CAM Part-----------------------------------#
def acceptCam():
    CAMserver = socket.create_server(lib.CAM_ADDR,family=socket.AF_INET,dualstack_ipv6=False)

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
    
    t = Thread(target=updateloc, args=(s,))
    t.start()
        
            
def updateloc(c:lib.connection):
    global camConnection
    camConnection =c
    
    global cameraState
    camhandshake = False
    print(lib.logg(), "Camera is Connected on port ",camConnection.port)
    
    while not camhandshake :
        try:
            handshakeID = lib.recv(camConnection.s)
            camhandshake = True
        except:
            print(lib.logg(),"Cam cannot receive handshake")     
    
    while(True):
        listForUpdate = []
        try: #get data part and create list for update
            empty = False
            counter = 0
            camdata = lib.recvdata(camConnection.s)
            
                
        except:
            pass
            # print("No data")
            camdata = None
        
        try:# put list of robot to be update into list and execute updates
            recvLocJson = json.loads(camdata.data['data'])
            # print(lib.fnlogg(),"Parsed cam data")
            print(recvLocJson)
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
        except:
            # print(lib.logg(),"No robot exits yet")
            pass
        
        
#------------------------------CAM Part-----------------------------------#


#--------------------------------CLI interface--------------------------------#
def acceptCLI():
    #Objective: Create a socket keep looking for cli
    CLIserver = socket.create_server(lib.CLI_ADDR,family=socket.AF_INET,dualstack_ipv6=False)
    CLIserver.listen()
    
    print(lib.logg(), "CLI Server Listening at ",lib.CLI_ADDR)
    while(True): 
        s = CLIserver.accept()
        s = lib.connection(s)
        lib.recv(s.s) #delet this when no handshake
        global cliConnection
        cliConnection = s  
        cliConnection.s.setblocking(True)
        global cliState
        cliState = True
        t = Thread(target=updateCommand, args=(s,))
        t.start()
def acceptCLIOnce():
    #Objective: Create a socket keep looking for cli
    CLIserver = socket.create_server(lib.CLI_ADDR,family=socket.AF_INET,dualstack_ipv6=False)
    CLIserver.listen()
    
    print(lib.logg(), "CLI Server Listening at ",lib.CLI_ADDR)
    s = CLIserver.accept()
    s = lib.connection(s)
    lib.recv(s.s) #delet this when no handshake
    global cliConnection
    cliConnection = s  
    global cliState
    cliState = True
    t = Thread(target=updateCommand, args=(s,))
    t.start()
        
def updateCommand(c:lib.connection):
    alive = True
    while(alive):
        try:
            #receive cli cmd
            # tmp =lib.recvdata(cliConnection.s)
            # access the global CLI_cmd variable
            print("waiting msg...")
            tmp =lib.recvdata(c.s)
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
            alive = False
        try:
            analyzeCMD(general_cmd)
        except:
            "No cmd"
def analyzeSpecificCMD(command:str,robot:lib.Robot):
    if (command=='dir'):
        robot.startContAction(command)
        ori = int(robot.orientation)
        print('Orientation: ',ori)
        if(ori<75):
            robot.action = 'cw' 
        elif(ori>105):
            robot.action = 'ccw'
        else: 
            robot.action = 'stop'
            print('90 Degree!')
            robot.endContAction()    
def analyzeCMD(message:lib.msg):
    targets = []
    command = ''
    print(lib.logg(),"calling analyze cmd")
    #CMD type: onee-time, continue, mass,specific
    try: #if mass
        cmdstr = message.getCMD()
        cmdstr = cmdstr.split(",")
    except: #otherwise
        pass
    if(len(cmdstr)==1):
        print(lib.fnlogg(),"cmdstr[0]:",cmdstr[0])
        if(cmdstr[0]=="display"):
            for robot in robotlist:
                robot.displayInfo()
            
        else:
            for robot in robotlist:
                targets.append(robot.arindex)
            command=cmdstr[0]
            print(lib.fnlogg(),"command to all")
            # for robot in robotlist:
            #     robot.action = cmdstr
            #     print(lib.fnlogg(),"updated action of all")
    else:
        print(lib.fnlogg(),"specific cmd")
        command = cmdstr[len(cmdstr)-1]
        print(lib.fnlogg(),"command: ",command)
        for ID in cmdstr:
            targets.append(ID)
    
     
    for target in targets:
        for robot in robotlist:
            if(robot.arindex==target):
                #find-grained control
                if ('dir' in command):
                    analyzeSpecificCMD(command,robot)

                #for consistent action like lighting or cw           
                else:
                    robot.action = command
                    print(lib.logg(),"updated action of",robot.arindex)
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
    
    ROBOTserver = socket.create_server(lib.ROBOT_ADDR,family=socket.AF_INET,dualstack_ipv6=False)
    ROBOTserver.listen()
    print(lib.logg(), "ROBOT Server Listening at ",lib.ROBOT_ADDR)
    while(True):
        duplicated = False
        # ROBOTserver.setblocking(False)
        
        s = ROBOTserver.accept()
        ID = lib.recv(s[0]) # handshake
        print("RobotList",len(robotlist))
        for robot in robotlist:
            # s[0] = socket and [1] = ip+port
            if s[1][0] == robot.conn.ip:
                print(lib.logg(),'this ip is duplicated!')
                robot.updateConnection(s)
                robot.handshake = True
                duplicated = True 
        if not duplicated:
            s = lib.connection(s)
            robot=lib.Robot(id=ID,conn=s)
            robot.handshake=True 
            robotlist.append(robot)# list socket 
            robot.displayInfo()
            print(lib.logg(),'New Artec is Registered')
#--------------------------------Robt Interface------------------------#
        

    
    
def GUI():
    def set_label():
        currentTime = lib.datetime.now()
        label['text'] = currentTime
        
        
        for robot in robotlist:
            oriList[int(robot.arindex)]['text']=str(robot.orientation)
            actionList[int(robot.arindex)]['text']=str(robot.action)
            hsList[int(robot.arindex)]['text']=str(robot.handshake)
            caList[int(robot.arindex)]['text']=str(robot.continuousActionFlag)
            locstr = str(robot.location[0])+" , "+str(robot.location[1])
            locList[int(robot.arindex)]['text']=locstr
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

    label = tk.Label(window, text="placeholder")
    label.grid(column=1,row=0)
    
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
    
    
    
    oriList =[]
    idList = []
    actionList =[]
    hsList = []
    caList = []
    locList = []
    for i in range (10):
        ID = tk.Label(window, text=str(i))
        Ori = tk.Label(window, text="not connected")
        act = tk.Label(window, text="not connected")
        hs = tk.Label(window, text="not connected")
        ca = tk.Label(window, text="not connected")
        loc = tk.Label(window, text="not connected")
        ID.grid(column=0,row=i+3)
        Ori.grid(column=1,row=i+3)
        act.grid(column=2,row=i+3)
        hs.grid(column=3,row=i+3)
        ca.grid(column=4,row=i+3)
        loc.grid(column=5,row=i+3)
        idList.append(ID)
        oriList.append(Ori)
        actionList.append(act)
        hsList.append(hs)
        caList.append(ca)
        locList.append(loc)
        

    # label.pack()
    dataupdate()
    set_label()
    window.mainloop() #must




def issueCMD():
    while(True):
        time.sleep(0.15)
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
          
# def __main__() :
print("Sever Program")
global cliState
global cliConnection
cliState = False
global general_cmd
global robotlist
l:list[lib.Robot]=[]
robotlist=l
t = Thread(target=GUI)
t.start()
t = Thread(target=acceptRobot)
t.start()
# acceptCamOnce()
# acceptCLIOnce()


lock = threading.Lock()


t = Thread(target=issueCMD)
t.start()

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
    