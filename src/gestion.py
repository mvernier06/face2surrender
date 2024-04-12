import torch
from torchvision import transforms
from PIL import Image
import os
import random
import json
import uuid
from torchvision.utils import save_image

current_directory = os.path.dirname(os.path.realpath(__file__))

def loadtmp(folder_name):
    folder_path = os.path.join('static', folder_name)  # Chemin relatif vers le dossier dans 'static'
    try:
        if not os.path.isdir(folder_path):
            print(f"Le dossier '{folder_path}' n'existe pas ou ne peut pas être lu.")
            return []

        image_files = os.listdir(folder_path)
        #print(image_files)
        # Construit la liste des images avec chemin d'accès relatif pour 'url_for'
        images = [
            {
                "src": os.path.join(folder_name, file),  # Chemin relatif adapté pour 'url_for'
                "alt": f"Description de {file}"
            }
            for file in image_files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
        ]
        return random.sample(images,9) # Retourne une liste aléatoire de 9 images

    except Exception as e:
        print(f"Une erreur est survenue lors du chargement des images du dossier '{folder_path}': {e}")
        return []


def charger_images_par_attribut(chemin_fichier):
    with open(chemin_fichier, 'r') as fichier:
        images_par_attribut = json.load(fichier)
    return images_par_attribut

images_par_attribut = charger_images_par_attribut(os.path.join(current_directory,'static/attribute_images.json'))

def intersection_des_listes(listes):
    if not listes:
        return []
    ensemble_resultant = set(listes[0])
    for liste in listes[1:]:
        ensemble_resultant.intersection_update(liste)
    return list(ensemble_resultant)

def selectionner_images_finale(attributs_choisis):
    images_par_attribut = charger_images_par_attribut(os.path.join(current_directory,'static/attribute_images.json'))
    toutes_images = os.listdir(os.path.join(current_directory,'static/tmp/img_align_celeba'))
    if not attributs_choisis:
        return random.sample(toutes_images, min(9, len(toutes_images)))

    listes = [images_par_attribut[attr] for attr in attributs_choisis if attr in images_par_attribut]
    images_finale = intersection_des_listes(listes)

    if len(images_finale) < 9:
        images_manquantes = set(toutes_images) - set(images_finale)
        images_finale.extend(random.sample(list(images_manquantes), min(9 - len(images_finale), len(images_manquantes))))

    return random.sample(images_finale, min(9, len(images_finale)))


def load_attributes(filepath):
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
    filtered_images = []
    for image_name, attributes in images_attributes.items():
        # Vérifier si l'image correspond aux attributs désirés
        match = all(attributes[attr] == val for attr, val in desired_attributes.items())
        if match:
            filtered_images.append(image_name)  
    return filtered_images

def filter_existing_images(filtered_images, existing_files):
 # Filtrer pour ne conserver que les images qui sont à la fois dans filtered_images et existing_files
    existing_files_set = set(existing_files)
    existing_filtered_images = [img for img in filtered_images if img in existing_files_set]
    return existing_filtered_images

