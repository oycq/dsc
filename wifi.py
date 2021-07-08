import socket
import struct
import time 
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
        if len(content) == 73:
            angles_temp = []
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

while(1):
    print(angles)
    time.sleep(0.05)

client.close()
s.close()

