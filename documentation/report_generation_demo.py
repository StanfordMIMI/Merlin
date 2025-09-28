"""
Generate a radiology report for each organ system in the Merlin Abdominal CT Dataset
and print the report for each organ system

Usage:
accelerate launch --mixed_precision fp16 report_generation_demo.py

Output:
Prints the radiology report for each organ system

"""

import os
import warnings
import torch

from merlin.data import download_sample_data
from merlin.data import DataLoader
from merlin import Merlin


from transformers import StoppingCriteria
from collections import defaultdict


class EosListStoppingCriteria(StoppingCriteria):
    def __init__(self, eos_sequence=[48134]):
        self.eos_sequence = eos_sequence

    def __call__(
        self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs
    ) -> bool:
        last_ids = input_ids[:, -len(self.eos_sequence) :].tolist()
        return self.eos_sequence in last_ids


warnings.filterwarnings("ignore")
device = "cuda" if torch.cuda.is_available() else "cpu"

model = Merlin()
model.eval()
model.cuda()

data_dir = os.path.join(os.path.dirname(__file__), "abct_data")
cache_dir = data_dir.replace("abct_data", "abct_data_cache")

organ_system_variations = {
    "lower thorax|lower chest|lung bases": "lower thorax",
    "liver|liver and biliary tree|biliary system": "liver",
    "gallbladder": "gallbladder",
    "spleen": "spleen",
    "pancreas": "pancreas",
    "adrenal glands|adrenals": "adrenal glands",
    "kidneys|kidneys and ureters| gu |kidneys, ureters": "kidneys",
    "bowel|gastrointestinal tract| gi |bowel/mesentery": "bowel",
    "peritoneal space|peritoneal cavity|abdominal wall|peritoneum": "peritoneum",
    "pelvic organs|bladder|prostate and seminal vesicles|pelvis|uterus and ovaries": "pelvic",
    "vasculature": "circulatory",
    "lymph nodes": "lymph nodes",
    "musculoskeletal|bones": "musculoskeletal",
}

organ_systems = list(organ_system_variations.values())


datalist = [
    {
        "image": download_sample_data(
            data_dir
        ),  # function returns local path to nifti file
    },
]

dataloader = DataLoader(
    datalist=datalist,
    cache_dir=cache_dir,
    batchsize=8,
    shuffle=True,
    num_workers=0,
)

model = Merlin(RadiologyReport=True)
model.eval()
model.cuda()

generations_dict = defaultdict(list)

for batch in dataloader:
    images = batch["image"]
    images = images.cuda()
    for i, organ_system in enumerate(organ_systems):
        prefix = "Generate a radiology report for " + organ_system + "###\n"
        prefix_in = [prefix] * len(images)
        generations = model.generate(
            images,
            prefix_in,
            do_sample=False,
            num_beams=1,
            repetition_penalty=1.2,
            max_new_tokens=128,
            stopping_criteria=[EosListStoppingCriteria()],
        )
        generations_dict[organ_system].extend(generations)

    # Print the generations for each organ system
    print("Merlin Radiology Report: ", end="")
    for _, value in generations_dict.items():
        print(value[0].split("###")[0], end=" ")
