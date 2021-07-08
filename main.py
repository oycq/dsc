import socket
import struct
import time 
import sys
import threading
import re
from pyquaternion import Quaternion
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 7755))
fig = plt.figure(figsize=(10, 10))
ax = Axes3D(fig)
plt.xlabel("X axis")
plt.ylabel("Y axis")
#$plt.zlabel("Z axis")
ax.set_xlim3d([-1.2, 1.2])
ax.set_ylim3d([-1.2, 1.2])
ax.set_zlim3d([-1.2, 1.2])

quat = Quaternion((0, 0, 0, 1))
def get_data():
    global quat
    while(1):
        data, addr = s.recvfrom(1024) # buffer size is 1024 bytes
        a = re.findall(r"[-+]?\d*\.\d+|\d+", data)
        #quat = Quaternion((float(a[3]),float(a[0]),float(a[1]),float(a[2])))
        quat = Quaternion((float(a[3]),-float(a[1]),-float(a[2]),float(a[0])))
x = threading.Thread(target=get_data)
x.daemon = True
x.start()
time.sleep(0.33)

q_init = 0
for i in range(10):
    q_init += quat * 0.1

while(1):
    #q_delta = quat.conjugate * q_init
    q_delta = q_init.conjugate * quat
    #q_delta = q_init * quat.conjugate
    del ax.lines[:]
    ax.plot((0,0), (0,0), (0,0.5), lw=2, c="g")
    x = q_delta* Quaternion((0, 0, 0, -0.5))  * q_delta.conjugate
    ax.plot((0,x[1]), (0,x[2]), (0,x[3]), lw=2, c="r")
    y = q_delta* Quaternion((0, 0, 0.1, -0.5))  * q_delta.conjugate
    ax.plot((y[1],x[1]), (y[2],x[2]), (y[3],x[3]), lw=2, c="r")
    #x = q_delta* Quaternion((0, 0, 0, 1))  * q_delta.conjugate
    #ax.plot((0,x[1]), (0,x[2]), (0,x[3]), lw=2, c="g")
    #x = q_delta* Quaternion((0, 0, 1, 0))  * q_delta.conjugate
    #ax.plot((0,x[1]), (0,x[2]), (0,x[3]), lw=2, c="r")
    #x = q_delta* Quaternion((0, 1, 0, 0))  * q_delta.conjugate
    #ax.plot((0,x[1]), (0,x[2]), (0,x[3]), lw=2, c="b")


    plt.pause(0.0001)

s.close()

