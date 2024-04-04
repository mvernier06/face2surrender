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
import torch.nn.functional as F
import dataset
import vae


# Define the root directory where CelebA dataset is stored
celeba_root = '../data/img_align_celeba'
annotations_file = '../data/list_attr_celeba.txt'

# Define the transformations to be applied to the images
transform = transforms.Compose([
    transforms.Resize((64, 64)),  # Resize images to 64x64
    transforms.ToTensor(),         # Convert images to tensors
])

# Create an instance of CelebADataset
celeba_dataset = dataset.CelebADataset(root_dir=celeba_root, annotations_file=annotations_file, transform=transform)

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
    
    
# Parameters
# Define the number of dimensions for the latent space and the training parameters
latent_dim = 500
epochs = 780
batch_size = 32
learning_rate = 1e-3
input_channels=3

# Initialize the model
model = vae.VAE(input_channels=3, latent_dim=latent_dim)  # Assuming 3 input channels for RGB images

# Define optimizer
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

#dividing into subset because celebA is too big
dataset_size = len(celeba_dataset)
subset_size = 2000  # Specify the desired size of the subset

# Randomly sample indices for the subset
indices = torch.randperm(dataset_size)[:subset_size]

# Create a subset of the CelebA dataset
celeba_subset = Subset(celeba_dataset, indices)

# Create a DataLoader for the subset
batch_size = 32
subset_loader = DataLoader(celeba_subset, batch_size=batch_size, shuffle=True)



#TRAINING
# Training loop
for epoch in range(epochs):
    total_loss = 0
    for batch_images, batch_attributes in subset_loader:
        optimizer.zero_grad()
        
        # Forward pass
        reconstructed, mu, logvar = model(batch_images, batch_attributes)  # Pass both images and attributes
        
        # Compute the VAE loss
        loss = vae_loss(reconstructed, batch_images, mu, logvar)
        
        # Backpropagation
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
    
    # Print epoch loss
    average_loss = total_loss / len(subset_loader.dataset)
    print(f"Epoch [{epoch+1}/{epochs}], Loss: {average_loss}")


# Function to display images
def show_images(images, title):
    fig, axes = plt.subplots(1, len(images), figsize=(10, 5))
    for ax, img in zip(axes, images):
        ax.imshow(np.transpose(img.detach().numpy(), (1, 2, 0)))
        ax.axis('off')
    plt.suptitle(title)
    plt.show()

# Sample some images from the dataset
sample_images, _ = next(iter(subset_loader))

# Display original images
show_images(sample_images[:5], title='Original Images')

# Pass the images through the VAE
# Assuming sample_images and sample_attributes are your image and attribute data

reconstructed_images, mu, logvar = model(sample_images,_ )


# Display reconstructed images
show_images(reconstructed_images[:5], title='Reconstructed Images')



# Save the model
torch.save(model.state_dict(), 'model_780.pth')

# Save the training subset 
torch.save(subset_loader, 'subset_780.pt')