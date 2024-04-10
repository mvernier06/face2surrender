import sklearn
import matplotlib.pyplot as plt
import torch
import vae
import os
import numpy

model = vae.load_model()

# Paramètres de l'algorithme génétique
taille_vecteur = 128
taux_mutation = 0.3
nombre_nouveaux_individus = 20  # Générer 20 vecteurs enfants 