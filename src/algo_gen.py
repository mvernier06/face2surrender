import sklearn
import matplotlib.pyplot as plt
import torch
import vae
import os
import numpy as np

model = vae.load_model()
# Paramètres de l'algorithme génétique
taille_vecteur = 500 # dimension des vecteurs latents définis dans vae
seuil_mutation = 0.3 # Une VA suivant N(0,1) déterminera si un élément d'un vecteur latent sera muté. Un zscore de 1.64 en valeur absolue comme seuil permettra de muter environ 10% des éléments
taux_croisement = 0.5
nombre_nouveaux_individus = 20  # Générer 20 vecteurs enfants 

# Fonction de croisement intercalé entre les vecteurs latents qui simule une recombinaison
def croisement_intercalé(parents):
    taille_segment = int(taille_vecteur * taux_croisement)
    if taille_segment < 1:
        return print("Les vecteurs latents sont de dimension inférieure au seuil taux de croisement * dimension.")
    nouveaux_individus = []
    for i in range(nombre_nouveaux_individus):
        nouvel_individu = np.zeros(taille_vecteur)
        position_actuelle = np.random.randint(0, taille_vecteur - taille_segment + 1)
        for j, parent in enumerate(parents):
            fin_segment = position_actuelle + taille_segment
            if fin_segment > taille_vecteur:
                fin_segment = taille_vecteur
            segment = parent[position_actuelle:fin_segment]
            if len(segment) > 0: # Si le segment n'est pas vide
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

# def convert_to_tensor(parent):
#     if isinstance(parent, list) and all(isinstance(i, list) for i in parent):
#         return [torch.from_numpy(np.array(i)).clone() for i in parent]
#     elif isinstance(parent, list):
#         return [torch.from_numpy(np.array(i)).clone() for i in parent]
#     else:
#         return parent.clone()

# # Fonction pour calculer la distance euclidienne
# def comparer_parents_enfants(parents, enfants):
#     distances_moyennes = []
#     parents_copy = [convert_to_tensor(parent) for parent in parents]
#     enfants_copy = [enfant.copy() for enfant in enfants]
#     for enfant in enfants_copy:
#         distances = [np.linalg.norm(enfant - parent.numpy()) for parent in parents_copy]
#         distance_moyenne = np.mean(distances)
#         distances_moyennes.append(distance_moyenne)
#     return distances_moyennes

def convert_to_tensor(parent):
    if isinstance(parent, list):
        tensors = [torch.tensor(i) for i in parent if isinstance(i, (np.ndarray, list)) and i is not parent]
        return torch.stack(tensors) if tensors else None
    else:
        return parent.clone()

def comparer_parents_enfants(parents, enfants):
    distances_moyennes = []
    parents_copy = [convert_to_tensor(parent) for parent in parents]
    enfants_copy = [enfant.copy() for enfant in enfants]
    for enfant in enfants_copy:
        distances = [np.linalg.norm(enfant - parent.numpy()) for parent in parents_copy if parent is not None]
        distance_moyenne = np.mean(distances)
        distances_moyennes.append(distance_moyenne)
    return distances_moyennes

def algo_gen(vecteurs_parents): 
    for i, vecteur in enumerate(vecteurs_parents, start=1):
        print(f"Vecteur latent {i} : {vecteur}")
    # Application du croisement intercalé et mutation
    if len(vecteurs_parents)==1 : 
        vecteurs_parents.append(vecteurs_parents) # On réplique les vecteurs latents unique, pour croisement et mutation
    elif len(vecteurs_parents)==0 :
        return print("Aucun vecteur latent n'a pu être récupéré à partir des images sélectionnées.")
    nouveaux_individus = croisement_intercalé(vecteurs_parents) # À partir des parents, on produit 20 nouveaux individus
    print(f"Nouveaux individus:",nouveaux_individus)
    nouveaux_individus = mutation(nouveaux_individus) # Que l'on fait muter.
    # Calcul des distances moyennes et sélection des 9 enfants avec la plus petite distance moyenne
    distances_moyennes = comparer_parents_enfants(vecteurs_parents, nouveaux_individus)
    indices_selectionnés = np.argsort(distances_moyennes)[-9:]  # Indices des 9 plus grandes distances
    # Sélection des 9 enfants avec la plus petite distance moyenne afin de minimiser le risque de modifications 'outliers'. 
    indices_plus_grandes_distances = np.argsort(distances_moyennes)[-3:]  # Indices des 3 plus grandes distances
    indices_plus_petites_distances = np.argsort(distances_moyennes)[:3]  # Indices des 3 plus petites distances
    indices_selectionnes = np.concatenate((indices_plus_grandes_distances, indices_plus_petites_distances))
    indices_non_selectionnes = [i for i in range(len(nouveaux_individus)) if i not in indices_selectionnes]
    indices_aleatoires = np.random.choice(indices_non_selectionnes, 3, replace=False)  # Indices de 3 individus sélectionnés au hasard
    indices_selectionnes = np.concatenate((indices_selectionnes, indices_aleatoires))
    enfants_selectionnés = [nouveaux_individus[i].copy() for i in indices_selectionnes]
    print(enfants_selectionnés)
    return enfants_selectionnés

# # Affichage des vecteurs des enfants sélectionnés
# for i, enfant in enumerate(enfants_selectionnés, start=1):
#     print(f"Enfant sélectionné {i} : {enfant[:128]}")