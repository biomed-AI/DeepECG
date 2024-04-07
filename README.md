![](figures/Pipeline.png)

# DeepECG: Empowering genome-wide association study by imputing electrocardiograms from genotype in UK-biobank 
DeepECG is a densely connected network for ECG traits prediction using genotype data. The predicted ECG traits from DeepECG can be used to predict cardiovascular diseases (CVDs) risk and perform GWAS analysis.

## Installation

To reproduce **DeepECG**, we suggest first create a conda environment by:

~~~shell
conda create -n DeepECG python=3.8
conda activate DeepECG
~~~

and then run the following code to install the required package:

~~~shell
pip install -r requirements.txt
~~~
### Requirements
- `pytorch(1.8.1)`
- `torchvision(0.9.1)`
- `matplotlib(3.3.4)`
- `pandas(1.1.5)`
- `tqdm(4.62.3)`
- `numpy(1.19.2)`
- `scikit-learn(1.0.2)`
- `scipy(1.6.2)`

PLINK (v1.90) can be downloaded from  https://www.cog-genomics.org/plink/ .

## 1. Data preprocessing

In order to run **DeepECG** , we need to first create genotype data as a binary file from bfile data.

### 1.1 Extracting SNPs from bfile and encode SNP as (0/1/2)

![](figures/Step1.1.png)

Use PLINK (v1.90) to extract specific SNPs from the genotype data stored in bfile format.These SNPs are encoded as sample-major additive **(0/1/2)**. Here,“0” refers to homozygous for the reference allele, “1” refers to heterozygous for the alternative allele, and “2” refers to the homozygous for the alternative allele. The results will be saved in "rawdata_path". 

```
cd DeepECG
plink --bfile mydata \ # input data (plink bfile)
	  --extract ./data/SNP_list/SNP_path \ #input data (SNPs used for ECG prediction)
	  --export A \
	  --out ./data/npy_data/rawdata_path #output
```
By running the above code, the output file will be stored in one specific path:
- `./data/npy_data/rawdata_path`: storing the specific SNPs encoded as 0/1/2

The example raw data can be downloaded from https://zenodo.org/uploads/10935155

### 1.2 Convert raw data into binary file in .npy format

![](figures/Step1.2.png)

The genotype data pre-processed by PLINK will be converted into an array, a binary file in “.npy” format by  numpy(1.19.2).

```
python ./preprocess.py --rawdata ./data/npy_data/rawdata_path \ #input data (geneotype raw data)
	      --geno_out ./data/npy_data/npy_path \ #output (genotype data in .npy format)
              --FID_out ./data/npy_data/FID_path #output (human ID)
```
By running the above command, two files will be generated under specific path: 
- `./data/npy_data/npy_path`: a binary file storing the genotype data in .npy format
- `./data/npy_data/FID_path`: a table file storing the human ID

## 2. Predicting ECG traits by DeepECG

![](figures/Step2.png)

The processed genotype data are used as input to DeepECG and output a table (column name: FID, predicted_trait) in .csv format

```
python main.py  --ECG_trait feature \ # indicated ECG trait for prediction
                --geno_path  ./data/npy_data/npy_path \ # input genotype data
                --FID_path  ./data/npy_dataFID_path \ # input human ID
                --out ./data/predicted_ECG_traits/feature.csv  # output ECG trait
```
Running the above command will generate one output file in the output path:
- `./data/predicted_ECG_traits/feature.csv`: a table file storing the predicted ECG trait

## 3. Applications of DeepECG in CVDs prediction and GWAS

### 3.1 Use ECG traits to predict cardiovascular disease

![](figures/Step3.1.png)

The output file of “main.py” is input into cvd_pred.py by running the code:
```
python CVD_predict.py  --CVD_name CVD \ # indicated cardiovascular disease for prediction
                --ECG_trait_path  ./data/predicted_ECG_traits/feature.csv \ # input ECG traits
                --out ./data/CVD_risk.csv  # output (predicted CVD risk)
```
Running the above command will generate one output file in the output path:
- `./data/predicted_ECG_traits/feature.csv`: a table file storing the predicted CVD risk. The first column is human ID, the second column is predicted ECG trait.

### 3.2 Use ECG traits to perform GWAS analysis

![](figures/Step3.2.png)

When DeepECG has been used in a large population for predicting ECG traits from genotype, the predicted ECG traits can be used in GWAS. The code of BOLT-LMM (v2.3.5) for GWAS analysis can be downloaded from https://alkesgroup.broadinstitute.org/BOLT-LMM/BOLT-LMM_manual.html, and BOLT-LMM can be run by the code:

```
./BOLT-LMM_v2.3.5/bolt --bfile=$file_bfile \ # input genotype data
--LDscoresFile=$file_ld \ # input SNP LD data
--lmm \
--phenoFile=$file_pheno \ # input ECG trait data
--phenoCol=$trait \ # input ECG trait
--modelSnps=$file_modsnp \ # input SNP list
--numThreads=$nthread \
--statsFile=$file_out # output GWAS
```

## Citation

If you find our codes useful, please consider citing our work:

~~~bibtex


@article{
  title={Empowering genome-wide association study by imputing electrocardiograms from genotype in UK-biobank},
  author={Siying Lin, Mengling Qi, Yuedong Yang, Huiying Zhao*},
  journal={},
  year={2024},
}
~~~
