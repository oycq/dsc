import struct
import numpy as np
import sys

txt = open('./save.txt')
txt_data = txt.readline().split(" 00 00 00 0A ")[1:-1]
data = np.zeros((len(txt_data),17))
ii = -1
for i in range(len(txt_data)):
    convert_line = ''
    struct_bytes = txt_data[i].split(' ')
    if struct_bytes[-1] != '08' or len(struct_bytes) != 69:
        continue
    else:
        ii += 1
        struct_bytes = struct_bytes[:-1]
    for j in range(17):
        float_bytes  = ''
        for k in range(4):
            float_bytes = float_bytes + struct_bytes[(3-k)+j*4]
        float_data = struct.unpack('!f', bytes.fromhex(float_bytes))[0]
        data[ii][j] = float_data
        convert_line += str(float_data) + ','
    convert_line= convert_line[:-1] + '\n'
print(ii)

import matplotlib.pyplot as plt
import numpy as np

plt.scatter(range(ii),data[:ii,10])
plt.scatter(range(ii),data[:ii,11])
plt.scatter(range(ii),data[:ii,12])


plt.show()
