import os

import torch
from torch import nn

from merlin.models.build import MerlinArchitecture
from merlin.utils import download_file


class Merlin(nn.Module):
    def __init__(self, ImageEmbedding: bool = False, PhenotypeCls: bool = False):
        super(Merlin, self).__init__()
        self.ImageEmbedding = ImageEmbedding
        self.PhenotypeCls = PhenotypeCls

        # If both are True, raise an error
        if self.ImageEmbedding and self.PhenotypeCls:
            raise ValueError(
                "Both ImageEmbedding and PhenotypeCls cannot be True at the same time."
            )

        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.local_dir = os.path.join(self.current_path, "checkpoints")
        self.checkpoint_name = (
            "i3_resnet_clinical_longformer_best_clip_04-02-2024_23-21-36_epoch_99.pt"
        )
        self.repo_id = "stanfordmimi/Merlin"
        self.model = self._load_model()

    """
    Load the Merlin model with the initialized weights
    """

    def _load_model(self):
        self._download_checkpoint()
        model = MerlinArchitecture(
            ImageEmbedding=self.ImageEmbedding, PhenotypeCls=self.PhenotypeCls
        )
        model.load_state_dict(
            torch.load(os.path.join(self.local_dir, self.checkpoint_name))
        )
        return model

    """ 
    Download the Merlin weights from the Hugging Face Hub
    """

    def _download_checkpoint(self):
        download_file(
            repo_id=self.repo_id,
            filename=self.checkpoint_name,
            local_dir=self.local_dir,
        )

    def forward(self, *input):
        return self.model(*input)
