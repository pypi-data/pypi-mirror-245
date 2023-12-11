import torch
import torch.nn as nn
from functools import partial
from torchvision import transforms
from PIL import Image
import os
import pandas as pd
import random
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset, random_split
from torchvision.transforms import v2

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from collections import Counter

MODEL_PATH = "../models/"

class ResidualBlock(torch.nn.Module):
    def __init__(self, in_channels, out_channels, stride):
        super().__init__()
        self.C1 = torch.nn.Conv2d(
            in_channels,
            out_channels,
            3,
            stride=stride,
            padding=1,
        )
        self.N1 = torch.nn.BatchNorm2d(num_features=out_channels)
        self.R1 = torch.nn.ReLU()
        self.C2 = torch.nn.Conv2d(out_channels, out_channels, 3, padding=1)
        self.N2 = torch.nn.BatchNorm2d(num_features=out_channels)
        self.R2 = torch.nn.ReLU()

        self.has_skip_conv = stride != 0 or in_channels != out_channels
        if self.has_skip_conv:
            self.C3 = torch.nn.Conv2d(
                in_channels,
                out_channels,
                3,
                stride=stride,
                padding=1,
            )
            self.N3 = torch.nn.BatchNorm2d(num_features=out_channels)
        

    def forward(self, x):
        skip_x = x

        x = self.C1(x)
        x = self.N1(x)
        x = self.R1(x)
        x = self.C2(x)
        x = self.N2(x)

        if self.has_skip_conv:
            skip_x = self.C3(skip_x)
            skip_x = self.N3(skip_x)

        x = self.R2(x + skip_x)
        return x
        

class NonResidualBlock(torch.nn.Module):
    def __init__(self, in_channels, out_channels, stride):
        super().__init__()
        self.C1 = torch.nn.Conv2d(
            in_channels,
            out_channels,
            3,
            stride=stride,
            padding=1,
        )
        self.N1 = torch.nn.BatchNorm2d(num_features=out_channels)
        self.R1 = torch.nn.ReLU()
        self.C2 = torch.nn.Conv2d(out_channels, out_channels, 3, padding=1)
        self.N2 = torch.nn.BatchNorm2d(num_features=out_channels)
        self.R2 = torch.nn.ReLU()

    def forward(self, x):
        x = self.C1(x)
        x = self.N1(x)
        x = self.R1(x)
        x = self.C2(x)
        x = self.N2(x)
        x = self.R2(x)
        return x


def get_model(depth, block_type="ResidualBlock", base_width=16):
    if block_type == "ResidualBlock":
        block_factory = ResidualBlock
    elif block_type == "NonResidualBlock":
        block_factory = NonResidualBlock
    else:
        raise ValueError()

    # Input layers
    modules = [
        torch.nn.Conv2d(3, base_width, 3, padding=1),
        torch.nn.BatchNorm2d(base_width),
        torch.nn.ReLU(),
    ]

    # Blocks and stages (based off the configuration used in the ResNet paper)
    blocks_per_stage = (depth - 2) // 6
    assert depth == blocks_per_stage * 6 + 2
    in_channels = base_width
    out_channels = base_width
    for stage_idx in range(3):
        for block_idx in range(blocks_per_stage):
            stride = 2 if block_idx == 0 and stage_idx > 0 else 1
            modules.append(
                block_factory(
                    in_channels,
                    out_channels,
                    stride,
                )
            )
            in_channels = out_channels
        out_channels = out_channels * 2

    # Output layers
    modules.extend(
        [
            torch.nn.AdaptiveAvgPool2d(1),
            torch.nn.Flatten(),
            torch.nn.Linear(in_channels, 4),
        ]
    )

    model = torch.nn.Sequential(*modules)
    return model

def load_pretrained_model():
    model = get_model(32, "ResidualBlock", 16)
    import os 
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    model.load_state_dict(torch.load(current_dir + "/model1_state.pth"))
    model.eval()
    return model

def inference(model, image):
    with torch.no_grad():
        output = model(image)
        output = torch.nn.functional.softmax(output, dim=1)
        p, classe = torch.max(output, dim=1)
        p = p.item() * 100
        classe = classe.item()
        return output, p, classe

def prepare_img_for_inference(image):
    image = Image.open(image)

    transform = transforms.Compose([
        transforms.Resize((300, 300)), 
        transforms.ToTensor(),
    ])
    
    image = transform(image)
    image = image.unsqueeze(0)
    return image

def test():
    print("hello")
    return 