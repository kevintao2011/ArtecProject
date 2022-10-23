import json
import socket

# from server import Robot

class msg:
    def __init__(self,source,target=[-1],cmd = "Null"):
        self.source = source
        self.target = target
        self.cmd = cmd
        
    def __init__(self,cmd,data):
        self.cmd = cmd
        self.data = data
    
    
    def decode (message):
        try:
            jsondict = json.loads(message)
            msgObj = msg(jsondict["source"],jsondict["target"],jsondict["cmd"])
            return msgObj
        
        except:
            return message #return a String
            
   
def isJSON(Text):
    try:
        return json.dumps(Text)
    except:
        return False         
    
        



class device:
    numberOfDevice = 0
    devicelist = []
    def __init__(self, addr ,connObj,role):
        
        self.addr = addr  # 
        self.index = len(self.devicelist)   # need change
        self.connObj = connObj 
        self.nextAction = ""
        self.role = role #put the first handshake msg sting here
        #Cli, ob (Same ip from )
        #robot (different robot)
        self.devicelist.append(self)
        self.numberOfDevice = len(self.devicelist)
        
        
        
        duplicate = False
        for Adevice in self.devicelist:
            if self.addr[0] == Adevice.addr[0]: #device reconnection/ new connection from host 
                if self.addr[0] == "localhost": #May be cli or optical detection process 
                    if Adevice.role == self.role : #same role existed before --> update
                            Adevice.addr == self.addr 
                            Adevice.connObj == self.connObj
                            Adevice.role == self.role
                            self.__del__() #delet since just need update the existing obj
                            raise Exception("Existed")
                    else: #same role from host not existed before --> pass to create
                        pass #Unfinished
                else: #duplicate not from host --> update
                    pass #Unfinished
            else:
                pass
        
        # duplicated = False
        # currentDevice= any
        # # Now many local connection, current program cannot classify them
        # for devices in devicelist: #Check if new connection
        #     print("Host : Old addr:",devices.addr," New addr:",addr)
        #     if devices.addr[0]==addr[0]: #if duplicated
        #         print("Host : device Duplicated")
        #         devices.addr = addr
        #         devices.connObj = conn
        #         print("Host : Updated socket") #reconnection will chg socket and the cnnection
        #         duplicated = True
        #         currentDevice= devices
                
        # if(not duplicated): #Check if it is new device
        #     print("addr: " , addr)
        #     devicelist.append(device(addr,conn))
        #     currentDevice= devicelist[len(devicelist)-1]
        #     # print("registered new device:," )
        #     # print("IpAddress =" ,addr)
        #     # print("Index",devicelist[len(devicelist)-1])
            
        print("Host :Created new device")
        print("Host :device ip is", self.addr)
        print("Host :device index is",self.index)
        print("Host :Number of connnected device")
                        
                            
                                
                        
    def getDeviceCount(self):
        return self.numberOfDevice
    
    def __del__(self,reason):
        print("Device object is destoyed/not yet create becoz of:",reason)
    
        
class robot(device):
    def __init__(self, addr ,connObj):
        device.__init__(self, addr ,connObj)
        self.location = (0,0)
        self.p1 = (0,0)
        self.p2 = (0,0)
        self.p3 = (0,0)
        self.p4 = (0,0)
        self.numberOfDevice+=1
    def setloc(self,locations): #location is list of list
        self.p1 = (locations[0][0],locations[0][1])
        self.p2 = (locations[1][0],locations[1][1])
        self.p3 = (locations[2][0],locations[2][1])
        self.p4 = (locations[3][0],locations[3][1])
    
# message = msg("Me")
# CLI = device(1,2,"robot")
# Artec1 = robot(1,2,"robot")
# print("Number of Devicess: ", Artec1.numberOfDevice)

# print(message.cmd) 

class A(object):
    lista = []
    
    def __new__(self,number):
        instance=object.__new__(self)
        # try:
        for i in range(len(self.lista)):
            if number == self.lista[i].number:
                print("Duplicated!")
                return None
                # raise Exception()
        else:
            return instance
        # except:
        #     print("is 1!")
        #     del self
    # def __del__(self):
    #     print("Destructor called")
    def __init__(self,number):
        self.lista.append(self)
        self.number = number
        print("Created!")
        
a = A(1)
a = A(1)
b = A(2)
c = A(3)
d = A(4)
for i in d.lista:
    print(i.number)

listB = [1,2,3,4,5]
print(1 in listB)
print("length of list: ",len(d.lista))
print(b.__dict__)

txt = "this"
cmd = txt.split(",")
print(cmd)

class b:
    
    blist = []
    def __init__(self, num):
        self.num=num
        self.blist.append(self)
        
class c(b):
    def __init__(self, num):
        b.__init__(self, num)
        self.num=num
        
          
p = c(2) 
print(b.blist[0],p)
print(b.blist[0]==(p))
