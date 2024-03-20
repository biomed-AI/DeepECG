# DeepECG: Empowering genome-wide association study by imputing electrocardiograms from genotype in UK-biobank 
DeepECG is a densely connected network that can be used to predicted ECG traits from genotype.

**Table of Contents**

* [Installation](#Installation)
* [Usage](#Usage)
* [Citation](#Citation)

## Installation

To reproduce **SANGO**, we suggest first create a conda environment by:

~~~shell
conda create -n DeepECG python=3.8
conda activate DeepECG
~~~

and then run the following code to install the required package:

~~~shell
pip install -r requirements.txt
~~~
## Requirements
- `pytorch`
- `torchvision`
- `opencv-python`
- `imgaug`
- `matplotlib`
- `scikit-learn`
- `scikit-image`
- `pydensecrf`
- `pandas`
- `tqdm`
- `numpy`
- `PIL`
- `collections`

## Usage 
### 1 Data preprocessing

In order to run **DeepECG** , we need to first create genotype data as a binary file from bfile data.

**1.1 Extracting SNPs from bfile and encode SNP as (0/1/2)**

Use PLINK (v1.90) to extract specific SNPs from the genetic data stored in the "mydata" files and encode the SNPs as sample-major additive (0/1/2). “0” refers to homozygous for the reference allele, “1” refers to heterozygous for the alternative allele, and “2” refers to the homozygous for the alternative allele. The results will be saved in "rawdata_path".

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
python main.py  --data_dir ../../output/reference_query_example/CACNN_output.h5ad \ # input data
                --train_name_list reference --test_name query \
                --save_path ../../output \
                --save_name reference_query_example
```

## Citation

If you find our codes useful, please consider citing our work:

~~~bibtex


@article{zengSANGO,
  title={Deciphering Cell Types by Integrating scATAC-seq Data with Genome Sequences},
  author={Yuansong Zeng, Mai Luo, Ningyuan Shangguan, Peiyu Shi, Junxi Feng, Jin Xu, Weijiang Yu, and Yuedong Yang},
  journal={},
  year={2023},
}
~~~
