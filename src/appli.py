import flask
from flask import Flask
from flask import render_template, url_for
from gestion import loadtmp
from flask import request, redirect

app = Flask(__name__)

@app.route("/home")
def home():
    return render_template('home.html')


from flask import request, render_template, jsonify

@app.route("/criminel", methods=['GET', 'POST'])
def criminel():
    if request.method == 'POST':
        # Vérifie si les données viennent d'un formulaire standard
        if request.content_type.startswith('application/x-www-form-urlencoded'):
            # Traite les données de formulaire standard
            selected_attributes = request.form.getlist('attributes')
            print("Attributs sélectionnés à partir du formulaire:", selected_attributes)

            # Filtrez vos images ici ou faites tout traitement nécessaire
            #images = filter_images_based_on_attributes(selected_attributes)
            return render_template('criminel.html')#, imgtmp=images)
        
        # Vérifie si les données viennent d'une requête JSON (AJAX)
        elif request.content_type.startswith('application/json'):
            data = request.json
            selected_images = data.get('selected_images', [])
            specific_param = data.get('specific_param', 'default_value')
            print("Images sélectionnées pour le traitement:", selected_images)
            print("Paramètre spécifique:", specific_param)

            # Faites ici le traitement nécessaire sur les images sélectionnées
            #processed_images = process_images(selected_images, specific_param)
            return render_template('criminel.html')#, imgtmp=processed_images)

    # Si la méthode est GET ou autre chose, chargez simplement la page avec un formulaire initial
    return render_template('criminel.html')


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