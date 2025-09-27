import torch
from einops import rearrange
from torch import nn
from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM
from peft import get_peft_model, LoraConfig
import torchvision
from merlin.models import i3res
import copy


class ModifiedI3ResNet(nn.Module):
    def __init__(self, original_model):
        super(ModifiedI3ResNet, self).__init__()
        self.features = nn.Sequential(
            original_model.conv1,
            original_model.bn1,
            original_model.relu,
            original_model.maxpool,
            original_model.layer1,
            original_model.layer2,
            original_model.layer3,
            original_model.layer4,
        )

    def forward(self, x):
        x = self.features(x)
        # flatten the outputs torch.Size([8, 2048, 10, 7, 7]) -> torch.Size([8, 2048, 490])
        x = torch.flatten(x, start_dim=2)
        # swap 1st and 2nd dimensions torch.Size([8, 2048, 490]) -> torch.Size([8, 490, 2048])
        x = rearrange(x, "b c n -> b n c")
        return x


class ModifiedImageEncoder(nn.Module):
    def __init__(self):
        super().__init__()

        # Load the i3d resnet model
        resnet = torchvision.models.resnet152(pretrained=True)
        i3_resnet = i3res.I3ResNet(
            copy.deepcopy(resnet),
            class_nb=1692,
            conv_class=True,
            ImageEmbedding=True,
            PhenotypeCls=False,
        )

        # Modify the i3d resnet model
        modified_model = ModifiedI3ResNet(i3_resnet)

        self.vision_model = modified_model

    def forward(self, images):
        images = images.permute(0, 1, 4, 2, 3)
        images = torch.cat((images, images, images), dim=1)
        image_embeddings = self.vision_model(images)
        if len(image_embeddings.shape) == 2:
            image_embeddings = image_embeddings.unsqueeze(1)
        return image_embeddings


class Adapter(nn.Module):
    def __init__(self, input_size, output_size):
        super(Adapter, self).__init__()
        self.linear2 = nn.Linear(input_size, output_size)

    def forward(self, x):
        x = self.linear2(x)
        return x


class TextDecoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.tokenizer = AutoTokenizer.from_pretrained(
            "StanfordAIMI/RadLLaMA-7b",
            use_fast=True,
            trust_remote_code=True,
            cache_dir="./checkpoints",
        )
        self.text_decoder = AutoModelForCausalLM.from_pretrained(
            "StanfordAIMI/RadLLaMA-7b",
            cache_dir="./checkpoints",
        )
        self.text_decoder.gradient_checkpointing_enable()

        peft_params = LoraConfig(
            lora_alpha=16, lora_dropout=0.1, r=512, bias="none", task_type="CAUSAL_LM"
        )

        self.text_decoder = get_peft_model(self.text_decoder, peft_params)
        self.text_decoder.print_trainable_parameters()

    def forward(self, image_embeds, text_labels):
        inputs = self.tokenizer(
            text_labels,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=1024,
        ).to(self.text_decoder.device)

        input_ids = inputs.input_ids
        print("Input ids before crop:")
        print(input_ids)
        input_ids = input_ids[:, 1:]
        print("Input ids after crop:")
        print(input_ids)

        attention_mask = inputs.attention_mask[:, 1:]
        labels = input_ids.clone()
        labels[labels == self.tokenizer.pad_token_id] = -100
        # get the number of tokens until first : (inclusive) and set labels to -100
        for i in range(labels.shape[0]):
            for j in range(labels.shape[1]):
                if labels[i, j] == self.tokenizer.convert_tokens_to_ids("###\n"):
                    labels[i, : (j + 1)] = -100
                    break

        input_embeds = self.text_decoder.model.model.embed_tokens(input_ids)
        image_embeds_len = image_embeds.shape[1]
        image_labels = torch.ones(
            (image_embeds.shape[0], image_embeds_len), dtype=torch.long
        ).to(self.text_decoder.device)
        image_labels = image_labels * -100
        input_embeds = torch.cat((image_embeds, input_embeds), dim=1)
        labels = torch.cat((image_labels, labels), dim=1)
        attention_mask = torch.cat(
            (torch.ones_like(image_labels), attention_mask), dim=1
        )
        max_seq_len = 1024
        if input_embeds.shape[1] > max_seq_len:
            input_embeds = input_embeds[:, :max_seq_len, :]
            labels = labels[:, :max_seq_len]
            attention_mask = attention_mask[:, :max_seq_len]

        outputs = self.text_decoder(
            inputs_embeds=input_embeds, attention_mask=attention_mask, labels=labels
        )

        loss = outputs.loss
        return loss

    @torch.no_grad()
    def generate(self, image_embeds, text_labels, **kwargs):
        inputs = self.tokenizer(
            text_labels,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=1024,
        ).to(self.text_decoder.device)
        input_ids = inputs.input_ids
        input_ids = input_ids[:, 1:]

        input_embeds = self.text_decoder.model.model.embed_tokens(input_ids)

        input_embeds = torch.cat((image_embeds, input_embeds), dim=1)
        outputs = self.text_decoder.generate(inputs_embeds=input_embeds, **kwargs)
        texts = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
        return texts


class Clip3DForTextGeneration(nn.Module):
    def __init__(self):
        super().__init__()
        self.encode_image = ModifiedImageEncoder()
        self.decode_text = TextDecoder()
        self.adapter = Adapter(2048, 4096)
        for param in self.encode_image.parameters():
            param.requires_grad = False

    def forward(self, image, text):
        with torch.no_grad():
            image_features = self.encode_image(image)
            image_features = self.adapter(image_features)
            loss = self.decode_text(image_features, text)
            return loss

    @torch.no_grad()
    def generate(self, image, text_labels, **kwargs):
        image_features = self.encode_image(image)
        image_features = self.adapter(image_features)
        texts = self.decode_text.generate(image_features, text_labels, **kwargs)
        return texts
