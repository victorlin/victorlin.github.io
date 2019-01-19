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

# what's my route?
def zero():
    pass
    # template: 0.html
