from flask import Flask, render_template, jsonify
from flask import request
import os
import pprint as p
import webbrowser

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('/index.html', number= +33633829480)


def jules():
    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'##Force à ouvrir sur Google Chrome par défaut
    webbrowser.get(chrome_path).open("http://127.0.0.1:5000/")
    print("a fonctionné 2")
        