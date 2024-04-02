import os
from PIL import Image
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms 
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np
from torch.utils.data import Subset, SubsetRandomSampler


class CelebADataset(Dataset):
    def __init__(self, root_dir, annotations_file, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.image_filenames = os.listdir(root_dir)
        self.attributes = self.parse_attributes(annotations_file)

    def __len__(self):
        return len(self.image_filenames)

    def __getitem__(self, idx):
        img_name = os.path.join(self.root_dir, self.image_filenames[idx])
        image = Image.open(img_name)
        if self.transform:
            image = self.transform(image)

        # Get attributes for the current image and convert to tensor
        attr = torch.tensor(self.attributes[self.image_filenames[idx]], dtype=torch.float32)

        return image, attr

    def parse_attributes(self, annotations_file):
        attributes = {}
        with open(annotations_file, 'r') as f:
            lines = f.readlines()
            header = lines[1].strip().split()  # Skip header line
            for line in lines[2:]:
                parts = line.strip().split()
                filename = parts[0]
                attr = [int(x) for x in parts[1:]]
                attributes[filename] = attr
        return attributes


# Define the root directory where CelebA dataset is stored
celeba_root = '../data/img_align_celeba'
annotations_file = '../data/list_attr_celeba.txt'

# Define the transformations to be applied to the images
transform = transforms.Compose([
    transforms.Resize((64, 64)),  # Resize images to 64x64
    transforms.ToTensor(),         # Convert images to tensors
])

# Create an instance of CelebADataset
celeba_dataset = CelebADataset(root_dir=celeba_root, annotations_file=annotations_file, transform=transform)

# Create a DataLoader for batching and shuffling the data
batch_size = 32
dataloader = DataLoader(celeba_dataset, batch_size=batch_size, shuffle=True)

# Now you can iterate over the DataLoader
for batch_images, batch_attributes in dataloader:
    # Process each batch here
    print("Batch size:", batch_images.size(0))
    print("Shape of batch image tensor:", batch_images.shape)  # Example: torch.Size([32, 3, 64, 64]) for RGB images
    print("Shape of batch attribute tensor:", batch_attributes.shape)  # Example: torch.Size([32, num_attributes])
    break  # Break after printing the first batch