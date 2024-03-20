# DeepECG: Empowering genome-wide association study by imputing electrocardiograms from genotype in UK-biobank 
DeepECG is a densely connected network that can be used to predicted ECG traits from genotype.
## Pre-requisites:
+ NVIDIA GPU (Nvidia GeForce RTX 2080 Ti) with CUDA 11.6
+ pytorch(1.8.1), torchvision(0.9.1), numpy(1.19.2), pandas(1.1.5), matplotlib(3.3.4), scipy(1.5.4), tqdm(4.62.3)
## Usage 
### 1 Generating encoded SNPs for ECG traits prediction
**1.1 Extracting SNPs from bfile and encode SNP as (0/1/2)**
Use PLINK (v1.90) to extract specific SNPs from the genetic data stored in the "mydata" files and encode the SNPs as sample-major additive (0/1/2). “0” refers to homozygous for the reference allele, “1” refers to heterozygous for the alternative allele, and “2” refers to the homozygous for the alternative allele.The results will be saved in "rawdata_path".
```
plink --bfile mydata --extract SNP_path ---export A --out rawdata_path
```
**1.2 Converting rawdata into array**
Use numpy(1.19.2) to covert the rawdata into array as a binary file in .npy format
```
python ./preprocess.py --rawdata rawdata_path --out npy_path
```
### 2 Using DeepECG to predict ECG traits from genotype data
```
python ./preprocess.py --rawdata rawdata_path --out npy_path
```
