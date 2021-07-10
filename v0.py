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
while(1):
    data, addr = s.recvfrom(1024) # buffer size is 1024 bytes
    print(data)
