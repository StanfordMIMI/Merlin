FROM pytorch/pytorch:2.1.2-cuda11.8-cudnn8-runtime

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt-get update && apt-get install -y --no-install-recommends \
    git tzdata ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r user && useradd -r -m -g user user \
    && mkdir -p /workspace/inputs /workspace/outputs \
    && chown -R user:user /workspace

USER user
WORKDIR /opt/app

ENV PATH=/home/user/.local/bin:${PATH}
ENV HF_HOME=/home/user/.cache/huggingface
ENV TORCH_HOME=/home/user/.cache/torch
ENV MERLIN_CHECKPOINT_DIR=/home/user/.cache/huggingface/checkpoints

COPY --chown=user:user requirements.txt /opt/app/
RUN pip install --user --no-cache-dir -U pip && \
    pip install --user --no-cache-dir -r requirements.txt

# Pre-cache: Merlin checkpoint, Clinical-Longformer, ResNet-152
RUN mkdir -p ${MERLIN_CHECKPOINT_DIR} ${TORCH_HOME} && \
    python -c "from huggingface_hub import hf_hub_download; \
hf_hub_download(repo_id='stanfordmimi/Merlin', \
filename='i3_resnet_clinical_longformer_best_clip_04-02-2024_23-21-36_epoch_99.pt', \
local_dir='${MERLIN_CHECKPOINT_DIR}')" && \
    python -c "from transformers import AutoTokenizer, AutoModel; \
AutoTokenizer.from_pretrained('yikuan8/Clinical-Longformer'); \
AutoModel.from_pretrained('yikuan8/Clinical-Longformer')" && \
    python -c "import torchvision; torchvision.models.resnet152(pretrained=True)" && \
    python -c "import nltk; nltk.download('punkt', download_dir='/home/user/nltk_data')"

ENV NLTK_DATA=/home/user/nltk_data

COPY --chown=user:user transforms.py extract_feat_LP.py extract_feat_LP.sh /opt/app/
RUN chmod +x /opt/app/extract_feat_LP.sh

ENTRYPOINT []
