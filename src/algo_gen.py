import sklearn
import matplotlib.pyplot as plt
import torch
import vae
import os
import numpy as np
from vae import latent_dim

model = vae.load_model()

# Paramètres de l'algorithme génétique
taille_vecteur = 500 # dimension des vecteurs latents définis dans vae
taux_mutation = 0.3
taux_croisement = 0.2
nombre_nouveaux_individus = 20  # Générer 20 vecteurs enfants 

# Fonction de croisement intercalé entre les vecteurs latents
def croisement_intercalé(parents):
    taille_segment = int(taille_vecteur * taux_croisement)
    if taille_segment < 1:
        return print("Les vecteurs latents n'ont pas pu être lus ou sont de dimension inférieure au seuil taux de croisement * dimension.")
    nouveaux_individus = []
    for i in range(nombre_nouveaux_individus):
        nouvel_individu = np.zeros(taille_vecteur)
        position_actuelle = 0
        for j, parent in enumerate(parents):
            fin_segment = position_actuelle + taille_segment
            if fin_segment > taille_vecteur:
                fin_segment = taille_vecteur
            segment = parent[position_actuelle:fin_segment]
            nouvel_individu[position_actuelle:fin_segment] = segment
            position_actuelle += taille_segment
            if position_actuelle >= taille_vecteur:
                break
        nouveaux_individus.append(nouvel_individu)
    return nouveaux_individus