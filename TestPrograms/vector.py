import math
import numpy as np
def vectorAngle(p1,p2): #ee 2104
    # print('p1[0]',p1[0])
    # print('p1[1]',p1[1])
    # print('p2[0]',p2[0])
    # print('p2[1]',p2[1])
    p1 = [p1[0]+ 1j*p1[1]]
    p2 = [p2[0]+ 1j*p2[1]]
    vector1 = np.array(p1)
    vector2 = np.array(p2)
    # r = -vector1 + vector2 #from p1 to p2
    r =  -vector1+vector2 
    # r = np.conjugate(r)
    print(r[0])
    #np angle return The counterclockwise angle from the positive real axis on the complex plane 
    # return int(np.angle(r,True))
    if (int(np.angle(r,True))<0):
        return (450+int(np.angle(r,True)))%360
    else:
        return (90+int(np.angle(r,True)))%360
a=(0,0)
pos = []
r = 300
t = 0
stepSize = 0.2

while t < 2 * math.pi:
    x = r * math.cos(t)
    y = r * math.sin(t)
    pos.append((x,y))
    t += stepSize
print(pos)
angles = []
for co in pos:
    angles.append(vectorAngle(co,a))
for i in range(len(pos)):

    print(pos[i]," ",angles[i])

print(vectorAngle((69,172),(700,500)))