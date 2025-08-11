# MSRENet: A Generalized Residual Encoder nnU-Net for Robust Multiple Sclerosis Lesion Segmentation

This repository contains the official implementation for the paper "MSRENet: A Generalized Residual Encoder nnU-Net for Robust Multiple Sclerosis Lesion Segmentation Across Diverse MRI Datasets".

## Abstract

Accurate segmentation of multiple sclerosis (MS) lesions in MRI is essential for reliable diagnosis and effective disease monitoring; however, it remains a challenging task due to lesion heterogeneity and variability in imaging protocols. In this study, MSRENet, a 3D deep learning framework based on the nnU-Net architecture, is proposed for automated MS lesion segmentation. The model employs residual connections within the encoder to improve feature representation and generalization. It utilizes multimodal MRI inputs, including FLAIR, T1-weighted, and T2-weighted sequences, and uses a hybrid loss function combining Dice and cross-entropy terms to address class imbalance. A standardized preprocessing pipeline is also applied to ensure consistency across inputs. MSRENet achieves state-of-the-art performance on benchmark datasets, demonstrating its robustness and potential for clinical application.

## Collaboration with PaxeraHealth

This research is a collaboration with **PaxeraHealth**, aiming to bridge the gap between academic research and real-world clinical applications. The MSRENet model is designed to be deployed within the **ARK platform**, an AI-powered medical imaging solution.

The model can be used as a ready-to-use tool inside ARK, which provides a seamless environment with all necessary libraries and dependencies pre-installed.

[![PaxeraHealth ARK Platform](https://i.ytimg.com/vi/EvmUMBrUVJE/maxresdefault.jpg )](https://www.youtube.com/watch?v=EvmUMBrUVJE "PaxeraHealth ARK Platform" )

*Click the image above to watch a video about the ARK platform.*

## Repository Structure

```
MSRENet/
│
├── data/
├── notebooks/
├── src/
│   ├── preprocess.py
│   ├── train.py
│   └── model.py
│
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

The code is designed to run within the **PaxeraHealth ARK platform**, where all dependencies are pre-installed. No manual installation of libraries is required when using ARK.

For local development, you will need Python 3.8+ and the following libraries:
- PyTorch
- SimpleITK
- NumPy
- and other standard scientific computing libraries.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/MSRENet.git
    cd MSRENet
    ```

2.  **Download the data:**
    The datasets used are publicly available:
    -   **MSSEG2016:** [https://portal.fli-iam.irisa.fr/msseg-challenge/](https://portal.fli-iam.irisa.fr/msseg-challenge/ )
    -   **ISBI2015:** [https://smart-stats-tools.org/](https://smart-stats-tools.org/ )

    Please download the datasets and place them in the `data/` directory.

### Usage

#### 1. Data Preprocessing

The preprocessing pipeline standardizes the input MRI data. It includes the following steps:
1.  **Denoising:** Reduces noise while preserving anatomical structures.
2.  **Rigid Registration:** Aligns all MRI sequences to the FLAIR image.
3.  **Skull Stripping:** Removes non-brain tissue.
4.  **Bias Field Correction:** Corrects for intensity inhomogeneities.

To run the preprocessing script:
```bash
python src/preprocess.py
```
*Note: You will need to modify the script to point to your data directories.*

#### 2. Model Training

To train the MSRENet model, run the training script:
```bash
python src/train.py
```

## Using the Model in ARK

The MSRENet model can be seamlessly integrated and used within the PaxeraHealth ARK platform. Here are the steps illustrated with screenshots:

1.  **Step 1: Upload the Model**
    *(Screenshot showing the model upload interface in ARK)*

2.  **Step 2: Select the Model for an Imaging Study**
    *(Screenshot of selecting the MSRENet model from a dropdown menu in ARK)*

3.  **Step 3: Run the Segmentation**
    *(Screenshot of the ARK interface running the model on an MRI scan)*

4.  **Step 4: Visualize the Results**
    *(Screenshot showing the segmentation overlay on the original MRI within the ARK viewer)*

## Citation

If you use this code or model in your research, please cite our paper:

```bibtex
@article{Nabil2025MSRENet,
  title={MSRENet: A Generalized Residual Encoder nnUNet for Robust Multiple Sclerosis Lesion Segmentation Across Diverse MRI Datasets},
  author={Essam Nabil and Nourhan S. Salem and Eman A. Tafweek and Ghada M. El-Banby},
  journal={Neuroinformatics},
  year={2025}
}
```
