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
    # si on a selectionné des images, on les traite dans cette partie
    if flask.request.method == 'POST':
        selected_images = request.json.get('selected_images', [])
        
        print(selected_images)
        # ici il faudra envoyer les images selectionnée à l'algo génétique
        # et récuperer 9 nouvelles images faites pas l'algo génétique
        images = loadtmp('tmp/img_align_celeba')
        return render_template('criminel.html', imgtmp=images)
    images = loadtmp('tmp/img_align_celeba')
    return render_template('criminel.html', imgtmp=images)

@app.route("/resultat", methods=['GET'])
def resultat():
    image=request.args['selected_image']
    print(image)
    #lien=image['src']
    return render_template('resultat.html', img=image )
