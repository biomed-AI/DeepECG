import pandas as pd
import numpy as np
import argparse

def return_int_list(intput_list):
    output_list = []
    for a in intput_list:
        #a = a.split('\n')[0] 
        if a!='NA':
            output_list.append(int(a))
        else:
            output_list.append(0)
    return output_list

def raw2npy(rawdata_path, geno_path, FID_path):
    genotype_data = []
    n=0
    with open(FID_path, 'w+') as file:
        for line in open(rawdata_path):
            line = line.split('\n')[0]
            FID = line.split(' ')[0]
            file.write(FID+'\n')
            if n!=0:
                genotype_data.append(return_int_list(line.split(' ')[6:]))
            n+=1
            # if n%(int(max_n/100))==0:
            #     print('\r',int(n/(int(max_n/100))), end='', flush=True)
    np.save(geno_path, np.array(genotype_data))

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument("--rawdata", type=str, default = "./data/V1_inteT.raw")
    parse.add_argument("--geno_out", type=str, default = "./data/V1_inteT.npy")
    parse.add_argument("--FID_out", type=str, default = "./data/V1_inteT.FID")
    args = parse.parse_args()
    raw2npy(args.rawdata, args.geno_out, args.FID_out)
