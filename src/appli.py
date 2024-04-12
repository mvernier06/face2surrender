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

    
# @app.route("/criminel", methods=['GET', 'POST'])
# def criminel():
#     if request.method == 'POST':
#         if request.content_type.startswith('application/json'):
#             data = request.json
#             if 'attributes' in data:
#                 selected_attributes = data['attributes']
#                 print("Attributs sélectionnés à partir d'AJAX:", selected_attributes)
#                 # Vous pouvez ici filtrer les images basées sur les attributs
#                 # images = filter_images_based_on_attributes(selected_attributes)
#                 # return jsonify({'success': True, 'images': images})  # Pour une réponse AJAX
#                 return render_template('criminel.html')  # Ou afficher une page avec des images   
#             elif 'selected_images' in data:
#                 selected_images = data['selected_images']
#                 specific_param = data.get('specific_param', 'default_value')
#                 print("Images sélectionnées pour le traitement:", selected_images)
#                 print("Paramètre spécifique:", specific_param)
#                 # Traitement des images ici
#                 # return jsonify({'success': True})  # Pour AJAX

#         return render_template('criminel.html')
    
#     return render_template('home.html')


# @app.route("/criminel", methods=['GET', 'POST'])
# def criminel():
#     if request.method == 'POST':
#         # Vérifie si les données viennent d'un formulaire standard
#         if request.content_type.startswith('application/x-www-form-urlencoded'):
#             selected_attributes = request.form.getlist('attributes')
#             print("Attributs sélectionnés à partir du formulaire:", selected_attributes)

#             # Filtrez vos images ici ou faites tout traitement nécessaire
#             #images = filter_images_based_on_attributes(selected_attributes)
#             return render_template('criminel.html')#, imgtmp=images)
        
#         # Vérifie si les données viennent d'une requête JSON (AJAX)
#         elif request.content_type.startswith('application/json'):
#             data = request.json
#             selected_images = data.get('selected_images', [])
#             specific_param = data.get('specific_param', 'default_value')
#             print("Images sélectionnées pour le traitement:", selected_images)
#             print("Paramètre spécifique:", specific_param)

#             # Faites ici le traitement nécessaire sur les images sélectionnées
#             #processed_images = process_images(selected_images, specific_param)
#             return render_template('criminel.html')#, imgtmp=processed_images)

#     # Si la méthode est GET ou autre chose, chargez simplement la page avec un formulaire initial
#     return render_template('criminel.html')


# @app.route("/criminel", methods=['GET', 'POST'])
# def criminel():
#     # si on a selectionné des images, on les traite dans cette partie
#     if flask.request.method == 'POST':
#         data = request.json
#         selected_images = data.get('selected_images', [])
#         specific_param = data.get('specific_param', 'default_value')

#         print(selected_images)
#         print(specific_param)

#         # ici il faudra envoyer les images selectionnée à l'algo génétique
#         # et récuperer 9 nouvelles images faites pas l'algo génétique

#         # Utilisez specific_param pour déterminer la fonction de chargement d'images à utiliser
#         if specific_param == 'value1':
#             images = loadtmp('tmp/img_align_celeba')
#         elif specific_param == 'value2':
#             images = loadtmp('tmp/img_align_celeba')
#         # etc.

#         return render_template('criminel.html', imgtmp=images)

#     images = loadtmp('tmp/img_align_celeba')
#     return render_template('criminel.html', imgtmp=images)

@app.route("/resultat", methods=['GET'])
def resultat():
    image=request.args['selected_image']
    print(image)
    #lien=image['src']
    return render_template('resultat.html', img=image )

@app.route("/traitement", methods=['POST'])
def traitement():
    data = request.json
    checkboxes = data.get('checkboxes', [])
    print(checkboxes)
    # Faites quelque chose avec checkboxes ici
    return redirect(url_for('criminel'))