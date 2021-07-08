import struct
txt = open('./save2.txt')
output_txt = open('6050_convert.csv','w')
data = txt.readline().split(" 01 00 00 00 0A ")[1:-1]
print(len(data))
for i in range(len(data)):
    convert_line = ''
    struct_bytes = data[i].split(' ')
    for j in range(17):
        float_bytes  = ''
        for k in range(4):
            float_bytes = float_bytes + struct_bytes[(3-k)+j*4]
        float_data = struct.unpack('!f', bytes.fromhex(float_bytes))[0]
        convert_line += str(float_data) + ','
    convert_line= convert_line[:-1] + '\n'
    output_txt.write(convert_line)

