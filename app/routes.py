from app import app
from flask import render_template, send_from_directory, abort


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/parameter', methods=['GET'])
def parameter():
    return "Prosperity Index Health Score,Population using at least basic drinking-water services (%)," \
           "Human development index (HDI),Population. total (millions)Population. under age 5 (%),Population. ages 65 " \
           "and older (%),yearly anual Temperature "


@app.route('/graphs')
def graphs():
    try:
        return send_from_directory(app.config["CLIENT_CSV"], filename="../dataProcessing/PipelineIntermediates/CountryCasesFromHopkins.csv", as_attachment=True)
    except FileNotFoundError:
        abort(404)