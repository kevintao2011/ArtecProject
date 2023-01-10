import socket
import sys
sys.path.append('./')
import lib
import serverThread
from threading import Thread
import json

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
        
            
def updateloc(c:lib.connection):
    global camConnection
    camConnection =c
    camConnection.s.setblocking(False)
    global cameraState
    cameraState = True
    print(lib.logg(), "Camera is Connected on port ",camConnection.port)
    try: 
        cam = lib.recv(camConnection.s)
    except:
        print(lib.logg(),"Cam cannot receive handshake")     
    
    while(True):
        listForUpdate = []
        try: #get data part and create list for update
            
            rawdata = lib.recvdata(camConnection.s)
        except:
            pass
            print("No data")
            rawdata = None
        
        try:# put list of robot to be update into list and execute updates
            recvLocJson = json.loads(rawdata.data['data'])
            for i in range(len(recvLocJson)): 
                listForUpdate.append(recvLocJson[i]['index'][0])
            print("captured robots'ID",listForUpdate)
            if listForUpdate.count>0:
                for i in listForUpdate: #for # of detected robot
                    print("captured robots'ID",i)
                    for robot in robotlist:
                        if int(robot.arindex) == int(i):
                            robot.setloc(recvLocJson[0]['coordination'][0],recvLocJson[0]['orientation'])
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
            analyzeCMD(general_cmd)
        except:
            print(lib.logg(), "sth goes wrong,close connection")
            c.s.close()
            alive = False
            
def analyzeCMD(message:lib.msg):
    print(lib.logg(),"calling analyze cmd")
    #CMD type: onee-time, continue, mass,specific
    try:
        cmdstr = message.getCMD()
        cmdstr = cmdstr.split(",")
    except:
        pass
    if(len(cmdstr)==1):
        cmdstr=cmdstr[0]
        print("command to all")
        for robot in robotlist:
            robot.action = cmdstr
            print(lib.fnlogg(),"updated action of all")
    else:
        print(lib.fnlogg(),"specific cmd")
        print(lib.fnlogg(),"cmdstr: ",cmdstr)
        command = cmdstr[len(cmdstr)-1]
        print(lib.fnlogg(),"popped")
        for targets in cmdstr:
            print(lib.fnlogg(),"target: ",targets)
            for robot in robotlist:
                if(robot.arindex==targets):
                    robot.action = command
                    print(lib.logg(),"updated action of",robot.arindex)
            
#--------------------------------CLI interface-------------------------#

#--------------------------------Robt Interface------------------------#
            
    
def acceptRobot():
    
    ROBOTserver = socket.create_server(lib.ROBOT_ADDR,family=socket.AF_INET,dualstack_ipv6=False)
    ROBOTserver.listen()
    print(lib.logg(), "ROBOT Server Listening at ",lib.ROBOT_ADDR)
    while(True):
        duplicated = False
        ROBOTserver.setblocking(True)
        s = ROBOTserver.accept()
        ID = lib.recv(s[0])
        print("RobotList",len(robotlist))
        for robot in robotlist:
            # s[0] = socket and [1] = ip+port
            if s[1][0] == robot.conn.ip:
                print(lib.logg(),'this ip is duplicated!')
                robot.updateConnection(s)
                duplicated = True 
        if not duplicated:
            s = lib.connection(s)
            r=lib.Robot(id=ID,conn=s)
            robotlist.append(r)# list socket 
            r.displayInfo()
            print(lib.logg(),'New Artec is Registered')
#--------------------------------Robt Interface------------------------#
        
        
# def __main__() :
print("Sever Program")
global cliState
global cliConnection
cliState = False
t = Thread(target=acceptCam)
t.start()  
t = Thread(target=acceptCLI)
t.start()
t = Thread(target=acceptRobot)
t.start()

global general_cmd
global robotlist
l:list[lib.Robot]=[]
robotlist=l

while(True):
    
    try:
        for robot in robotlist:
            if((robot.action!='')):
                print(lib.logg(),"Sending CMD", robot.action,"to ", robot.arindex," using ip ",robot.conn.ip,robot.conn.port)
                lib.send(robot.conn.s,robot.action)
                robot.action=''
                print(lib.logg(),"Sent CMD to ", robot.arindex,)
            pass
    except:
        #No CMD to send
        pass