import struct
import numpy as np
import sys

txt = open('./sav2.txt')
txt_data = txt.readline().split(" 00 00 00 0A ")[1:-1]
data = np.zeros((len(txt_data),3))
ii = -1
for ident in range(5):
    ident = ident + 1
    output_txt = open('6050_convert_%d.csv'%ident,'w')
    for i in range(len(txt_data)):
        convert_line = ''
        struct_bytes = txt_data[i].split(' ')
        if struct_bytes[-1] != '0%d'%ident or len(struct_bytes) != 13:
            continue
        else:
            ii += 1
            struct_bytes = struct_bytes[:-1]
        for j in range(3):
            float_bytes  = ''
            for k in range(4):
                float_bytes = float_bytes + struct_bytes[(3-k)+j*4]
            float_data = struct.unpack('!f', bytes.fromhex(float_bytes))[0]
            data[ii][j] = float_data
            convert_line += str(float_data) + ','
        convert_line= convert_line[:-1] + '\n'
        output_txt.write(convert_line)

