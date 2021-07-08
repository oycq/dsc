import torch
from torch.utils.data import Dataset
import numpy as np
import sys
import datetime
import tqdm
import matplotlib.pyplot as plt

DATE_LEN = 810 #684
date_0 = datetime.date(2017, 2, 1)
train_data = open('./train_step1.csv').readlines()[1:]
train_data_len = len(train_data)

identity_list = []
last_identity = 0
data = np.zeros((18416, DATE_LEN))


for i in tqdm.tqdm(range(train_data_len), total=train_data_len):
#for i in range(train_data_len):
    identity, date_str, value = train_data[i][:-1].split(',')
    day, monty, year = date_str[-2:], date_str[5:7], date_str[:4]
    date = datetime.date(int(year), int(monty), int(day))
    date_delta = (date - date_0).days
    identity = int(identity)
    if identity != last_identity:
        last_identity = identity
        identity_list.append(identity)
    identity = len(identity_list) - 1
    value = float(value)
    data[identity, date_delta] = value

data = torch.from_numpy(data)
#b = data[:,680:685].mean(-1)
b = data[:,684]

input_txt = open('./test_step1.csv')
input_lines = input_txt.readlines()[:]
output_txt = open('./result_step1.txt','w+')

last_identity = 0
last_ids = -99
for i, line in tqdm.tqdm(enumerate(input_lines), total=len(input_lines)):
    if line[:2]=='id':
        output_txt.write(line)
        continue
    line = line[:-1]
    identity, date_str = line.split(',')
    identity = int(identity)
    if identity == last_identity:
        ids = last_ids
    else:
        last_identity = identity
        last_ids = identity_list.index(identity)
        ids = last_ids
    value = b[ids]
    output_line = line.split('\n')[0] + ',%f\n'%value
    output_txt.write(output_line)
output_txt.close()
input_txt.close()
#c = data[:,670:685].mean()
#for i in range(10000):
#    plt.figure(figsize=(30, 16))
#    plt.scatter(range(DATE_LEN),data[i])
#    plt.show()
