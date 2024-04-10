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
seuil_mutation = 1.64 # Une VA suivant N(0,1) déterminera si un élément d'un vecteur latent sera muté. Un zscore de 1.64 en valeur absolue comme seuil permettra de muter environ 10% des éléments
taux_croisement = 0.2
nombre_nouveaux_individus = 20  # Générer 20 vecteurs enfants 

# Fonction de croisement intercalé entre les vecteurs latents
def croisement_intercalé(parents):
    taille_segment = int(taille_vecteur * taux_croisement)
    if taille_segment < 1:
        return print("Les vecteurs latents sont de dimension inférieure au seuil taux de croisement * dimension.")
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
# S'il y a une corrélation spatiale dans le vecteur latent,le fait de recombiner des segments entier permet de maintenir la cohérence des caractéristiques visuelles dans les images générées.

# Fonction de mutation
def mutation(individus):
    for individu in individus:
        for i in range(taille_vecteur):
            if abs(np.random.rand()) > seuil_mutation:
                individu[i] += np.random.randn() * 0.1 # On atténue la variation pour produire des changements visuels légers. 
    return individus

# Fonction pour calculer la distance euclidienne
def comparer_parents_enfants(parents, enfants):
    distances_moyennes = []
    for enfant in enfants:
        distances = [np.linalg.norm(enfant - parent) for parent in parents]
        distance_moyenne = np.mean(distances)
        distances_moyennes.append(distance_moyenne)
    return distances_moyennes