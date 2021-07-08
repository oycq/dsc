import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import time
import math


def show3Dpose(vals, ax, lcolor="#3498db", rcolor="#e74c3c"): # blue, orange
  I   = np.array([1,2,5,4,6,5]) # start points
  J   = np.array([3,3,3,5,5,7]) # end points
  LR  = np.array([1,0,1,1,0,0], dtype=bool)
  for i in np.arange( len(I) ):
    x, y, z = [np.array( [vals[I[i], j], vals[J[i], j]] ) for j in range(3)]
    ax.plot(x, y, z, lw=2, c=lcolor if LR[i] else rcolor)


#fig = plt.figure(figsize=(19.2, 10.8))
fig = plt.figure(figsize=(10.8, 10.8))
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
angle = 0
for i in range(90):
    angle = angle + 1
    t1 = time.time()
    angle_rad = math. radians(angle)
    vals[2,0] = 100 * math.sin(angle_rad)
    vals[2,2] = 100 - 100 * math.cos(angle_rad)
    print(vals[2])
    show3Dpose(vals, ax)
    plt.pause(0.001)
    del ax.lines[:]
    t2 = time.time()
    #print((t2-t1)*1000)

show3Dpose(vals, ax)
plt.show()

