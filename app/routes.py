from app import app
from flask import render_template, abort, request
import pandas as pd


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/parameter', methods=['GET'])
def parameter():
    try:
        df = pd.read_csv("../dataProcessing/PipelineIntermediates/finalCleanDataCopyPasteBasic.csv")
        return df.to_csv()
    except OSError:
        abort(404)


@app.route('/graphs')
def graphs():
    try:
        df = pd.read_csv("../dataProcessing/PipelineIntermediates/CountryCasesFromHopkins.csv")
        return df.to_csv()
    except OSError:
        abort(404)


@app.route('/getModel')
def get_model():
    print(request.args.get('parameterList'))
    try:
        df = pd.read_csv("../dataProcessing/savedModels/bestModel.csv")
        return df.to_csv()
    except OSError:
        abort(404)


# TODO @Lorenz
# parameterliste -> bestModel.csv
