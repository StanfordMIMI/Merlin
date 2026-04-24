"""Generic Merlin LP feature extractor (Docker entrypoint).

Reads .nii.gz files from --imgs_path, optionally pairs with binary fg_masks
in --masks_path, writes one .h5 per case to --out_path with key 'y_hat'.
"""

import argparse
import os

import h5py
import monai
import torch

from merlin import Merlin
from transforms import build_non_roi_transform, build_roi_transform


def build_datalist(imgs_path, masks_path):
    files = sorted(f for f in os.listdir(imgs_path) if f.endswith(".nii.gz"))
    if masks_path:
        files = [f for f in files if os.path.exists(os.path.join(masks_path, f))]

    datalist = []
    for fname in files:
        case_id = fname[: -len(".nii.gz")]
        item = {"image": os.path.join(imgs_path, fname), "filename": case_id}
        if masks_path:
            mask = os.path.join(masks_path, fname)
            item["mask"] = mask
            item["mask_original"] = mask
        datalist.append(item)
    return datalist


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--imgs_path", default="workspace/inputs")
    ap.add_argument("-o", "--out_path", default="workspace/outputs")
    ap.add_argument(
        "--masks_path", default="", help="Binary fg_mask dir; enables ROI crop when set"
    )
    ap.add_argument("--batch_size", type=int, default=1)
    ap.add_argument("--num_workers", type=int, default=0)
    args = ap.parse_args()

    masks_path = args.masks_path or None
    os.makedirs(args.out_path, exist_ok=True)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = Merlin(ImageEmbedding=True).eval().to(device)

    transform = build_roi_transform() if masks_path else build_non_roi_transform()
    datalist = build_datalist(args.imgs_path, masks_path)
    print(f"Found {len(datalist)} cases (masks={'on' if masks_path else 'off'})")

    dataloader = monai.data.ThreadDataLoader(
        monai.data.Dataset(data=datalist, transform=transform),
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=args.num_workers,
        pin_memory=False,
    )

    with torch.no_grad():
        for batch in dataloader:
            filenames = batch["filename"]
            images = batch["image"].to(device, non_blocking=True)
            embeds = model(images)[0].detach().cpu()
            for i, filename in enumerate(filenames):
                out_path = os.path.join(args.out_path, f"{filename}.h5")
                with h5py.File(out_path, "w") as hf:
                    hf.create_dataset("y_hat", data=embeds[i].numpy())
                print(f"Saved {out_path} (shape={tuple(embeds[i].shape)})")
            torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
