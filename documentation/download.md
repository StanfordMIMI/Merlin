# Merlin Abdominal CT Dataset

We are excited to announce that along with the **Merlin paper**, we are also releasing the **Merlin Abdominal CT Dataset** to the community, a large-scale medical imaging resource developed at Stanford University!  🚀  

---

## 📊 Dataset Overview

The **Merlin Abdominal CT Dataset** is a large-scale abdominal CT dataset curated from the Stanford Hospital Emergency Department between **2012–2018**. It contains:

- **25,494 scans**  
- **18,317 unique patients**  
- Each scan paired with its **radiology report**  

Exams are **abdominal and pelvis CT** scans, identified using CPT codes: 72192, 72193, 72194, 74150, 74160, 74170, 74176, 74177, 74178. Selected via the **STARR tool** (Stanford Medicine Research Data Repository).  

For each exam, the DICOM series with the largest slice count was retained. Converted to NIfTI format for ease of use. Scans were compressed and de-identified by removing all patient-identifiable metadata.  

---
## 🔗 Accessing the Dataset

The Merlin Abdominal CT dataset is hosted by the **Stanford AIMI Center**. To gain access, you must complete a data-use agreement form on the dataset's download page. Upon approval, you will receive a secure Azure Blob Storage URL to download the files.

👉 [Merlin Abdominal CT Dataset Download Page](https://stanfordaimi.azurewebsites.net/datasets/60b9c7ff-877b-48ce-96c3-0194c8205c40)

#### Download Instructions
1.  **Install AzCopy:** First, download the AzCopy command-line utility, which is required for accessing the dataset from Azure.
    * [AzCopy Download and Installation Guide](https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10)
2.  **Run the Download Command:** Open your terminal and run the following command, replacing `YOUR_BLOB_URL_HERE` with the unique URL you received.
    ```bash
    azcopy cp --recursive "YOUR_BLOB_URL_HERE" .
    ```

---
## 📂 Dataset Structure

The downloaded directory, `merlinabdominalctdataset/`, contains the following files and folders:

* **`merlin_data/`**
    * This directory holds the complete collection of 25,494 abdominal CT scans in NIfTI (`.nii`) format.

* **`reports_final.xlsx`**
    * An Excel spreadsheet that links to the CT scans and includes:
        * The full text from the "Findings" section of the corresponding radiology report.
        * The designated dataset split (train, validation, or test) for each scan.
        * A flag to identify scans that were part of the few-shot experiments.

* **`zero_shot_findings_disease_cls.csv`**
    * A CSV file containing the results of a zero-shot disease classification task performed on the report findings. The labels are encoded as follows:
        * **`1`** (Positive): The disease or finding was mentioned.
        * **`0`** (Negative): The disease or finding was explicitly negated.
        * **`-1`** (Missing): The disease or finding was not mentioned.
- **`five_years_disease_task.csv`**  
CSV file containing **multi-disease 5-year prediction labels** for the **test set**.

## ⚠️ Notes

- Please ensure compliance with Stanford’s **data use agreements** when accessing and working with the dataset.  
- Permission is granted to view and use the Merlin Abdominal CT Dataset Dataset without charge for personal, non-commercial research purposes only. 
- If interested in commercial use of the Merlin dataset, please see the [Stanford AIMI Commerical Use Page](https://aimi.stanford.edu/datasets-commercial-use).

## 🔗 Citation

If you use the Merlin Dataset in your research, please cite:

```bibtex
@article{blankemeier2024merlin,
  title={Merlin: A vision language foundation model for 3d computed tomography},
  author={Blankemeier, Louis and Cohen, Joseph Paul and Kumar, Ashwin and Van Veen, Dave and Gardezi, Syed Jamal Safdar and Paschali, Magdalini and Chen, Zhihong and Delbrouck, Jean-Benoit and Reis, Eduardo and Truyts, Cesar and others},
  journal={Research Square},
  pages={rs--3},
  year={2024}
}