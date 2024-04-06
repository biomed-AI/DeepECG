import math
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from tqdm import tqdm
from scipy.stats import pearsonr,spearmanr
from torch import optim
from utils.Dataloader import SNP_ECG_dataset, SNP_ECG_dataset2
from DeepECG import DeepECG, DeepECG_addcov2
from collections import Counter
from sklearn.metrics import r2_score
import os
import argparse
from sklearn.model_selection import KFold

def get_predicted_ECG_trait(ECG_trait, geno_path, FID_path, save_path):

    input_dim = np.load(geno_path).shape[1]
    device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = DeepECG(input_dim).to(device=device)
    model_weigth = os.path.join('./models', ECG_trait, ECG_trait+'.pt')
    model.load_state_dict(torch.load(model_weigth))
    model.eval()

    dataset = SNP_ECG_dataset2(geno_path, FID_path)
    dataloader = torch.utils.data.DataLoader(dataset=dataset, batch_size=128, num_workers=20)

    for step,(batch_x,batch_fid) in enumerate(tqdm(dataloader)):
        batch_x = batch_x.type(torch.FloatTensor).to(device)
        batch_fid = batch_fid.reshape(-1,1)
        pred_y = model(batch_x).cpu().detach().numpy()
        batch_fid = batch_fid.cpu().detach().numpy()
        if step==0:
            pred_y_all = pred_y
            fid_all = batch_fid
        else:
            pred_y_all = np.concatenate((pred_y_all, pred_y))
            fid_all = np.concatenate((fid_all, batch_fid))

    ECG_traits_df = pd.DataFrame(columns=['FID', ECG_trait])
    ECG_traits_df['FID'] = fid_all.reshape(-1)
    ECG_traits_df[ECG_trait] = pred_y_all.reshape(-1)
    ECG_traits_df.to_csv(save_path, index=False)

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument("--ECG_trait", type=str, default = "V1_inteT")
    parse.add_argument("--geno_path", type=str, default = "./data/V1_inteT.npy")
    parse.add_argument("--FID_path", type=str, default = "./data/V1_inteT.FID")
    parse.add_argument("--out", type=str, default = "./data/predicted_ECG_traits/V1_inteT.csv")
    args = parse.parse_args()
    get_predicted_ECG_trait(args.ECG_trait, args.geno_path, args.FID_path, args.out)