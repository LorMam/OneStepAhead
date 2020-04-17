import atexit
import time

from app import app
from flask import render_template, abort, request
import pandas as pd

from .dataProcessing.predictionModel import predict
from apscheduler.schedulers.background import BackgroundScheduler


#TODO @Lorenz
#update johnhopkinsdata
def updateDaily():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


scheduler = BackgroundScheduler()
scheduler.add_job(func=updateDaily, trigger="interval", hours=24)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


@app.route('/')
@app.route('/index')
def index():
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
    print(predict(param))
    try:
        df = pd.read_csv("dataProcessing/savedModels/bestModel.csv")
        #run predict(Parameters) from predictionModel
        #print(df.to_csv())
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
