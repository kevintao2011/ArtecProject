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

def findAruco(img,connected:bool,marker_size=4 , total_markers = 250,draw = True ):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    key=getattr(aruco,f'DICT_{marker_size}X{marker_size}_{total_markers}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    bbox,ids,_=aruco.detectMarkers(gray,arucoDict,parameters=arucoParam)
    # bbox = clock-wise position starting from top left corner
    
    # print(ids)
    # print('location',bbox)
    loclist = []
    
    #conncetion to server required
    if(connected):
        try:
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
                
        except:
            print('Server Connection lost')
            
            return False
    fpsstring = "FPS:" + str(fps)
    img = cv2.putText(img, str(len(bbox)),(50, 50),cv2.FONT_HERSHEY_SIMPLEX,1,(0, 255, 0),2)
    img = cv2.putText(img, fpsstring,(50, 100),cv2.FONT_HERSHEY_SIMPLEX,1,(0, 255, 0),2)
    if(connected):
        img = cv2.putText(img, 'Online Mode',(50, 150),cv2.FONT_HERSHEY_SIMPLEX,1,(0, 255, 0),2)
    else:
        img = cv2.putText(img, 'Offline Mode',(50, 150),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 0, 0),2)
    
    try:
        print(bbox)
        print(bbox[0][0][0][0])
        # (array([[[660., 311.],
        # [745., 291.],
        # [783., 372.],
        # [689., 396.]]], dtype=float32),)
        
        idlist:list
        idlist = ids.tolist()
        print('id written:',idlist)
        for i in range(len(idlist)) :
            print(i,'id written solo:',idlist[i][0])
            print('id locs:',bbox)
            print('id loc:',bbox[i][0][0][0])
            img = cv2.putText(img, str(idlist[i][0]),(int(bbox[i][0][0][0]), int(bbox[i][0][0][1])),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0, 0),2)
    except:
        pass
    aruco.drawDetectedMarkers(img,bbox)
    return True
#Functions
 
if __name__ == "__main__":   
       
    #-- Camera Init --
    VideoCap = True
    cap=cv2.VideoCapture(0,  cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,800)

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
    
    # Connection Init
    terminate = False
    while not terminate:
        haveServer=False
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(ADDR)
            print("connected")
            # send("From Object detection")
            haveServer=True
        except:
            print('Run in no server Mode ')
        
        # Connection Init
        sendtime = time.time()        
        while True:
            # print("Hi")
            if VideoCap: _,img = cap.read()
            else:
                pass
            if cv2.waitKey(1)==113 :
                terminate = True
                break
            
            if cv2.waitKey(1)==114:
                print('try reconnect')
                try:
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client.connect(ADDR)
                    print("connected")
                    # send("From Object detection")
                    haveServer=True
                except:
                    print('Run in no server Mode ')
            if cv2.waitKey(1)==100:
                print('Disconnect')
                try:
                    client.close()
                    print("Disconnected")
                    # send("From Object detection")
                    haveServer=False
                    print('Run in no server Mode ')
                except:
                    print('sth wrong')
            
            if(not findAruco(img,haveServer)):
                break
            cv2.imshow("img",img)
    
