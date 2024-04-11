import os
import random

def loadtmp(folder_name):
    folder_path = os.path.join('static', folder_name)  # Chemin absolu vers le dossier dans 'static'
    try:
        if not os.path.isdir(folder_path):
            print(f"Le dossier '{folder_path}' n'existe pas ou ne peut pas être lu.")
            return []

        image_files = os.listdir(folder_path)
        print(image_files)
        # Construit la liste des images avec chemin d'accès relatif pour 'url_for'
        images = [
            {
                "src": os.path.join(folder_name, file),  # Chemin relatif adapté pour 'url_for'
                "alt": f"Description de {file}"
            }
            for file in image_files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
        ]
        return random.sample(images,9)

    except Exception as e:
        print(f"Une erreur est survenue lors du chargement des images du dossier '{folder_path}': {e}")
        return []

def load_attributes(filepath):
    """
    Charge les attributs des images depuis un fichier.
    """
    with open(filepath, 'r') as file:
        lines = file.readlines()
    
    # La première ligne contient le nombre d'images, on l'ignore ici
    # La deuxième ligne contient les noms des attributs
    attributes_names = lines[1].strip().split()
    
    # Créer un dictionnaire pour stocker les attributs de chaque image
    images_attributes = {}
    
    # Parcourir les lignes restantes qui contiennent les données d'attributs
    for line in lines[2:]:
        parts = line.strip().split()
        image_name = parts[0]
        attributes_values = [int(x) for x in parts[1:]]
        images_attributes[image_name] = dict(zip(attributes_names, attributes_values))
    
    return images_attributes

def filter_images_by_attributes(images_attributes, desired_attributes):
    """
    Filtre les images basées sur des attributs désirés.
    """
    filtered_images = []
    for image_name, attributes in images_attributes.items():
        # Vérifier si l'image correspond aux attributs désirés
        match = all(attributes[attr] == val for attr, val in desired_attributes.items())
        if match:
            filtered_images.append(image_name)
    
    return filtered_images

# Exemple d'utilisation
attributes_filepath = '/Users/thimotespitz/Downloads/list_attr_celeba.txt'
images_attributes = load_attributes(attributes_filepath)

# Disons que vous voulez des images où "Smiling" = 1 et "Male" = -1
desired_attributes = {"Smiling": 1, "Male": -1}
filtered_images = filter_images_by_attributes(images_attributes, desired_attributes)
print(filtered_images)
# Maintenant, filtered_images contient les noms des images qui correspondent aux attributs désirés


import os

def filter_existing_images(filtered_images, existing_files):
 # Filtrer pour ne conserver que les images qui sont à la fois dans filtered_images et existing_files
    existing_filtered_images = [img for img in filtered_images if img in existing_files]
    return existing_filtered_images

# Exemple d'utilisation
folder_path = 'chemin/vers/votre/dossier/images'
# Supposons que filtered_images soit la liste des noms d'images filtrées par attributs
# Utilisez la fonction filter_images_by_attributes pour obtenir cette liste
existing_filtered_images = filter_existing_images(filtered_images, folder_path)

# Maintenant, existing_filtered_images contient les noms des images qui correspondent aux attributs désirés
# et qui existent physiquement dans le dossier spécifié.



import torch
from torchvision import transforms
from PIL import Image
import os

def images_to_latent_vectors_list(image_names, folder_path, model, image_size=64):
    """
    Charge des images, les transforme sans normalisation, et utilise un modèle VAE pour obtenir les vecteurs latents,
    renvoyant une liste de vecteurs latents.
    
    Parameters:
    - image_names: Liste des noms des fichiers d'images à charger.
    - folder_path: Chemin vers le dossier contenant les images.
    - model: Modèle VAE pré-entraîné à utiliser pour encoder les images.
    - image_size: Taille à laquelle les images doivent être redimensionnées.
    
    Returns:
    - Liste contenant les vecteurs latents des images sous forme de tenseurs.
    """
    model.eval()  # Mettre le modèle en mode évaluation
    
    # Définir les transformations à appliquer aux images
    transform = transforms.Compose([
        transforms.Resize((image_size, image_size)),  # Redimensionner les images
        transforms.ToTensor(),                        # Convertir les images en tenseurs
    ])
    
    latent_vectors = []  # Pour stocker les vecteurs latents en tant que liste
    
    for image_name in image_names:
        # Charger et transformer l'image
        image_path = os.path.join(folder_path, image_name)
        image = Image.open(image_path).convert('RGB')
        image = transform(image).unsqueeze(0)  # Appliquer la transformation et ajouter une dimension de batch
        
        # Passer l'image à travers le modèle pour obtenir mu et logvar
        with torch.no_grad():  # Pas besoin de calculer les gradients
            mu, logvar = model.encode(image)
            latent_vector = model.reparameterize(mu, logvar)
            latent_vectors.append(latent_vector.squeeze(0))  # Supprimer la dimension de batch et ajouter à la liste
    
    return latent_vectors

import torch
import os
import uuid
from torchvision.utils import save_image
from PIL import Image

def decode_and_save_images(latent_vectors, model, parent_uuid=None, output_dir='tmp/current'):
    """
    Décode les vecteurs latents en images, et enregistre les images en format .jpg.
    
    Parameters:
    - latent_vectors: Liste de vecteurs latents à décoder.
    - model: Le modèle VAE pré-entraîné pour le décodage.
    - parent_uuid: UUID du parent. Si None, utilise 'celeba' pour les images initiales.
    - output_dir: Le dossier de base où les images seront enregistrées.
    """
    model.eval()  # Mettre le modèle en mode évaluation
    
    # Générer un UUID unique pour cette opération
    operation_uuid = str(uuid.uuid4())
    
    # Déterminer le nom du dossier basé sur l'UUID du parent
    if parent_uuid is None:
        parent_name = 'celeba'
    else:
        parent_name = parent_uuid
    
    # Créer le chemin du dossier pour sauvegarder les images
    save_path = os.path.join(output_dir, f"{operation_uuid}_{parent_name}")
    os.makedirs(save_path, exist_ok=True)
    
    # Boucle sur chaque vecteur latent
    for i, latent_vector in enumerate(latent_vectors, start=1):
        # Décoder le vecteur latent en image
        with torch.no_grad():
            decoded_image = model.decode(latent_vector.unsqueeze(0))
        
        # Convertir le tenseur en image PIL pour sauvegarde en format .jpg
        image = decoded_image.squeeze(0).detach().cpu()  # Supprimer la dimension de batch et déplacer en mémoire CPU
        image = transforms.ToPILImage()(image)
        
        # Construire le chemin de l'image et sauvegarder
        image_path = os.path.join(save_path, f"{operation_uuid}_{i}.jpg")
        image.save(image_path, 'JPEG')

# Exemple d'utilisation
# Présumant que vous avez une liste de vecteurs latents `latent_vectors` et un modèle `model_780`
# decode_and_save_images(latent_vectors, model_780, parent_uuid="exemple_parent_uuid")
