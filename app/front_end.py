import atexit
import time
from apscheduler.schedulers.background import BackgroundScheduler

from flask import render_template, abort, request, Blueprint
import pandas as pd

from .dataProcessing.predictionModel import predict
from .dataProcessing.gettingData import getDataFromJohnshopkinsGithub
from .dataProcessing.gettingData import WriteGrowthRates

frontEnd = Blueprint('frontEnd', __name__)

#update johnhopkinsdata
#then use this to update growth rates
def updateDaily():
    #getDataFromJohnshopkinsGithub("dataProcessing/PipelineIntermediates/CountryCasesFromHopkins.csv")
    #WriteGrowthRates("dataProcessing/PipelineIntermediates/CountryCasesFromHopkins.csv", "PipelineIntermediates/GrowthRates.csv")
    #TODO join these to into the static Data
    print("Updated: " + time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


scheduler = BackgroundScheduler()
scheduler.add_job(func=updateDaily, trigger="interval", hours=24)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


@frontEnd.route('/')
@frontEnd.route('/index')
def index():
    #getDataFromJohnshopkinsGithub("dataProcessing/PipelineIntermediates/CountryCasesFromHopkins.csv") habs nur hier hingetan, damit ich nicht 24h auf die Aktualisierung warten muss ;)
    return render_template("index.html")


@frontEnd.route('/parameter', methods=['GET'])
def parameter():
    try:
        df = pd.read_csv("dataProcessing/PipelineIntermediates/finalCleanDataCopyPasteBasic.csv")
        return df.to_csv()
    except OSError:
        abort(404)


@frontEnd.route('/graphs')
def graphs():
    try:
        open(r"dataProcessing/PipelineIntermediates/CountryCasesFromHopkins.csv", 'r')
    except OSError:
        print("error")
    try:
        df = pd.read_csv(r"dataProcessing/PipelineIntermediates/CountryCasesFromHopkins.csv")
        return df.to_csv()
    except OSError:
        abort(404)


@frontEnd.route('/getModel', methods=['GET', 'POST'])
def get_model():
    parameters = request.args.get('parameterList')
    param = str(parameters).split(',')
    try:
        print(predict(param))
        return predict(param)
    except OSError:
        abort(404)


@frontEnd.route('/finalCleanData')
def finalCleanData():
    try:
        df = pd.read_csv("dataProcessing/PipelineIntermediates/finalCleanDataCopyPasteBasic.csv")
        return df.to_csv()
    except OSError:
        abort(404)
