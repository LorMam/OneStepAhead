import atexit
import time

from app import app
from flask import render_template, abort, request
import pandas as pd

from .dataProcessing.predictionModel import predict
from apscheduler.schedulers.background import BackgroundScheduler
from .dataProcessing.gettingData import getDataFromJohnshopkinsGithub


#TODO @Lorenz
#update johnhopkinsdata
def updateDaily():
    getDataFromJohnshopkinsGithub("dataProcessing/PipelineIntermediates/CountryCasesFromHopkins.csv")
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


scheduler = BackgroundScheduler()
scheduler.add_job(func=updateDaily, trigger="interval", hours=24)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


@app.route('/')
@app.route('/index')
def index():
    #getDataFromJohnshopkinsGithub("dataProcessing/PipelineIntermediates/CountryCasesFromHopkins.csv") habs nur hier hingetan, damit ich nicht 24h auf die Aktualisierung warten muss ;)
    return render_template("index.html")


@app.route('/parameter', methods=['GET'])
def parameter():
    try:
        df = pd.read_csv("dataProcessing/PipelineIntermediates/finalCleanDataCopyPasteBasic.csv")
        return df.to_csv()
    except OSError:
        abort(404)


@app.route('/graphs')
def graphs():
    try:
        df = pd.read_csv("dataProcessing/PipelineIntermediates/CountryCasesFromHopkins.csv")
        return df.to_csv()
    except OSError:
        abort(404)


@app.route('/getModel', methods=['GET', 'POST'])
def get_model():
    parameters = request.args.get('parameterList')
    param = str(parameters).split(',')
    try:
        print(predict(param))
        return predict(param)
    except OSError:
        abort(404)


@app.route('/finalCleanData')
def finalCleanData():
    try:
        df = pd.read_csv("dataProcessing/PipelineIntermediates/finalCleanDataCopyPasteBasic.csv")
        return df.to_csv()
    except OSError:
        abort(404)
