import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import time
import math

import socket
import struct
import sys
import threading

angles = [0,0,0]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 6000))
s.listen(0)
client, addr = s.accept()
client.settimeout(5)

angles = [0,0,0]

def get_data(client):
    global angles 
    while(1):
        content = client.recv(1024)
        angles_temp = []
        if len(content) == 73:
            for j in [10,11,12]:
                float_bytes  = ''
                for k in range(4):
                    float_bytes = float_bytes + '%.2x'%(content[(3-k)+j*4])
                float_data = struct.unpack('!f', bytes.fromhex(float_bytes))[0]
                angles_temp.append(float_data)
            angles = angles_temp
        else:
            print('...')
            pass


x = threading.Thread(target=get_data, args=(client,))
x.daemon = True
x.start()



def show3Dpose(vals, ax, lcolor="#3498db", rcolor="#e74c3c"): # blue, orange
  I   = np.array([1,2,5,4,6,5]) # start points
  J   = np.array([3,3,3,5,5,7]) # end points
  LR  = np.array([1,0,1,1,0,0], dtype=bool)
  for i in np.arange( len(I) ):
    x, y, z = [np.array( [vals[I[i], j], vals[J[i], j]] ) for j in range(3)]
    ax.plot(x, y, z, lw=2, c=lcolor if LR[i] else rcolor)


#fig = plt.figure(figsize=(19.2, 10.8))
fig = plt.figure(figsize=(10.8/2, 10.8/2))
ax = Axes3D(fig)
RADIUS = 200
ax.set_xlim3d([-RADIUS, RADIUS])
ax.set_zlim3d([0, RADIUS*2])
ax.set_ylim3d([-RADIUS, RADIUS])

ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])

ax.get_xaxis().set_ticklabels([])
ax.get_yaxis().set_ticklabels([])
ax.set_zticklabels([])

white = (1.0, 1.0, 1.0, 0.0)
ax.w_xaxis.set_pane_color(white)
ax.w_yaxis.set_pane_color(white)
# Keep z pane

ax.w_xaxis.line.set_color(white)
ax.w_yaxis.line.set_color(white)
ax.w_zaxis.line.set_color(white)



vals = np.zeros((10,3))
vals[1] = [0,-25,0]
vals[2] = [0,25,0]
vals[3] = [0,0,100]
vals[4] = [0,-30,80]
vals[5] = [0,0,150]
vals[6] = [0,30,80]
vals[7] = [0,0,170]

while(1):
    t1 = time.time()
    #print(angles[2])
    angle_rad = math.radians(angles[2])
    vals[2,0] = 100 * math.sin(angle_rad)
    vals[2,2] = 100 - 100 * math.cos(angle_rad)
    show3Dpose(vals, ax)
    plt.pause(0.04)
    del ax.lines[:]
    t2 = time.time()
    #print((t2-t1)*1000)

show3Dpose(vals, ax)
plt.show()


