import socket 
import threading
import json
import time
from unittest import case
import _thread
FIELD_SIZE = (640,240)
devicelist = []

HEADER = 64

# SERVER = "192.168.1.8"
# SERVER = "192.168.1.17"
# SERVER = "192.168.1.40"
SERVER = "127.0.0.1"
# SERVER = "10.22.1.126" #winstar
# SERVER = "192.168.0.181" #
# SERVER = "172.20.10.12" #phone
# SERVER = "192.168.31.36" #Xiaomi
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
general_cmd = ""
# lock = threading.Lock()

class device(object):
    def __init__(self, addr ,connObj):
        self.addr = addr  # 
        self.index = len(devicelist)   # need change
        self.connObj = connObj 
        self.nextAction = ""
        print("Host :Created new device")
        print("Host :device ip is", self.addr)
        print("Host :device index is",self.index)
    
        
class Robot(device):
    robotlist = []
    def __init__(self, addr ,connObj):
        device.__init__(self, addr ,connObj)
        self.robotlist.append(self)
        self.location = (0,0)
        self.orientation = 0
        self.arindex = -1
        # sequence -> lt , rt , rb, lb
        self.p1 = (0,0)
        self.p2 = (0,0)
        self.p3 = (0,0)
        self.p4 = (0,0)
        self.CLI_cmd = "Keep Standby"
        print("Added new Robot")
    def setloc(self,locations,orientation): 
    #self = robotobj , locations = list of list , orientation = number
        self.p1 = (locations[0][0],locations[0][1])
        self.p2 = (locations[1][0],locations[1][1])
        self.p3 = (locations[2][0],locations[2][1])
        self.p4 = (locations[3][0],locations[3][1])
        self.location = ((self.p1[0]+self.p3[0])/2,(self.p1[1]+self.p3[1])/2)
        self.orientation = orientation
        print("Loc updated")
    def displayInfo(self):
        print("**********Information**********")
        print("Ar Tag index:     ",self.index)
        if (self.arindex==-1):
            print("Ar Tag index:     ","Registered but not yet recognised by Camera")
        else:
            print("Ar Tag index:     ",self.arindex)
        print("IP address:       ",self.addr)
        print("location:         ",self.location)
        print("orientation:      ",self.orientation)
        
        print("**********Information**********")
    
class msg:
    def __init__(self,cmd,data):
        self.cmd = cmd
        self.data = data

# class msg:
#     def __init__(self,source,target,command):
#         self.source = source
#         self.target = target
#         self.cmd = command
        
class locInfo:
    def __init__(self,index,coordination,orientation):
        self.index = index
        self.coordination = coordination
        self.orientation = orientation
        
def getConnected():
    return devicelist

def terminal_thread(robot,command):
    time.sleep(3)
    cmdmsg = msg(robot.addr,robot.connObj)
    command.split(",")
    robot = devicelist[robot.index]
    #robot.connObj.send("wtauohiweduijwh djahjkawhdjkaw nkdywcwqycadca.".encode(FORMAT)) #can actively send  cmd


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def convertJson(text):
    print('Function: convertJson')
    mymsg = json.dumps(msg("Host",text).__dict__) #_dict_ send in plaint json text
    return mymsg

