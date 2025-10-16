# Merlin: Vision Language Foundation Model for 3D Computed Tomography

[![arXiv](https://img.shields.io/badge/arXiv-2406.06512-b31b1b.svg?style=for-the-badge)](https://arxiv.org/abs/2406.06512)    [![Hugging Face](https://huggingface.co/datasets/huggingface/badges/resolve/main/model-on-hf-md.svg)](https://huggingface.co/stanfordmimi/Merlin)    [![pypi](https://img.shields.io/pypi/v/merlin-vlm?style=for-the-badge)](https://pypi.org/project/merlin-vlm/)    ![Static Badge](https://img.shields.io/badge/Merlin%20Dataset-blue?style=for-the-badge&link=https%3A%2F%2Fstanfordaimi.azurewebsites.net%2Fdatasets%2F60b9c7ff-877b-48ce-96c3-0194c8205c40)    [![Watch the Talk on YouTube](https://img.shields.io/badge/YouTube-Talk-red?style=for-the-badge&logo=youtube)](https://youtu.be/XWmCkbpXOUw?si=6GggZgj9U4kbLAKx)    ![License](https://img.shields.io/github/license/stanfordmimi/merlin?style=for-the-badge)

*Merlin is a 3D VLM for computed tomography that leverages both structured electronic health records (EHR) and unstructured radiology reports for pretraining.*

![Key Graphic](documentation/assets/overview.png)

## ⚡️ Installation

To install Merlin, you can simply run:

```bash
pip install merlin-vlm
```

For an editable installation, use the following commands to clone and install this repository.

```bash
conda create --name merlin python==3.10
conda activate merlin

git clone https://github.com/StanfordMIMI/Merlin.git
cd Merlin
pip install -e .

# Alternatively, to install exact package versions as tested:
# uv sync
```

## 🚀 Inference with Merlin

To create a Merlin model with both image and text embeddings enabled, use the following:

```python
from merlin import Merlin

model = Merlin()
```

To initialize the model with **only image embeddings** active, use:

```python
from merlin import Merlin

model = Merlin(ImageEmbedding=True)
```

To initialize the model for **phenotype classification**, use:

```python
from merlin import Merlin

model = Merlin(PhenotypeCls=True)
```

To initialize the model for **five-year disease prediction**, use:

```python
from merlin import Merlin

model = Merlin(FiveYearPred=True)
```

To initialize the model for **radiology report generation**, use:

```python
from merlin import Merlin

model = Merlin(RadiologyReport=True)
```

#### For inference on a demo CT scan, please check out the [general demo](documentation/demo.py) and [report generation demo](documentation/radiology_report_generation.py).

#### For additional information, please read the [inference documentation](documentation/inference.md) and [report generation documentation](documentation/report_generation.md).

## 📂  Merlin Abdominal CT Dataset

We are excited to release the **Merlin Abdominal CT Dataset** to the community!

For details on accessing and using the dataset, please see the [download documentation](documentation/download.md)!

## 📎 Citation

If you find this repository useful for your work, please cite the cite the [original paper](https://arxiv.org/abs/2406.06512):

```bibtex
@article{blankemeier2024merlin,
  title={Merlin: A vision language foundation model for 3d computed tomography},
  author={Blankemeier, Louis and Cohen, Joseph Paul and Kumar, Ashwin and Van Veen, Dave and Gardezi, Syed Jamal Safdar and Paschali, Magdalini and Chen, Zhihong and Delbrouck, Jean-Benoit and Reis, Eduardo and Truyts, Cesar and others},
  journal={Research Square},
  pages={rs--3},
  year={2024}
}
```