def get_filtered_images(desired_attributes, attributes_filepath, folder_path):
    """
    Retourne une liste de noms d'images présentes dans le dossier spécifié et qui correspondent aux attributs désirés.
    
    Parameters:
    - desired_attributes: Dictionnaire des attributs désirés avec leurs valeurs.
    - attributes_filepath: Chemin vers le fichier contenant les attributs des images.
    - folder_name: Nom du dossier contenant les images.
    
    Returns:
    - Liste des noms d'images filtrées et existantes dans le dossier spécifié.
    """
    # Charger les attributs des images depuis le fichier
    images_attributes = load_attributes(attributes_filepath)    
    # Filtrer les images basées sur des attributs désirés
    filtered_images = filter_images_by_attributes(images_attributes, desired_attributes)    
    try:
        existing_files = os.listdir(folder_path)
    except Exception as e:
        print(f"Une erreur est survenue lors de la tentative de lecture du dossier '{folder_path}': {e}")
        return []
    
    # Filtrer pour ne conserver que les images qui sont à la fois dans filtered_images et existing_files
    existing_filtered_images = filter_existing_images(filtered_images, existing_files)
    
    return existing_filtered_images


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
    if isinstance(image_names, dict): # Si un dictionnaire est fourni, utiliser les clés comme noms d'images
        image_names = list(image_names.keys())
    for image in image_names:
        # Charger et transformer l'image
        if '/tmp/img_align_celeba' in folder_path and 'tmp/current/' in image:
            image_path = os.path.join(folder_path.replace('/tmp/img_align_celeba', '/tmp/current'), image.split('tmp/current/')[1])
        else:
            image_path = os.path.join(folder_path, image)
        print(f"Chemin de l'image pb",folder_path, image)
        image = Image.open(image_path).convert('RGB')
        image = transform(image).unsqueeze(0)  # Appliquer la transformation et ajouter une dimension de batch
        
        # Passer l'image à travers le modèle pour obtenir mu et logvar
        with torch.no_grad():  # Pas besoin de calculer les gradients
            mu, logvar = model.encode(image)
            latent_vector = model.reparameterize(mu, logvar)
            latent_vectors.append(latent_vector.squeeze(0))  # Supprimer la dimension de batch et ajouter à la liste
    print(f"Vecteurs sortis encodeur",latent_vectors)
    return latent_vectors

def decode_and_save_images(latent_vectors, model, parent_uuid=None, output_dir='tmp/current'):
    """
    Décode les vecteurs latents en images, et enregistre les images en format .jpg.
    
    Parameters:
    - latent_vectors: Liste de vecteurs latents à décoder.
    - model: Le modèle VAE pré-entraîné pour le décodage.
    - parent_uuid: UUID du parent. Si None, utilise 'celeba' pour les images initiales.
    - output_dir: Le dossier de base où les images seront enregistrées.
    
    Returns:
    - Le nom du dossier où les images ont été enregistrées.
    """
    model.eval()  # Mettre le modèle en mode évaluation
    
    # Générer un UUID unique pour cette opération
    operation_uuid = str(uuid.uuid4())
    
    # Déterminer le nom du dossier basé sur l'UUID du parent
    if parent_uuid is None:
        parent_name = 'celeba'
    else:
        parent_name = parent_uuid
    
    # Vérifie si 'tmp/current' ou 'tmp/celeba' est déjà dans 'output_dir'
    if 'tmp/current' in output_dir or 'tmp/celeba' in output_dir:
        # Si c'est le cas, utilisez simplement 'output_dir' comme chemin du dossier
        save_path_rel = os.path.join(output_dir, f"a_{operation_uuid}_{parent_name}")
    else:
        # Sinon, ajoutez 'tmp/current' ou 'tmp/celeba' au début de 'output_dir' en fonction de 'parent_name'
        save_path_rel = os.path.join(output_dir, f"tmp/{parent_name}", f"a_{operation_uuid}_{parent_name}")

    save_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static', save_path_rel)
    os.makedirs(save_path, exist_ok=True)
    
    # Boucle sur chaque vecteur latent
    for i, latent_vector in enumerate(latent_vectors, start=1):
        # Décoder le vecteur latent en image
        with torch.no_grad():
            latent_vector = torch.from_numpy(latent_vector).unsqueeze(0)
            decoded_image = model.decode(latent_vector.type_as(model.decoder_fc.weight))
        
        # Convertir le tenseur en image PIL pour sauvegarde en format .jpg
        image = decoded_image.squeeze(0).detach().cpu()  # Supprimer la dimension de batch et déplacer en mémoire CPU
        image = transforms.ToPILImage()(image)
        
        # Construire le chemin de l'image et sauvegarder
        image_path = os.path.join(save_path, f"a_{operation_uuid}_{i}.jpg")
        image.save(image_path, 'JPEG')
    print(f"Oui oui", save_path_rel)
    return save_path_rel

