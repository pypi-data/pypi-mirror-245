"""
Image dataset classes.
"""

# Imports ---------------------------------------------------------------------

import os
import numpy as np
import pandas as pd
import torch

from torch.utils.data import Dataset
from torchvision.io import read_image
from torchvision.io import ImageReadMode

# Errors ----------------------------------------------------------------------

class ImageReadError(Exception):
    pass

# ImagePathDataset ------------------------------------------------------------

class ImagePathDataset(Dataset):

    def __init__(
        self, 
        data, 
        read_mode=None,
        transform=None, 
        target_transform=None):

        self.data = data.to_numpy()
        self.transform = transform
        self.target_transform = target_transform
        self.read_mode = self.get_read_mode(read_mode)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):

        try:

            image_path = self.data[idx, 0]
            image = read_image(image_path, self.read_mode).type(torch.float32)
            labels = self.get_labels(idx)
                            
            if self.transform:
                image = self.transform(image)
            
            if self.target_transform:
                labels = self.target_transform(labels)

            return image, labels

        except Exception as error:
            msg = f"Error reading {image_path}: {error}"
            raise ImageReadError(msg)

    def get_labels(self, idx):
        return torch.tensor(
            self.data[idx, 1:].astype(np.float32), 
            dtype=torch.float32)

    @classmethod
    def get_read_mode(cls, read_mode):
        if read_mode == "GRAY":
            read_mode = ImageReadMode.GRAY
        elif read_mode == "GRAY_ALPHA":
            read_mode = ImageReadMode.GRAY_ALPHA
        elif read_mode == "RGB":
            read_mode = ImageReadMode.RGB
        elif read_mode == "RGB_ALPHA":
            read_mode = ImageReadMode.RGB_ALPHA
        else:
            read_mode = ImageReadMode.UNCHANGED
        return read_mode

    @classmethod
    def create_unlabelled_dataset(
        cls,
        dir_path,
        read_mode=None,
        transform=None,
        skip_files=[],
        skip_unreadable=False):

        # Add unreadable files to skip_files
        if skip_unreadable == True:
            skip_files += cls.find_unreadable_images(
                dir_path=dir_path, 
                read_mode=read_mode)
        
        # Create a dataframe of paths to images
        files = []
        for f in os.listdir(dir_path):
            if not f.startswith(".") and not f in skip_files:
                files.append(os.path.join(dir_path, f))
        data = pd.DataFrame({"path": files, "label": -1})

        # Create and return a dataset
        return cls(
            data, 
            read_mode=read_mode,
            transform=transform)

    @classmethod
    def find_unreadable_images(
        cls, 
        dir_path, 
        read_mode=None):
        
        read_mode = cls.get_read_mode(read_mode)
        unreadable_images = []
        for f in os.listdir(dir_path):
            if not f.startswith("."):
                try:
                    image_path = os.path.join(dir_path, f)
                    _ = read_image(image_path, read_mode)
                except Exception as error:
                    unreadable_images.append(f)
                    continue
        return unreadable_images

# MulticlassImagePathDataset --------------------------------------------------

class MulticlassImagePathDataset(ImagePathDataset):
    
    def __init__(
        self, 
        data, 
        read_mode=None,
        transform=None, 
        target_transform=None):

        super().__init__(
            data, 
            read_mode,
            transform, 
            target_transform)

    def get_labels(self, idx):
        return self.data.iloc[idx, 1]