def handle_client(conn:socket, addr): #Thread function
    global general_cmd # access the global CLI_cmd variable
    # print(f"[NEW CONNECTION] {addr} connected.")
    duplicated = False
    currentDevice= any
    
    
    # Now many local connection, current program cannot classify them
    for devices in devicelist: #Check if new connection
        print("Host : Old addr:",devices.addr," New addr:",addr)
        if (devices.addr[0]==addr[0] and addr[0]!=SERVER): #if duplicated
            print("Host : device Duplicated")
            devices.addr = addr
            devices.connObj = conn
            for robots in Robot.robotlist:
                if robots.addr[0]==addr[0]:
                    robots.addr = addr
                    robots.connObj = conn
            print("Host : Updated socket") #reconnection will chg socket and the cnnection
            duplicated = True
            currentDevice= devices
            
    if(not duplicated): #Check if it is new device
        print("addr: " , addr)
        if(addr[0]!=SERVER):
            thisRobot = Robot(addr,conn)
            print("New Robot joined!")
            print(len(Robot.robotlist))
            devicelist.append(device(addr,conn))
        else:
            devicelist.append(device(addr,conn))
        currentDevice= devicelist[len(devicelist)-1]
        # print("registered new device:," )
        # print("IpAddress =" ,addr)
        # print("Index",devicelist[len(devicelist)-1])
        
    getConnected() # show connected device
    
    print("currentDevice",currentDevice.index)
    connected = True
    while connected: #close loop for waiting message
        
        # bufsize should be a relatively small power of 2, for example, 4096
        msg_length = conn.recv(HEADER).decode(FORMAT) 
        
        
        if msg_length:
            print()
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            _thread.start_new_thread(terminal_thread,(currentDevice,"connected"))
            if msg == DISCONNECT_MESSAGE: #close connection
                connected = False
                
            #print("All Msg: "f"{msg}") #print the msg
            
            # check sending source
            elif(msg == "Connect form studuino bit"): 
                for x in range (len(devicelist)):
                    print("Index: ",devicelist[x].index," IP:",devicelist[x].addr)
            
            elif (msg == "From CLI"):
                conn.send(("Msg received:"f"{msg}".encode(FORMAT)))
            elif (msg == "From Object detection"):
                conn.send(("Msg received:"f"{msg}".encode(FORMAT)))    
            
            
            # check received command
            elif msg[0]=='{': #if receiving a JSON TEXT
                print("Host :receiveing JSON")
                data = json.loads(msg)
                
                print('Receiving cmd:',data['cmd'])
                print('Receiving data:',data['data'])
                print("Type",type(data))
                
                
                # for studuino response 
                if(data['cmd']=="Request"): #if it is regular update from robot
                    print(currentDevice.index,"From device: Requesting")
                    # if(currentDevice.nextAction==""):
                    # if(local_CLI_cmd==""):#if there is an command issued to that robot
                    #     conn.send(("Keep Standby".encode(FORMAT)))
                    # else: #if(currentDevice.nextAction==data['data']):
                    #     conn.send((local_CLI_cmd.encode(FORMAT)))
                    
                    
                    # add check if this device is robot , if robot have arindex then dun need to this
                    print(len(Robot.robotlist))
                    for robot in Robot.robotlist:
                        print("conn:",conn," New addr:",robot.connObj)
                        if(conn==robot.connObj):
                            robot.arindex=data['data']
                            print("Orientation:",robot.orientation) 
                            if(robot.CLI_cmd)=='90':
                                ori = int(robot.orientation)
                                if(ori<80):
                                    robot.CLI_cmd = 'cw' 
                                elif(ori>100):
                                    robot.CLI_cmd = 'ccw'
                                else: 
                                    robot.CLI_cmd = 'stop'
                                print("action = ", robot.CLI_cmd)
                                conn.send((robot.CLI_cmd.encode(FORMAT)))
                                robot.CLI_cmd = '90'
                            else:
                                print("action = ", robot.CLI_cmd)
                                conn.send((robot.CLI_cmd.encode(FORMAT)))
                            
                        # if(robot.CLI_cmd==""):#if there is an command issued to that robot
                        #     conn.send(("Keep Standby".encode(FORMAT)))
                        # else: #if(currentDevice.nextAction==data['data']):
                        
                            
                            
                # for CLI
                elif(data['cmd']=="Host"):
                    print(currentDevice.index,"CLI: Sending action to host")
                    if(len(data['data'].split(","))==1):
                        print("General command")
                        for robot in Robot.robotlist:
                            robot.CLI_cmd = data['data']
                            
                    else:
                        try:
                            print("specific command")
                            target = data['data'].split(",")[0]
                            print("Target: ",target)
                            action = data['data'].split(",")[1]
                            print("Action: ",action)
                            for robot in Robot.robotlist:
                                print(robot.arindex,target)
                                if(int(robot.arindex)==int(target)):
                                    robot.CLI_cmd = action
                            # command = ['data'].split(",")
                            # target = []
                            # for i in range(len(command)-1):
                            #     target.append(command[i])
                            # print("Target: ",target)
                            # action = command[len(command)-1]
                            # print("Action: ",action)
                            # for robot in Robot.robotlist:
                            #     print("General command")
                            #     print(robot.arindex,target)
                            #     for i in range(len(target)):
                            #         if(int(robot.arindex)==int(target[i])):
                            #             robot.CLI_cmd = action
                        except:
                            print("Robot not existed!")
                    #CLI_cmd = data['data']
                    # print("CLI_cmd:",local_CLI_cmd)
                    print("Sending Repond........")
                    conn.send("Received".encode(FORMAT)) #to cli
                    
                    
                #For Camera    
                elif(data['cmd']=="OD"):
                    conn.send("Device Location Received from server".encode(FORMAT)) #to OD
                    #{'cmd': 'OD', 
                    # 'data': '[{"index": [[9]], "coordination": [[271.0, 367.0], [242.0, 260.0], [325.0, 235.0], [356.0, 351.0]],
                    # "orientation": 255}]'}
                    
                    print(type(data['data']['data']))
                    recvLocJson = json.loads(data['data']['data'])
                    #x [{'index': [[8], [9], [0]], 
                    # 'coordination': [[385.0, 468.0], [324.0, 407.0], [360.0, 334.0], [426.0, 398.0]], 'orientation': 225}, {'index': [[8], [9], [0]], 'coordination': [[385.0, 468.0], [324.0, 407.0], [360.0, 334.0], [426.0, 398.0]], 'orientation': 222}, {'index': [[8], [9], [0]], 'coordination': [[385.0, 468.0], [324.0, 407.0], [360.0, 334.0], [426.0, 398.0]],
                    # 'orientation': 225}]
                    print("recvLocJson",recvLocJson)
                    print(recvLocJson[0]['index'][0])
                    print(recvLocJson[0]['coordination'][0]) # Coordination of 1st robot
                    
                    listForUpdate = []
                    for i in range(len(recvLocJson)):
                        listForUpdate.append(recvLocJson[i]['index'][0])
                    print("captured robots'ID",listForUpdate)
                        
                    for i in listForUpdate: #for # of detected robot
                        print("captured robots'ID",i)
                        for robot in Robot.robotlist:
                            print("Checking match ar tag")
                            print(robot.arindex, "==" ,i)
                            if int(robot.arindex) == int(i):
                                print("updating loc of robot-ID: ",i)
                                print(recvLocJson[0]['coordination'][0])
                                print(recvLocJson[0]['orientation'])
                                robot.setloc(recvLocJson[0]['coordination'][0],recvLocJson[0]['orientation'])
                                
                    for robot in Robot.robotlist:
                        robot.displayInfo()
            #recvLocJson 
            # [{'index': [[8], [0], [9]], 
            # 'coordination': [[401.0, 330.0], [387.0, 455.0], [291.0, 443.0], [304.0, 316.0]], 
            # 'orientation': 96},
            # {'index': [[8], [0], [9]], 
            # 'coordination': [[401.0, 330.0], [387.0, 455.0], [291.0, 443.0], [304.0, 316.0]], 
            # 'orientation': 95},
            # {'index': [[8], [0], [9]], 
            # 'coordination': [[401.0, 330.0], [387.0, 455.0], [291.0, 443.0], [304.0, 316.0]], 
            # 'orientation': 95}]
                else:
                    conn.send("Not a command".encode(FORMAT))
            else:
                conn.send("Unrecognised communication".encode(FORMAT))
                    
        #lock.release()       
                
            
    conn.close()
    print("Ended connection with ", addr)
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
start()

