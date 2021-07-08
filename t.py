import torch
import torch.nn as nn
import torch.optim as optim
from dataset import trainloader, testloader
from torch.utils.data import Dataset
import numpy as np
import sys
import datetime
import tqdm


IF_WANDB = 0
SAVE = 1
ID_LEN = 18416
EMBEDDING_VECTOR_SIZE = 7
SAVE_NAME = 'v1'

if IF_WANDB:
    import wandb
    wandb.init(project = 'dsc')#, name = '.')


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

net = Net().cuda()
#embedding = nn.Embedding(ID_LEN, EMBEDDING_VECTOR_SIZE, max_norm=True)
embedding = torch.randn((ID_LEN, EMBEDDING_VECTOR_SIZE)).cuda().requires_grad_()

optimizer_net = optim.Adam(net.parameters())
optimizer_embeding = optim.Adam([embedding])
for epoch in range(1000000):
    print(epoch)
    for i, data in enumerate(trainloader, 0):
        ids, dates, values = data[0].cuda(), data[1].cuda(), data[2].cuda()
        emb = embedding[ids]
        inputs = torch.cat((dates.unsqueeze(-1), emb), 1)
        predict = net(inputs)
        loss = (predict.squeeze(-1) - values).abs()
        loss = ((loss / (values+0.000001)))
        acc = (loss < 0.2).float().mean() * 100
        loss = loss.mean()
        optimizer_net.zero_grad()
        optimizer_embeding.zero_grad()
        loss.backward()
        optimizer_net.step()
        optimizer_embeding.step()
        if i % 300 == 0:
            print('%6d  %12.4f   %6.2%%f'%(i,loss,acc))
            if IF_WANDB:
                wandb.log({'acc':acc,'loss':loss})


    if epoch % 2 == 0:
        for i, data in enumerate(testloader, 0):
            ids, dates, values = data[0].cuda(), data[1].cuda(), data[2].cuda()
            emb = embedding[ids]
            inputs = torch.cat((dates.unsqueeze(-1), emb), 1)
            predict = net(inputs)
            loss = (predict.squeeze(-1) - values).abs()
            loss = ((loss / (values+0.00001)))
            acc = (loss < 0.2).float().mean() * 100
            loss = loss.mean()
            print('test    %6d  %12.4f   %6.2%%f'%(i,loss,acc))
            if i == 4:
                break
        if SAVE:
            torch.save(net.state_dict(), SAVE_NAME+'.model')
            torch.save(embedding, SAVE_NAME+'.emb')

    



