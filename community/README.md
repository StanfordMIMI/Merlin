# Merlin Community Projects 🤝

Work built on top of Merlin, which include models, datasets, tools, benchmarks, and tutorials contributed by the community.

Everything listed here is **hosted and maintained by its own authors**. This directory is an index: each project is described by a small YAML file in [`entries/`](entries), and the table below is generated from those files. Nothing is stored in this repository, and a listing is not an endorsement or a validation of clinical safety.

**Want to add your project?** See [CONTRIBUTING.md](CONTRIBUTING.md), copy [`template.yaml`](template.yaml), fill in the fields, and open a pull request.

## Projects

<!-- COMMUNITY_TABLE:START -->

| Project | Type | Description | License |
| --- | --- | --- | --- |
| [Merlin Plus](https://github.com/MrGiovanni/MerlinPlus) | dataset | Merlin Plus (MICCAI 2026) provides longitudinal metadata (patient IDs and scan dates) and per-voxel annotations for 44 organs and 9 tumor types in the Merlin dataset (Stanford, 25,494 CT scans). Merlin Plus allows AI models to surpass the state-of-the-art in multi-cancer detection and segmentation. | CC BY-NC-ND 4.0 |
| [Merlin-Cancer-Net](https://huggingface.co/AbdomenAtlas/Merlin-Cancer-Net) | model | Merlin-Cancer-Net is an nnU-Net trained with the tumor segmentation masks from the Merlin Plus dataset. It detects and segments tumors in 9 organs: bladder, gallbladder, spleen, esophagus, stomach, duodenum, prostate, uterus, and adrenal glands. | CC BY-NC-ND 4.0 |
| [Merlin-nnUNet](https://github.com/ashwinkumargb/Merlin-nnUNet) | model | Integrates the Merlin image encoder into the nnU-Net framework for 3D abdominal CT segmentation, with setup and inference instructions. | Apache-2.0 |
| [Merlin-Super](https://huggingface.co/AbdomenAtlas/Merlin-Cancer-Super) | model | R-Super (Report Supervision, MICCAI 2025 Best Paper runner-up) learns tumor segmentation from radiology reports. Merlin-Super is R-Super trained on Merlin Plus, surpassing public AI models for tumors in 9 organs: bladder, gallbladder, spleen, esophagus, stomach, duodenum, prostate, uterus, adrenal. | CC BY-NC-ND 4.0 |
| [ORCA-3DCT](https://github.com/renjie-liang/ORCA-3DCT) | dataset | Training-free ORCA compression of 3D-CT tokens on the Merlin abdominal CT dataset: SuPreM and SegVol embeddings (ORCA and grid-average at several budgets), the uncompressed encoder grids, and TotalSegmentator organ masks on each encoder's token grid. | CC BY-NC 4.0 |

<details>
<summary><b>Merlin Plus</b> — dataset</summary>

- **Description:** Merlin Plus (MICCAI 2026) provides longitudinal metadata (patient IDs and scan dates) and per-voxel annotations for 44 organs and 9 tumor types in the Merlin dataset (Stanford, 25,494 CT scans). Merlin Plus allows AI models to surpass the state-of-the-art in multi-cancer detection and segmentation.
- **Authors:** Pedro R. A. S. Bassi (Johns Hopkins University; Harvard Medical School; Massachusetts General Hospital), Wenxuan Li (Johns Hopkins University; Harvard Medical School; Massachusetts General Hospital), Szymon Płotka (Jagiellonian University), Ruby Honjol (Stanford University), Jakub Prządo (Warmian-Masurian Cancer Center), Xinze Zhou (Johns Hopkins University), Kang Wang (University of California, San Francisco), Yang Yang (University of California, San Francisco), Malte Jensen (Stanford University), Akshay S. Chaudhari (Stanford University), Curtis P. Langlotz (Stanford University), Alan L. Yuille (Johns Hopkins University), Zongwei Zhou (Johns Hopkins University; Johns Hopkins Medicine)
- **Links:** [Code](https://github.com/MrGiovanni/MerlinPlus) · [Data](https://huggingface.co/datasets/AbdomenAtlas/MerlinPlus) · [Paper](https://papers.miccai.org/miccai-2026/paper/4063_paper.pdf)
- **License:** CC BY-NC-ND 4.0
- **Builds on:** Merlin Abdominal CT Dataset
- **Tags:** `segmentation`, `abdominal-ct`, `cancer detection`, `cancer segmentation`, `tumor`
- **Contact:** psalvad2@jh.edu
- **Added:** 2026-09-23 · **Entry:** [`merlin-plus.yaml`](entries/merlin-plus.yaml)

```bibtex
@InProceedings{BasPed_Merlin_MICCAI2026,
      author = { Bassi, Pedro R. A. S. AND Li, Wenxuan AND Płotka, Szymon AND Honjol, Ruby AND Prządo, Jakub AND Zhou, Xinze AND Wang, Kang AND Yang, Yang AND Jensen, Malte AND Chaudhari, Akshay S. AND Langlotz, Curtis P. AND Yuille, Alan L. AND Zhou, Zongwei},
      title = { { Merlin Plus: A Large-Scale, Multi-cancer, Image-Mask-Report Dataset } },
      booktitle = {Medical Image Computing and Computer Assisted Intervention -- MICCAI 2026},
      year = {2026},
      publisher = {Springer Nature Switzerland},
      volume = {LNCS 16895},
      month = {September},
      page = {pending}
}
```

</details>

<details>
<summary><b>Merlin-Cancer-Net</b> — model</summary>

- **Description:** Merlin-Cancer-Net is an nnU-Net trained with the tumor segmentation masks from the Merlin Plus dataset. It detects and segments tumors in 9 organs: bladder, gallbladder, spleen, esophagus, stomach, duodenum, prostate, uterus, and adrenal glands.
- **Authors:** Pedro R. A. S. Bassi (Johns Hopkins University, Baltimore, MD, USA; Harvard Medical School, Boston, MA, USA; Massachusetts General Hospital, Boston, MA, USA), Xinze Zhou (Johns Hopkins University, Baltimore, MD, USA), Wenxuan Li (Johns Hopkins University, Baltimore, MD, USA; Harvard Medical School, Boston, MA, USA; Massachusetts General Hospital, Boston, MA, USA), Szymon Płotka (Jagiellonian University, Kraków, Poland), Jakob Wasserthal (University Hospital Basel, Basel, Switzerland), Jieneng Chen (Johns Hopkins University, Baltimore, MD, USA), Ibrahim E. Hamamci (University of Zurich, Zurich, Switzerland; ETH AI Center, Zurich, Switzerland), Sezgin Er (University of Zurich, Zurich, Switzerland; Istanbul Medipol University, Istanbul, Turkey), Jakub Prządo (Warmian-Masurian Cancer Center, Olsztyn, Poland), Zheren Zhu (University of California, Berkeley, CA, USA; University of California, San Francisco, CA, USA), Gorkem Durak (Northwestern University, Illinois, USA), Wiktoria Romańczyk (Medical University of Białystok, Poland), Yavuz B. Taktak (Istanbul University, Istanbul, Turkey), Melih Akan (Istanbul Medipol University, Istanbul, Turkey), Gülhan E. Akan (Istanbul Medipol University, Istanbul, Turkey), Yuhan Wang (University of California, Santa Cruz, CA, USA), Scott Ye (University of California, San Francisco, CA, USA), Qi Chen (Johns Hopkins University, Baltimore, MD, USA), Ashwin Kumar (Stanford University, Stanford, CA, USA), Lizhou Wu (Shandong Provincial Qianfoshan Hospital, Shandong, China), Guang Zhang (Shandong Provincial Qianfoshan Hospital, Shandong, China), Bjoern Menze (University of Zurich, Zurich, Switzerland), Jarosław B. Ćwikła (University of Warmia and Mazury, Olsztyn, Poland), Yuyin Zhou (University of California, Santa Cruz, CA, USA; Google, San Francisco, CA, USA), Frank H. Miller (Northwestern University, Illinois, USA), Yunhe Gao (Stanford University, Stanford, CA, USA), Akshay S. Chaudhari (Stanford University, Stanford, CA, USA), Curtis P. Langlotz (Stanford University, Stanford, CA, USA), Ulas Bagci (Northwestern University, Illinois, USA), Sergio Decherchi (Istituto Italiano di Tecnologia, Genoa, Italy), Andrea Cavalli (Istituto Italiano di Tecnologia, Genoa, Italy; University of Bologna, Bologna, Italy; École Polytechnique Fédérale de Lausanne, Lausanne, Switzerland), Arkadiusz Sitek (Harvard Medical School, Boston, MA, USA; Massachusetts General Hospital, Boston, MA, USA), Kang Wang (University of California, San Francisco, CA, USA), Yang Yang (University of California, San Francisco, CA, USA), Alan L. Yuille (Johns Hopkins University, Baltimore, MD, USA), Zongwei Zhou (Johns Hopkins University, Baltimore, MD, USA; Johns Hopkins Medicine, Baltimore, MD, USA)
- **Links:** [Code](https://huggingface.co/AbdomenAtlas/Merlin-Cancer-Net) · [Data](https://huggingface.co/datasets/AbdomenAtlas/MerlinPlus) · [Paper](https://www.researchsquare.com/article/rs-10131590/v1)
- **License:** CC BY-NC-ND 4.0
- **Builds on:** Merlin Abdominal CT Dataset
- **Tags:** `segmentation`, `abdominal-ct`, `cancer detection`, `cancer segmentation`, `tumor`
- **Contact:** psalvad2@jh.edu
- **Added:** 2026-09-23 · **Entry:** [`merlin-cancer-net.yaml`](entries/merlin-cancer-net.yaml)

```bibtex
@misc{bassi2026largescalemulticancer,
title = {Large-Scale Multi-Cancer Detection by Learning Segmentation from Reports},
author = {Pedro R A S Bassi and
          Xinze Zhou and
          Wenxuan Li and
          Szymon Płotka and
          Jakob Wasserthal and
          Jieneng Chen and
          Ibrahim E Hamamci and
          Sezgin Er and
          Jakub Prządo and
          Zheren Zhu and
          Gorkem Durak and
          Wiktoria Romańczyk and
          Yavuz B Taktak and
          Melih Akan and
          Yuhan Wang and
          Scott Ye and
          Qi Chen and
          Ashwin Kumar and
          Lizhou Wu and
          Guang Zhang and
          Bjoern Menze and
          Jarosław B Ćwikła and
          Yuyin Zhou and
          Frank H Miller and
          Yunhe Gao and
          Akshay S Chaudhari and
          Curtis P Langlotz and
          Ulas Bagci and
          Sergio Decherchi and
          Andrea Cavalli and
          Arkadiusz Sitek and
          Kang Wang and
          Yang Yang and
          Alan L Yuille and
          Zongwei Zhou},
year = {2026},
month = {7},
day = {15},
howpublished = {Research Square},
note = {Preprint, version 1},
doi = {10.21203/rs.3.rs-10131590/v1},
url = {https://www.researchsquare.com/article/rs-10131590/v1},
}
```

</details>

<details>
<summary><b>Merlin-nnUNet</b> — model</summary>

- **Description:** Integrates the Merlin image encoder into the nnU-Net framework for 3D abdominal CT segmentation, with setup and inference instructions.
- **Authors:** Ashwin Kumar (Stanford University)
- **Links:** [Code](https://github.com/ashwinkumargb/Merlin-nnUNet)
- **License:** Apache-2.0
- **Builds on:** image encoder
- **Tags:** `segmentation`, `abdominal-ct`, `nnU-Net`
- **Contact:** akkumar@stanford.edu
- **Added:** 2026-09-11 · **Entry:** [`merlin-nnunet.yaml`](entries/merlin-nnunet.yaml)

</details>

<details>
<summary><b>Merlin-Super</b> — model</summary>

- **Description:** R-Super (Report Supervision, MICCAI 2025 Best Paper runner-up) learns tumor segmentation from radiology reports. Merlin-Super is R-Super trained on Merlin Plus, surpassing public AI models for tumors in 9 organs: bladder, gallbladder, spleen, esophagus, stomach, duodenum, prostate, uterus, adrenal.
- **Authors:** Pedro R. A. S. Bassi (Johns Hopkins University, Baltimore, MD, USA; Harvard Medical School, Boston, MA, USA; Massachusetts General Hospital, Boston, MA, USA), Xinze Zhou (Johns Hopkins University, Baltimore, MD, USA), Wenxuan Li (Johns Hopkins University, Baltimore, MD, USA; Harvard Medical School, Boston, MA, USA; Massachusetts General Hospital, Boston, MA, USA), Szymon Płotka (Jagiellonian University, Kraków, Poland), Jakob Wasserthal (University Hospital Basel, Basel, Switzerland), Jieneng Chen (Johns Hopkins University, Baltimore, MD, USA), Ibrahim E. Hamamci (University of Zurich, Zurich, Switzerland; ETH AI Center, Zurich, Switzerland), Sezgin Er (University of Zurich, Zurich, Switzerland; Istanbul Medipol University, Istanbul, Turkey), Jakub Prządo (Warmian-Masurian Cancer Center, Olsztyn, Poland), Zheren Zhu (University of California, Berkeley, CA, USA; University of California, San Francisco, CA, USA), Gorkem Durak (Northwestern University, Illinois, USA), Wiktoria Romańczyk (Medical University of Białystok, Poland), Yavuz B. Taktak (Istanbul University, Istanbul, Turkey), Melih Akan (Istanbul Medipol University, Istanbul, Turkey), Gülhan E. Akan (Istanbul Medipol University, Istanbul, Turkey), Yuhan Wang (University of California, Santa Cruz, CA, USA), Scott Ye (University of California, San Francisco, CA, USA), Qi Chen (Johns Hopkins University, Baltimore, MD, USA), Ashwin Kumar (Stanford University, Stanford, CA, USA), Lizhou Wu (Shandong Provincial Qianfoshan Hospital, Shandong, China), Guang Zhang (Shandong Provincial Qianfoshan Hospital, Shandong, China), Bjoern Menze (University of Zurich, Zurich, Switzerland), Jarosław B. Ćwikła (University of Warmia and Mazury, Olsztyn, Poland), Yuyin Zhou (University of California, Santa Cruz, CA, USA; Google, San Francisco, CA, USA), Frank H. Miller (Northwestern University, Illinois, USA), Yunhe Gao (Stanford University, Stanford, CA, USA), Akshay S. Chaudhari (Stanford University, Stanford, CA, USA), Curtis P. Langlotz (Stanford University, Stanford, CA, USA), Ulas Bagci (Northwestern University, Illinois, USA), Sergio Decherchi (Istituto Italiano di Tecnologia, Genoa, Italy), Andrea Cavalli (Istituto Italiano di Tecnologia, Genoa, Italy; University of Bologna, Bologna, Italy; École Polytechnique Fédérale de Lausanne, Lausanne, Switzerland), Arkadiusz Sitek (Harvard Medical School, Boston, MA, USA; Massachusetts General Hospital, Boston, MA, USA), Kang Wang (University of California, San Francisco, CA, USA), Yang Yang (University of California, San Francisco, CA, USA), Alan L. Yuille (Johns Hopkins University, Baltimore, MD, USA), Zongwei Zhou (Johns Hopkins University, Baltimore, MD, USA; Johns Hopkins Medicine, Baltimore, MD, USA)
- **Links:** [Code](https://github.com/MrGiovanni/R-Super) · [Data](https://huggingface.co/datasets/AbdomenAtlas/MerlinPlus) · [Paper](https://www.researchsquare.com/article/rs-10131590/v1) · [Demo](https://huggingface.co/AbdomenAtlas/Merlin-Cancer-Super)
- **License:** CC BY-NC-ND 4.0
- **Builds on:** Merlin Abdominal CT Dataset
- **Tags:** `segmentation`, `abdominal-ct`, `cancer detection`, `cancer segmentation`, `tumor`
- **Contact:** psalvad2@jh.edu
- **Added:** 2026-09-23 · **Entry:** [`merlin-cancer-super.yaml`](entries/merlin-cancer-super.yaml)

```bibtex
@misc{bassi2026largescalemulticancer,
title = {Large-Scale Multi-Cancer Detection by Learning Segmentation from Reports},
author = {Pedro R A S Bassi and
          Xinze Zhou and
          Wenxuan Li and
          Szymon Płotka and
          Jakob Wasserthal and
          Jieneng Chen and
          Ibrahim E Hamamci and
          Sezgin Er and
          Jakub Prządo and
          Zheren Zhu and
          Gorkem Durak and
          Wiktoria Romańczyk and
          Yavuz B Taktak and
          Melih Akan and
          Yuhan Wang and
          Scott Ye and
          Qi Chen and
          Ashwin Kumar and
          Lizhou Wu and
          Guang Zhang and
          Bjoern Menze and
          Jarosław B Ćwikła and
          Yuyin Zhou and
          Frank H Miller and
          Yunhe Gao and
          Akshay S Chaudhari and
          Curtis P Langlotz and
          Ulas Bagci and
          Sergio Decherchi and
          Andrea Cavalli and
          Arkadiusz Sitek and
          Kang Wang and
          Yang Yang and
          Alan L Yuille and
          Zongwei Zhou},
year = {2026},
month = {7},
day = {15},
howpublished = {Research Square},
note = {Preprint, version 1},
doi = {10.21203/rs.3.rs-10131590/v1},
url = {https://www.researchsquare.com/article/rs-10131590/v1},
}
```

</details>

<details>
<summary><b>ORCA-3DCT</b> — dataset</summary>

- **Description:** Training-free ORCA compression of 3D-CT tokens on the Merlin abdominal CT dataset: SuPreM and SegVol embeddings (ORCA and grid-average at several budgets), the uncompressed encoder grids, and TotalSegmentator organ masks on each encoder's token grid.
- **Authors:** Renjie Liang, Zijian Xu, Jinqian Pan, Chengkun Sun, Zhengkang Fan, Shawn Li, You Qin, Mei Liu, Jie Xu
- **Links:** [Code](https://github.com/renjie-liang/ORCA-3DCT) · [Data](https://huggingface.co/datasets/LiangRenjie/ORCA-3DCT) · [Paper](https://arxiv.org/abs/2608.00345)
- **License:** CC BY-NC 4.0
- **Builds on:** Merlin Abdominal CT Dataset
- **Tags:** `3d-ct`, `token-compression`, `abdominal-ct`, `embeddings`, `organ-masks`
- **Contact:** liang.renjie@ufl.edu
- **Added:** 2026-09-14 · **Entry:** [`orca-3dct.yaml`](entries/orca-3dct.yaml)

```bibtex
@article{liang2026orca,
  title={ORCA: ORgan-Centroid Aggregation for Training-Free 3D CT Visual Token Compression},
  author={Liang, Renjie and Xu, Zijian and Pan, Jinqian and Sun, Chengkun and Fan, Zhengkang and Li, Shawn and Qin, You and Liu, Mei and Xu, Jie},
  journal={arXiv preprint arXiv:2608.00345},
  year={2026}
}
```

</details>

<!-- COMMUNITY_TABLE:END -->

<sub>The table and the expandable entries above are generated by [`validate.py`](validate.py) from the files in [`entries/`](entries). Therefore, you should edit your YAML file, not this section.</sub>
