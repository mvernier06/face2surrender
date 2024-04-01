import flask
from flask import Flask
from flask import render_template, url_for
from gestion import loadtmp
from flask import request

app = Flask(__name__)

@app.route("/home")
def home():
    return render_template('home.html')



@app.route("/criminel", methods=['GET', 'POST'])
def criminel():
    if flask.request.method == 'POST':
        # Traitement de la sélection des images...
        selected_images = request.json.get('selected_images', [])
        print(selected_images)  # Affiche les noms des images sélectionnées dans la console Flask
    images = loadtmp('tmp/img_align_celeba')
    return render_template('criminel.html', imgtmp=images)
