import torch
from torch.utils.data import Dataset
import numpy as np
import sys
import datetime
import tqdm

BATCH_SIZE = 3000
NUM_WORKERS = 8
ID_LEN = 18416
DATE_LEN = 810 #684
WRITE_IDS_DICT_TO_TXT = False
TRAIN_TEST_RATIO = 0.95 * 0.8444
date_0 = datetime.date(2017, 2, 1)
train_data = open('./train_step1.csv').readlines()[1:]
test_data = open('./test_step1.csv').readlines()[1:]
train_data_len = len(train_data)
train_id = np.zeros(train_data_len)
train_date = np.zeros(train_data_len)
train_value  = np.zeros(train_data_len)

identity_list = []
last_identity = 0

for i in tqdm.tqdm(range(train_data_len), total=train_data_len):
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
    train_id[i] = identity
    train_date[i] = date_delta * 1.0 / DATE_LEN
    train_value[i] = value

class MyDataset(Dataset):
    def __init__(self, test=False):
        ids = torch.from_numpy(train_id).long()
        dates = torch.from_numpy(train_date).float()
        values = torch.from_numpy(train_value).float()
        if test:
            select = dates > TRAIN_TEST_RATIO
        else:
            select = dates <= TRAIN_TEST_RATIO
        self.ids = ids[select]
        self.dates = dates[select]
        self.values = values[select]

    def __len__(self):
        return self.ids.shape[0]

    def __getitem__(self, idx):
        return self.ids[idx], self.dates[idx], self.values[idx]

trainloader = torch.utils.data.DataLoader(MyDataset(test = False), BATCH_SIZE,\
    shuffle = True, num_workers= NUM_WORKERS, drop_last =  True) 

testloader  = torch.utils.data.DataLoader(MyDataset(test = True), BATCH_SIZE,\
    shuffle = True, num_workers= NUM_WORKERS, drop_last =  True) 

if WRITE_IDS_DICT_TO_TXT:
    ids_txt = open('./id.txt','w+')
    for identity in identity_list:
        ids_txt.write('%d'%(identity))
