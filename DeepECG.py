import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.functional import *


class DeepECG(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        neural_num = 200
        d_prob = 0.1
        self.linears = nn.Sequential(
            nn.Linear(input_dim, 200),
            nn.ReLU(inplace=True),
            nn.Dropout(d_prob),
            nn.Linear(200, 200),
            nn.ReLU(inplace=True),
            nn.Dropout(d_prob),
            nn.Linear(200, 100),
            nn.ReLU(inplace=True),
            #nn.Dropout(d_prob),
            nn.Linear(100, 1),
        )
        self.linears2 = nn.Sequential(
            nn.Linear(50, 100),#63175
            nn.ReLU(inplace=True),
            nn.Dropout(d_prob),
            nn.Linear(100, 50),
            nn.ReLU(inplace=True),
            #nn.Dropout(d_prob),
            nn.Linear(50, 10),
            nn.ReLU(inplace=True),
            nn.Linear(10, 1)
        )
    def forward(self,x):
        x1 = self.linears(x)
        return x1

class DeepECG_addcov2(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        d_prob = 0.1
        self.linears1 = nn.Sequential(
            nn.Linear(input_dim, 500),#63175 89222
            nn.ReLU(inplace=True),
            nn.Dropout(d_prob),
            nn.Linear(500, 200),
            nn.ReLU(inplace=True),
            nn.Dropout(d_prob),
            nn.Linear(200, 100),
            nn.ReLU(inplace=True),
            nn.Linear(100, 50),
            #nn.ReLU(inplace=True),
            #nn.Dropout(d_prob),
            #nn.Linear(100, 1),
        )
        self.linears2 = nn.Sequential(
            nn.Linear(52, 20),
            nn.ReLU(inplace=True),
            #nn.Dropout(d_prob),
            nn.Linear(20, 10),
            nn.ReLU(inplace=True),
            nn.Linear(10, 1)
        )
        self.linears3 = nn.Sequential(
            nn.Linear(2, 10),
            nn.ReLU(inplace=True),
            #nn.Dropout(d_prob),
            nn.Linear(10, 10),
            nn.ReLU(inplace=True),
            nn.Linear(10, 1)
        )
        self.linears4 = nn.Sequential(
            nn.Linear(2, 10),#63175
            nn.ReLU(inplace=True),
            #nn.Dropout(d_prob),
            nn.Linear(10, 10),
            nn.ReLU(inplace=True),
            nn.Linear(10, 1)
        )

        self.linear1 = nn.Linear(10, 1)
        self.linear2 = nn.Linear(10, 1)
        self.linear3 = nn.Linear(20, 1)

    def forward(self,snp_x, cov2_x):
        #x1 = self.linears1(snp_x)
        #y1 = self.linear1(x1)

        # x2 = torch.cat([x1, cov2_x], dim=1) 
        # y3 = self.linears2(x2)
        # x2 = self.linears2(cov2_x)
        # y2 = self.linear2(x2)
        # x3 = torch.cat([x1, x2], dim=1) 
        # y3 = self.linear3(x3)
        y1 = self.linears1(snp_x)
        #y3 = self.linears3(cov2_x)
        x2 = torch.cat([y1, cov2_x], dim=1) 
        y4 = self.linears2(x2)
        return y4

class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Conv1d(1, 16, kernel_size=3, stride=3),
            nn.Conv1d(16, 16, kernel_size=3),
            nn.BatchNorm1d(16),
            nn.ReLU(inplace=True),
            nn.Conv1d(16, 64, kernel_size=3, stride=3),
            nn.Conv1d(64, 64, kernel_size=3),
            nn.BatchNorm1d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool1d(3),
            nn.Flatten(),

            nn.Linear(211392, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(inplace=True),
            nn.Dropout(0.2),

            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(inplace=True),
            nn.Dropout(0.2),
            nn.Linear(64, 1)
            # nn.Dropout(0.2),
            # nn.MaxPool1d(3),
            # nn.Flatten(),
            # nn.Linear(158592, 64),
            # nn.ReLU(inplace=True),
            # nn.Linear(64, 32),
            # nn.ReLU(inplace=True),
            # nn.Linear(32, 1)

        )

    def forward(self,x):
        x1 = self.layers(x)
        return x1


