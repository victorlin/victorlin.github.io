from flask import Flask
app = Flask(__name__)

from flask import render_template

from flask import request
import pandas as pd
from flask import jsonify
from flask import abort


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/0/')
def zero():
    return render_template('0.html')

@app.route('/hello/<name>')
def hello1(name):
    return render_template('hello.html', name=name)

@app.route('/hello/')
def hello2():
    name = request.args.get('name')
    return render_template('hello.html', name=name)

@app.route('/stocks/<stock>')
def api_stock(stock):
    data = pd.read_csv('data/individual_stocks_5yr/{}_data.csv'.format(stock))
    col = request.args.get('column')
    if col not in data.columns:
        return abort(400, 'Invalid or unspecified column.')
    return jsonify(list(data[col]))
