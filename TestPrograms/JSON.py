import json
import numpy as np

data = [1,3,4,6]

data2 = [{'A':13},
         {'Info':{
             'Name':'Kevin',
             'Age':11
         }}
        ]

dictA = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}
p1 = np.array([1,2])
p2 = np.array([3,5])
print(list(p1+p2))

class msg:
    def __init__(self,cmd,data):
        self.cmd = cmd
        self.data = data
    # def execute(thiscmd,thisdata):
    #     match(thiscmd):
    #         case 'motor':
    #             if thisdata == 

        
        
class locInfo:
    def __init__(self,index,coordination,orientation):
        self.index = index
        self.coordination = coordination
        self.orientation = orientation            
a = np.array([[
        [391., 325.]]])            
loc1 = locInfo(1,a.tolist(),
              273)

loc2 =locInfo(2,a.tolist(),
              233)

locl = []
locl.append(loc1)
locl.append(loc2)

# loc = locInfo(1,2,
#               273)
jsonData = json.dumps(data2)#converted to json string

print('JSON format:')
print('jsonData= ' ,jsonData)
print('jsonData[0] = ', jsonData[0])

#JSON in python: combination of list and dict
print('python obj format:')
pyData = json.loads(jsonData)
print(pyData[0])
print(type(pyData[0]['A']))

mymsg = msg("Request","Hi").__dict__
print(json.dumps(mymsg))
print(locl)
jsonl = json.dumps([ob.__dict__ for ob in locl])
locmsg = msg("OD",json.dumps([ob.__dict__ for ob in locl]))
print(locmsg)
# print(locmsg)

# {'cmd': 'OD', 'data': '[{"index": [[0], [9], [8]], "coordination": [
# [409.0, 179.0], [507.0, 234.0], [461.0, 360.0], [368.0, 300.0]], "orientation":
#  29}, {"index": [[0], [9], [8]], "coordination": [[409.0, 179.0], [507.0, 234.0
# ], [461.0, 360.0], [368.0, 300.0]], "orientation": 30}, {"index": [[0], [9], [8
# ]], "coordination": [[409.0, 179.0], [507.0, 234.0], [461.0, 360.0], [368.0, 30
# 0.0]], "orientation": 29}]'}