import sklearn
import matplotlib.pyplot as plt
import torch

# Charger le modèle
import vae
input_channels = 3
latent_dim = 500
model_780 = vae.VAE(input_channels, latent_dim)
model_780.load_state_dict(torch.load('model_780.pth'))