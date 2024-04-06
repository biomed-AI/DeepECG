import numpy as np
import pandas as pd
import os
import torch
from torch.utils.data import Dataset
from sklearn import datasets
from sklearn import preprocessing
import random

class SNP_ECG_dataset():
    def __init__(self, data_path, label_path, feature_name):
        self.X_data = np.load(data_path)#[:,[2406, 61595, 856, 62075, 38259, 23645, 53421, 31554, 1889]]
        label_df = pd.read_csv(label_path, sep=',')
        label_df = label_df.sort_values(by='FID')
        label_df['a'] = range(len(label_df))
        label_df = label_df.set_index('a').astype('float32')
        label_df2 = label_df.loc[:,feature_name]
        self.y_data=label_df2.values

        self.sex = label_df.loc[:,'sex'].values.reshape(-1,1)
        self.age = label_df.loc[:,'age'].values.reshape(-1,1)
        self.cov2 = np.concatenate([self.sex, self.age],1)
        #self.y_data = (self.y_data-np.mean(self.y_data))/np.std(self.y_data)
        self.len = self.y_data.shape[0]

    def __getitem__(self, index):
        return self.X_data[index], self.y_data[index], self.cov2[index]

    def __len__(self):
        return self.len

class SNP_ECG_dataset2():
    def __init__(self, data_path, FID_path):
        self.X_data = np.load(data_path)#[:,[2406, 61595, 856, 62075, 38259, 23645, 53421, 31554, 1889]]
        self.FID_list = pd.read_csv(FID_path)['FID'].tolist()
        self.len = len(self.FID_list)

    def __getitem__(self, index):
        return self.X_data[index], self.FID_list[index]

    def __len__(self):
        return self.len



