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


id_txt = open('./id.txt')
id_table = []
value_table = []
for line in id_txt.readlines():
    a,b = line[:-1].split(',')
    id_table.append(int(a))
    value_table.append(float(b))

input_txt = open('./test_step1.csv')
input_lines = input_txt.readlines()[:]
output_txt = open('./result_step1.txt','w+')

for i, line in tqdm.tqdm(enumerate(input_lines), total=len(input_lines)):
    if line[:2]=='id':
        output_txt.write(line)
        continue
    line = line[:-1]
    identity, date_str = line.split(',')
    ids = id_table.index(int(identity))
    value = value_table[ids]
    output_line = line.split('\n')[0] + ',%f\n'%value
    output_txt.write(output_line)
output_txt.close()
input_txt.close()
