import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset
import numpy as np
import sys
import datetime
import tqdm

NAME = 'v1'
ID_LEN = 18416
EMBEDDING_VECTOR_SIZE = 7
DATE_LEN = 810 #684
date_0 = datetime.date(2017, 2, 1)


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        hid = 256
        self.s = torch.nn.Sequential( 
            nn.Linear(EMBEDDING_VECTOR_SIZE + 1, hid),
            nn.BatchNorm1d(hid),
            nn.ReLU(inplace = True),
            nn.Linear(hid, hid),
            nn.BatchNorm1d(hid),
            nn.ReLU(inplace = True),
            nn.Linear(hid, hid),
            nn.BatchNorm1d(hid),
            nn.ReLU(inplace = True),
            nn.Linear(hid, 1),
            )

    def forward(self, inputs):
        return self.s(inputs)

net = Net().eval().cuda()
net.load_state_dict(torch.load(NAME+'.model'))
embedding = torch.load(NAME+'.emb')
id_txt = open('./id.txt')
id_table = []
for line in id_txt.readlines():
    id_table.append(int(line[:-1]))

input_txt = open('./test_step1.csv')
input_lines = input_txt.readlines()[:]
output_txt = open('./result_step1.txt','w+')

inputs = torch.zeros((len(input_lines), EMBEDDING_VECTOR_SIZE + 1))
outputs = torch.zeros((len(input_lines), 1)).cuda()

for i, line in tqdm.tqdm(enumerate(input_lines), total=len(input_lines)):
    if line[:2]=='id':
        continue
    line = line[:-1]
    identity, date_str = line.split(',')
    day, monty, year = date_str[-2:], date_str[5:7], date_str[:4]
    date = datetime.date(int(year), int(monty), int(day))
    date_delta = (date - date_0).days

    ids = id_table.index(int(identity))
    emb = embedding[ids]
    inputs[i][0] = date_delta * 1.0 / DATE_LEN
    inputs[i][1:] = emb

i = 0
with torch.no_grad():
    while(1):
        if i*1000 >= inputs.shape[0]:
            break
        a = inputs[i*1000 : i * 1000 + 1000].cuda()
        b = net(a)
        outputs[i*1000 : i * 1000 + 1000] = net(a)
        i = i + 1

for i, line in tqdm.tqdm(enumerate(input_lines), total=len(input_lines)):
    if line[:2]=='id':
        output_txt.write(line)
        continue
    value = outputs[i].item()
    if value < 0:
        value = 0
    output_line = line.split('\n')[0] + ',%f\n'%value
    output_txt.write(output_line)
output_txt.close()
input_txt.close()
