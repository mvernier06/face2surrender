import flask
from flask import Flask
from flask import render_template, url_for
from vae import load_model
from gestion import loadtmp
from algo_gen import algo_gen
from gestion import selectionner_images_finale, images_to_latent_vectors_list, decode_and_save_images
from flask import request, redirect
from flask import request, render_template, jsonify,session
import os

app = Flask(__name__)

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/")
def root():
    return render_template('home.html')

@app.route("/criminel", methods=['GET', 'POST'])
def criminel():
    if request.method == 'POST':
        # Vérifie si les données viennent du formulaire d'attributs
        if 'attributes' in request.form:
            selected_attributes = request.form.getlist('attributes')
            #print("Attributs sélectionnés à partir du formulaire:", selected_attributes)
            # Filtrer les images basées sur les attributs sélectionnés
            images = selectionner_images_finale(selected_attributes)
            dossier_image='tmp/img_align_celeba'
            return render_template('criminel.html', imgtmp=images,dossier_image=dossier_image)

        # Vérifie si les données viennent d'une requête JSON (AJAX) pour les images sélectionnées
        elif request.json and 'selected_images' in request.json:
            selected_images = request.json['selected_images']
            print("Images sélectionnées pour le traitement:", selected_images)
            model=load_model()
            # Faites ici le traitement nécessaire sur les images sélectionnées
            if not selected_images[0].startswith('a'):
                if 'tmp/img_align_celeba' in selected_images[0]:
                    image_dir = os.path.dirname(os.path.realpath(__file__))
                else:
                    image_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/tmp/img_align_celeba')
                latent_vectors = images_to_latent_vectors_list(selected_images, image_dir, model, image_size=64)
                vecteurs_enfants=algo_gen(latent_vectors)
                dossier_image=decode_and_save_images(vecteurs_enfants, model, parent_uuid=None, output_dir='tmp/current')
                print(f"Dossier image à tester", dossier_image)
                images=loadtmp(dossier_image)
                images = [image['src'] for image in images]
                dossier_ref='tmp/current'
                print(f"VoilàX",images)
            else:
                dossier_uuid=None
                if len(selected_images)>=1:
                    dossier_uuid = selected_images[0].split('_')[1]
                    folder_name = next((folder for folder in os.listdir('tmp/current') if folder.startswith('a_') and dossier_uuid in folder), None)
                    print(f"Folder name {folder_name}")
                    if folder_name:                        
                        latent_vectors=images_to_latent_vectors_list(selected_images,os.path.join(os.path.dirname(os.path.realpath(__file__)),'static',folder_name), model,image_size=64)
                        vecteurs_enfants=algo_gen(latent_vectors)
                        dossier_image=decode_and_save_images(vecteurs_enfants, model, parent_uuid=dossier_uuid, output_dir='tmp/current')
                        images=loadtmp(dossier_image)
                        images = [image['src'] for image in images]
                        print(f"Voilà",images)
            return render_template('criminel.html', imgtmp=images,dossier_image=dossier_image)

        # Gestion des autres cas non prévus
        return jsonify(success=False, message="Invalid request or data not provided")

    # Si la méthode est GET, afficher simplement la page avec un formulaire initial
    return render_template('home.html')

@app.route("/resultat", methods=['GET'])
def resultat():
    image=request.args['selected_image']
    print(image)
    #lien=image['src']
    return render_template('resultat.html', img=image )
