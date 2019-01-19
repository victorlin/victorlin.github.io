from flask import Flask
app = Flask(__name__)

from flask import render_template

# from flask import request
# import pandas as pd
# from flask import jsonify
# from flask import abort


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/0/')
def zero():
    return render_template('0.html')

@app.route('/hello/<name>')
def hello1(name):
    return render_template('hello.html', name=name)


def hello2():
    pass
    # route: '/hello/'
    # what is the URL "?"
    # hint: https://stackoverflow.com/q/24892035/python-flask-how-to-get-parameters-from-a-url
