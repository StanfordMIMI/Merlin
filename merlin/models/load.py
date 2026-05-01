import os

import torch
from torch import nn

from merlin.models.build import MerlinArchitecture
from merlin.models.radiology_report_generation import Clip3DForTextGeneration
from merlin.utils import download_file
from typing import Dict, Any

REPO_ID = "stanfordmimi/Merlin"
MODEL_CONFIGS: Dict[str, Dict[str, Any]] = {
    "default": {
        "builder": MerlinArchitecture,
        "checkpoint": "i3_resnet_clinical_longformer_best_clip_04-02-2024_23-21-36_epoch_99.pt",
    },
    "report_generation": {
        "builder": Clip3DForTextGeneration,
        "checkpoint": "resnet_gpt2_best_stanford_report_generation_average_mtl.pt",
    },
    "report_generation_stage1_stage2": {
        "builder": Clip3DForTextGeneration,
        "checkpoint": "resnet_gpt2_best_stanford_report_generation_average.pt",
    },
    "five_year_disease_prediction": {
        "builder": MerlinArchitecture,
        "checkpoint": "resnet_clinical_longformer_five_year_disease_prediction.pt",
    },
}


class Merlin(nn.Module):
    def __init__(
        self,
        ImageEmbedding: bool = False,
        PhenotypeCls: bool = False,
        RadiologyReport: bool = False,
        RadiologyReportStage1_Stage2: bool = False,
        FiveYearPred: bool = False,
    ):
        super(Merlin, self).__init__()

        # If both are True, raise an error
        if sum([ImageEmbedding, PhenotypeCls, FiveYearPred]) > 1:
            raise ValueError(
                "ImageEmbedding and PhenotypeCls and FiveYearPred cannot be True at the same time."
            )

        if sum([RadiologyReport, RadiologyReportStage1_Stage2]) > 1:
            raise ValueError(
                "RadiologyReport and RadiologyReportStage1_Stage2 cannot be True at the same time."
            )

        if RadiologyReport:
            self.task = "report_generation"
        elif RadiologyReportStage1_Stage2:
            self.task = "report_generation_stage1_stage2"
        elif FiveYearPred:
            self.task = "five_year_disease_prediction"
        else:
            self.task = "default"

        self._config = MODEL_CONFIGS[self.task]

        # Pass through the flags needed by the underlying model builders
        model_kwargs = (
            {
                "ImageEmbedding": ImageEmbedding,
                "PhenotypeCls": PhenotypeCls,
                "FiveYearPred": FiveYearPred,
            }
            if not RadiologyReport and not RadiologyReportStage1_Stage2
            else {}
        )
        self.model = self._load_model(**model_kwargs)

    def _load_model(self, **kwargs) -> nn.Module:
        """
        Downloads the correct checkpoint and constructs the appropriate model.
        """
        checkpoint_name = self._config["checkpoint"]
        model_builder = self._config["builder"]

        # Download checkpoint to local directory
        local_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "checkpoints"
        )
        checkpoint_path = os.path.join(local_dir, checkpoint_name)
        self._download_checkpoint(filename=checkpoint_name, local_dir=local_dir)

        # Build the model
        model = model_builder(**kwargs)

        print(f"Loading checkpoint for '{self.task}' task from {checkpoint_path}")
        state_dict = torch.load(checkpoint_path, map_location="cpu")

        if self.task == "five_year_disease_prediction":
            model.encode_image.i3_resnet.load_state_dict(state_dict, strict=True)
        else:
            model.load_state_dict(state_dict)

        return model

    def _download_checkpoint(self, filename: str, local_dir: str):
        if not os.path.exists(os.path.join(local_dir, filename)):
            print(f"Downloading {filename} from Hugging Face Hub...")
            download_file(repo_id=REPO_ID, filename=filename, local_dir=local_dir)

    def forward(self, *args, **kwargs):
        """Delegates the forward call to the underlying model."""
        return self.model(*args, **kwargs)

    def generate(self, *args, **kwargs):
        """
        Generates text if the model is in RadiologyReport mode.
        Passes all arguments to the underlying model's generate method.
        """
        if (
            self.task != "report_generation"
            and self.task != "report_generation_stage1_stage2"
        ):
            raise AttributeError(
                "The 'generate' method is only available when RadiologyReport=True or RadiologyReportStage1_Stage2=True."
            )
        # Delegate the call to the actual text generation model
        return self.model.generate(*args, **kwargs)
