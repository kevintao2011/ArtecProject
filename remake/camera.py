# lib for camera dfetection
from symbol import parameters


import cv2 as cv2
import cv2.aruco as aruco
import numpy as np
# lib for camera dfetection

# Init for Connection
import socket
import json
# Init for Connection

import sys
sys.path.append('./')
import lib
import time

    
#-- Camera Init --
VideoCap = True
cap=cv2.VideoCapture(0, 700)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

fps = int(cap.get(5))
# _, frame = cap.read()
#-- Camera Init --


# Connection variable
HEADER = 64
SERVER = lib.SERVER
PORT = lib.CAM_PORT
ADDR = lib.CAM_ADDR
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
# Connection variable

#Object Detection Var
loclist = []

#Object Detection Var

#Class used 
class msg:
    def __init__(self,cmd,data):
        self.cmd = cmd
        self.data = data
        
class locInfo:
    def __init__(self,index,coordination,orientation):
        self.index = index
        self.coordination = coordination
        self.orientation = orientation
        
#Class used 

#Functions
def send(msg):
    """_summary_
    send function in camera.py, send msg length & camdata 
    Args:
        msg (_type_): _description_
    """
    print('[SEND]msg = ',msg)
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    # a = client.recv(2048).decode(FORMAT)
    # print(a)
    
def jsonSend(sender,text): # send JSON with  cmd:host data:unify action
    #print("sent request")
    # print('Function: jsonSend')
    # mymsg = json.dumps(msg("OD",text).__dict__) #_dict_ send in plaint json text
    mymsg = lib.msg("OD",text).toJSON() #edited
    # print(lib.logg(),"dumped")
    send(mymsg)
    # print(lib.logg(),"sent")

def vectorAngle(p1,p2): #ee 2104
    p1 = [p1[0]+ 1j*p1[1]]
    p2 = [p2[0]+ 1j*p2[1]]
    vector1 = np.array(p1)
    vector2 = np.array(p2)
    r = -vector1 + vector2 #from p1 to p2
    if (int(np.angle(r,True))<0):
        return 360+int(np.angle(r,True))
    else:
        return int(np.angle(r,True))

def convertJson(text):
    print('Function: convertJson')
    mymsg = json.dumps(msg("Host",text).__dict__) #_dict_ send in plaint json text
    return mymsg

def findAruco(img,marker_size=4 , total_markers = 250,draw = True):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    key=getattr(aruco,f'DICT_{marker_size}X{marker_size}_{total_markers}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    bbox,ids,_=aruco.detectMarkers(gray,arucoDict,parameters=arucoParam)
    # bbox = clock-wise position starting from top left corner
    
    print(ids)
    # print('location',bbox)
    loclist = []
    
    for i in range (len(bbox)):
        
        id = ids.tolist()
        p1 = bbox[i][0][0].tolist()
        p2 = bbox[i][0][1].tolist()
        # print("type p1",type(p1))
        # print("type p2",type(p2))
        # print("type angle:",type(vectorAngle(p1,p2)))
        loclist.append(locInfo(id[i],bbox[i].tolist(),vectorAngle(p1,p2)))
        
        # print("locList: ",loclist[0].__dict__)
    for i in loclist:
        print("i.orientation: ",i.orientation)
    fpsstring = "FPS:" + str(fps)
    if (len(bbox)>0):
        locJSON = json.dumps([ob.__dict__ for ob in loclist])
        # print("locJSON passed")
        msgTxt = msg("OD",locJSON).__dict__
        # msgTxt = lib.msg("OD",locJSON).toJSON
        print("MSG TXT : ",msgTxt , type(msgTxt))
        
        # if ((time.time()-sendtime)>0.1):
        #     jsonSend(lib.showtime(),msgTxt)
        #     sendtime=time.time()
        jsonSend(lib.showtime(),msgTxt)
        # time.sleep(0.05)
        # lib.send(client,msgTxt)
    
    img = cv2.putText(img, str(len(bbox)),(50, 50),cv2.FONT_HERSHEY_SIMPLEX,1,(0, 255, 0),2)
    img = cv2.putText(img, fpsstring,(50, 100),cv2.FONT_HERSHEY_SIMPLEX,1,(0, 255, 0),2)
    
    aruco.drawDetectedMarkers(img,bbox)
#Functions
 
if __name__ == "__main__":    
    # Connection Init
 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print("connected")
    send("From Object detection")
    
    # Connection Init
    sendtime = time.time()        
    while True:
        # print("Hi")
        if VideoCap: _,img = cap.read()
        else:
            pass
        if cv2.waitKey(1)==113:
            break
        findAruco(img)
        cv2.imshow("img",img)
    
