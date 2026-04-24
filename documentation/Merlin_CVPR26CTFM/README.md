# Merlin for CVPR 2026 CT FM Challenge — Task 1 (LP)

Docker submission package for the [CVPR 2026 Foundation Models for 3D CT Challenge](https://www.codabench.org/competitions/12650/)
using the [Merlin](https://github.com/StanfordMIMI/Merlin) model (Stanford MIMI) as a frozen 3D CT feature extractor.

The container is dataset-agnostic: any folder of `.nii.gz` scans is accepted, and binary
foreground masks are used when present. Outputs one `.h5` per case (dataset key `y_hat`,
shape `(2048,)`).

## Get the image

### Option A — Download pre-built image (~8.4 GB)

A pre-built `merlin_lp.tar.gz` is available here:

> 🔗 **https://huggingface.co/yws0322/cvpr26ctfm-merlin/resolve/main/merlin_lp.tar.gz**

```bash
# Download then load into Docker
wget -O merlin_lp.tar.gz https://huggingface.co/yws0322/cvpr26ctfm-merlin/resolve/main/merlin_lp.tar.gz
docker load -i merlin_lp.tar.gz
docker images | grep merlin_lp   # confirm merlin_lp:latest is present
```

### Option B — Build from source

```bash
bash build_docker.sh
# → ./merlin_lp.tar.gz (bakes in Merlin checkpoint, Clinical-Longformer, ResNet-152)
```

## I/O contract

- **Input** (`-v $PWD/inputs/:/workspace/inputs/`): folder of `*.nii.gz` images.
- **Mask** (optional, `-e MASKS_DIR=/workspace/inputs/<subdir>`): binary fg_masks (label `1`)
  with filenames matching the images. When set, crops a `224×224×160` volume centered on
  the mask; otherwise center-crops the full image.
- **Output** (`-v $PWD/outputs/:/workspace/outputs/`): `<case_id>.h5` per case, one
  dataset `y_hat` of shape `(2048,)`.
- `batch_size=1`, single-image processing (challenge requirement).

## Run

### AMOS-clf-tr-val (CVPR26 challenge data)

ROI diseases use binary fg_masks; non-ROI diseases run without `MASKS_DIR`.

```bash
# ROI disease (e.g. adrenal_hyperplasia)
docker run --gpus '"device=0"' -m 32G --rm \
    -e MASKS_DIR=/workspace/inputs/fg_masks/adrenal_hyperplasia \
    -v /path/to/amos-clf-tr-val/:/workspace/inputs/ \
    -v $PWD/outputs_amos_roi/:/workspace/outputs/ \
    merlin_lp:latest /bin/bash -c "sh extract_feat_LP.sh"

# Non-ROI disease (e.g. ascites)
docker run --gpus '"device=0"' -m 32G --rm \
    -v /path/to/amos-clf-tr-val/images/:/workspace/inputs/ \
    -v $PWD/outputs_amos_nonroi/:/workspace/outputs/ \
    merlin_lp:latest /bin/bash -c "sh extract_feat_LP.sh"
```

### COVID-CT

No fg_masks → non-ROI mode (center crop).

```bash
docker run --gpus '"device=0"' -m 32G --rm \
    -v /path/to/COVID-CT/images/:/workspace/inputs/ \
    -v $PWD/outputs_covid/:/workspace/outputs/ \
    merlin_lp:latest /bin/bash -c "sh extract_feat_LP.sh"
```

### LUNA25

No fg_masks → non-ROI mode (center crop).

```bash
docker run --gpus '"device=0"' -m 32G --rm \
    -v /path/to/LUNA25/images/:/workspace/inputs/ \
    -v $PWD/outputs_luna25/:/workspace/outputs/ \
    merlin_lp:latest /bin/bash -c "sh extract_feat_LP.sh"
```

## Run without Docker (Python)

The same `extract_feat_LP.py` works standalone — useful for quick local runs
without building/loading the image.

```bash
# Setup
uv venv --python 3.11
source .venv/bin/activate
uv pip install -r requirements.txt

# Non-ROI mode (no mask)
python extract_feat_LP.py \
    -i /path/to/images \
    -o /path/to/outputs \
    --batch_size 4 --num_workers 4

# ROI mode (binary fg_mask)
python extract_feat_LP.py \
    -i /path/to/images \
    --masks_path /path/to/fg_masks/<disease> \
    -o /path/to/outputs \
    --batch_size 4 --num_workers 4
```

`batch_size` can be larger than 1 outside Docker (the `batch_size=1` constraint
is only for the challenge submission). Larger batches speed up bulk extraction
on training/val splits substantially.

## Files

| File | Role |
|------|------|
| `Dockerfile` | CUDA 11.8 image with Merlin and weights pre-baked |
| `extract_feat_LP.py` | Generic single-image feature extractor (Docker entrypoint logic) |
| `extract_feat_LP.sh` | Shell wrapper, env-driven (`INPUT_DIR`, `OUTPUT_DIR`, `MASKS_DIR`) |
| `transforms.py` | MONAI preprocessing pipelines (ROI / non-ROI) |
| `requirements.txt` | Python dependencies |
| `build_docker.sh` | Builds image and saves `merlin_lp.tar.gz` |

## Downstream LP

For LP head training, val inference, and `predictions.zip` generation, use the
upstream challenge repo: [`CVPR26-3DCTFMCompetition`](https://github.com/kmin940/CVPR26-3DCTFMCompetition)
(`run_LP.py` → `cvpr26_inference_LP.py` → `cvpr26_organize_eval_metrics_and_predictions.py`).
