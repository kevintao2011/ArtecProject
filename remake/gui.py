import sys
sys.path.append('./')
import lib
import tkinter as tk
import socket

def GUI(list):
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

if __name__=="__main__":
    l:list[lib.Robot]=[]
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.connect((lib.SERVER,lib.GUI_PORT))
        #send in neste Dict with key = robot id, sub key is properties, 
        robotData = lib.recvForGUI()
        er
        
