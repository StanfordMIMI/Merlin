# Report Generation Documentation

This document provides instructions on how to use the Merlin model for generating radiology reports.

______________________________________________________________________

## Initialization

To initialize the model specifically for radiology report generation, set the `RadiologyReport` flag to `True`:

```python
from merlin import Merlin

model = Merlin(RadiologyReport=True)
```

______________________________________________________________________

## Capabilities

The Merlin model can generate radiology reports that cover findings related to the following organ systems and anatomical regions:

- Lower Thorax
- Liver and Biliary Tree
- Gallbladder
- Spleen
- Pancreas
- Adrenal Glands
- Kidneys and Ureters
- Gastrointestinal Tract
- Peritoneal Cavity
- Pelvic Organs
- Vasculature
- Lymph Nodes
- Musculoskeletal

______________________________________________________________________

## Model Weights & Storage

> ⚠️ **Important: Disk Space Required**
>
> The model weights are approximately **25 GB**. During the first run, these weights will be downloaded to a cache directory located at `merlin/models/checkpoints`. Please ensure you have sufficient disk space available before initializing the model.

______________________________________________________________________

## Demo Script

For a complete working example, please refer to the `report_generation_demo.py` script included in the documentation folder.

To run the demo, use the `accelerate launch` command. The `--mixed_precision fp16` flag is recommended to enable mixed precision for improved performance and reduced memory usage:

```bash
accelerate launch --mixed_precision fp16 report_generation_demo.py
```

______________________________________________________________________

## ❗ Disclaimer

This report generation capability is for **research purposes only** and is **not intended for clinical use**.
