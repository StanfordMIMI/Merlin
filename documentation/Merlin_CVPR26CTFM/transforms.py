"""Shared MONAI transforms for Merlin LP feature extraction.

`MaskCenterCropd` is vendored here (not in PyPI `merlin-vlm==0.0.6`).
"""

import numpy as np
import torch
from monai.transforms import (
    CenterSpatialCropd,
    Compose,
    DeleteItemsd,
    EnsureChannelFirstd,
    LoadImaged,
    MapTransform,
    Orientationd,
    ScaleIntensityRanged,
    Spacingd,
    SpatialPadd,
    ToTensord,
)


ROI_SIZE = (224, 224, 160)
PIXDIM = (1.5, 1.5, 3)
INTENSITY_RANGE = dict(a_min=-1000, a_max=1000, b_min=0.0, b_max=1.0, clip=True)


class MaskCenterCropd(MapTransform):
    """Crop around the centroid of binary foreground mask voxels with zero padding."""

    def __init__(self, keys, mask_key="mask", roi_size=(224, 224, 160), fg_labels=None):
        super().__init__(keys)
        self.mask_key = mask_key
        self.roi_size = roi_size
        self.fg_labels = fg_labels
        self.img_key = "image"

    def __call__(self, data):
        d = dict(data)
        if self.fg_labels is not None:
            mask_arr = d[self.mask_key]
            if mask_arr.ndim == 4:
                mask_arr = mask_arr[0]
            mask_arr = np.isin(mask_arr, self.fg_labels).astype(np.uint8)
            coords = np.argwhere(mask_arr == 1)
            if coords.size == 0:
                # Fall back to original (un-resampled) mask if available, else image center
                mask_orig = d.get("mask_original")
                if mask_orig is not None:
                    if mask_orig.ndim == 4:
                        mask_orig = mask_orig[0]
                    mask_orig = np.isin(mask_orig, self.fg_labels).astype(np.uint8)
                    orig_coords = np.argwhere(mask_orig == 1)
                    if orig_coords.size > 0:
                        scale = np.array(mask_arr.shape) / np.array(mask_orig.shape)
                        coords = (orig_coords * scale).astype(int)
                if coords.size == 0:
                    coords = np.array([[s // 2 for s in mask_arr.shape]])
            center = tuple(coords.mean(axis=0).astype(int))
        else:
            img_arr = d[self.img_key]
            shape_img = img_arr.shape[1:] if img_arr.ndim == 4 else img_arr.shape
            center = tuple(s // 2 for s in shape_img)

        for key in self.keys:
            arr = d[key]
            has_channel = arr.ndim == 4
            arr_data = arr[0] if has_channel else arr
            cropped = self._crop_with_padding(arr_data, center, self.roi_size)
            d[key] = cropped[None] if has_channel else cropped
        return d

    @staticmethod
    def _crop_with_padding(arr, center, size):
        starts = [c - s // 2 for c, s in zip(center, size)]
        ends = [start + s for start, s in zip(starts, size)]
        if torch.is_tensor(arr):
            cropped = torch.zeros(size, dtype=arr.dtype, device=arr.device)
        else:
            cropped = np.zeros(size, dtype=arr.dtype)
        src_starts = [max(s, 0) for s in starts]
        src_ends = [min(e, arr.shape[i]) for i, e in enumerate(ends)]
        offs = [s - start for s, start in zip(src_starts, starts)]
        cropped[
            offs[0] : offs[0] + (src_ends[0] - src_starts[0]),
            offs[1] : offs[1] + (src_ends[1] - src_starts[1]),
            offs[2] : offs[2] + (src_ends[2] - src_starts[2]),
        ] = arr[
            src_starts[0] : src_ends[0],
            src_starts[1] : src_ends[1],
            src_starts[2] : src_ends[2],
        ]
        return cropped


def build_roi_transform():
    """Crop a 224×224×160 region centered on the binary fg_mask (label=1)."""
    return Compose(
        [
            LoadImaged(keys=["image", "mask", "mask_original"]),
            EnsureChannelFirstd(keys=["image", "mask", "mask_original"]),
            Orientationd(keys=["image", "mask", "mask_original"], axcodes="RAS"),
            Spacingd(
                keys=["image", "mask"], pixdim=PIXDIM, mode=("bilinear", "nearest")
            ),
            ScaleIntensityRanged(keys=["image"], **INTENSITY_RANGE),
            MaskCenterCropd(
                keys=["image"], mask_key="mask", roi_size=list(ROI_SIZE), fg_labels=[1]
            ),
            DeleteItemsd(keys=["mask", "mask_original"]),
            ToTensord(keys=["image"]),
        ]
    )


def build_non_roi_transform():
    """Center-crop a 224×224×160 region (no mask available)."""
    return Compose(
        [
            LoadImaged(keys=["image"]),
            EnsureChannelFirstd(keys=["image"]),
            Orientationd(keys=["image"], axcodes="RAS"),
            Spacingd(keys=["image"], pixdim=PIXDIM, mode="bilinear"),
            ScaleIntensityRanged(keys=["image"], **INTENSITY_RANGE),
            SpatialPadd(keys=["image"], spatial_size=list(ROI_SIZE)),
            CenterSpatialCropd(keys=["image"], roi_size=list(ROI_SIZE)),
            ToTensord(keys=["image"]),
        ]
    )
