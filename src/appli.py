import flask
from flask import Flask
from flask import render_template
from gestion import loadtmp

app = Flask(__name__)

@app.route("/home")
def home():
    return render_template('home.html')



@app.route("/criminel", methods=['GET', 'POST'])
def criminel():
    images = loadtmp('tmp/img_align_celeba')
    return render_template('criminel.html', imgtmp=images)
