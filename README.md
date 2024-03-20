# DeepECG
Empowering genome-wide association study by imputing electrocardiograms from genotype in UK-biobank 
## Pre-requisites:
+ NVIDIA GPU (Nvidia GeForce RTX 2080 Ti) with CUDA 11.6
+ pytorch(1.8.1), torchvision(0.9.1), numpy(1.19.2), pandas(1.1.5), matplotlib(3.3.4), scipy(1.5.4), tqdm(4.62.3)
## Usage 
### 1. Generating encoded SNPs for ECG traits prediction
```
python ./code/MSegNet_seg.py --batch_size 32 --ckpt_L1 ./model/L1_model.pth --ckpt_L2 ./model/L2_model.pth --slide_dir ./data/slide --data_dir ./data/intermediate_data --seg_results_dir ./data/seg_result
```
### 2. ...
```
python ./code/get_features.py --slide_dir ./data/slide --data_dir ./data/intermediate_data --seg_results_dir ./data/seg_result --save_csv_path ./data/image_results.csv
```
