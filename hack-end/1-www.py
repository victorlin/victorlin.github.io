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


def hello1(name=None):
    pass
    # route: '/hello/<name>'
    # template: hello.html
    # hint: http://flask.pocoo.org/docs/1.0/api/#flask.render_template
        # context: name=name
