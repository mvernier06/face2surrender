import os
import random
import io
# import torch
import numpy as np
# import base64
from PIL import Image
import tempfile
from io import BytesIO
# import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt



def loadtmp(folder_name):
    folder_path = os.path.join('static', folder_name)  # Chemin absolu vers le dossier dans 'static'
    try:
        if not os.path.isdir(folder_path):
            print(f"Le dossier '{folder_path}' n'existe pas ou ne peut pas être lu.")
            return []

        image_files = os.listdir(folder_path)

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
    


    return random.sample(loaded_sample_images_np, 9)
