import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import csv


#from dataProcessing import inData didn't work
def inData(PathOrDF):
    if (isinstance(PathOrDF, str)):
        data = pd.read_csv(PathOrDF)
    else:
        data = PathOrDF
    return data


def predict(Parameters):
    # print("Predicted growth rate for",PredictionDataset["Values"],"is",gr)
    # https://medium.com/datadriveninvestor/a-simple-guide-to-creating-predictive-models-in-python-part-2a-aa86ece98f86
    # Tensor Flow guide
    # https://medium.com/datadriveninvestor/a-simple-guide-to-creating-predictive-models-in-python-part-2b-7be3afb5c557

    # c = ["China", "Japan",  "United Kingdom", "United States", "Italy", "Germany", "Algeria", "Egypt", "South Africa", "Brazil", "Chile", "Australia"]
    # p = ["Prosperity Index Health Score", "Population using at least basic drinking-water services (%)", "Human development index (HDI)", "Population. total (millions)", "Population. under age 5 (%)", "Population. ages 65 and older (%)", "yearly anual Temperature"]
    # coef = [-2.36494606e-03,  2.15270501e-03,  2.80678716e-01,  3.49335911e-05, -1.39790582e+00, -5.83476662e-01,  1.63075352e-03]
    # score = [0.8777857786441605]

    # PredictionDataset = pd.DataFrame({ "Indices": ["Prosperity Index Health Score", "Population using at least basic drinking-water services (%)", "Human development index (HDI)", "Population. total (millions)",
    #         "Population. under age 5 (%)", "Population. ages 65 and older (%)",  "yearly anual Temperature"],
    #                                   "Values": [3, 0.3, 6, 6, 0.1, 0.2, 20]})

    dataallpath = "PipelineIntermediates/finalCleanDataCopyPasteBasic.csv"  # TODO must be the same that Frontend gets

    df = pd.read_csv(dataallpath)
    x = Model(df["Country"].tolist(), Parameters)
    df = df.filter(np.append(Parameters, ["Country", "GrowthRate1"]))
    x.createRegressionModel(df, Parameters)

    out = x.toDF()
    print('funktion läuft')
    pritn(out.to_csv(header=False))
    return out.to_csv(header=False)


class Model():
    def __init__(self, countriesInModel, parametersInModel):  #
        self.countries = countriesInModel
        self.parameters = parametersInModel

    def toDF(self):
        out = pd.DataFrame({'': self.countries})
        out = pd.concat([out, pd.DataFrame({'1': self.parameters})], axis=1)
        out = pd.concat([out, pd.DataFrame({'2': self.coef})], axis=1)
        out = pd.concat([out, pd.DataFrame({'3': [self.score]})], 1)
        return out.transpose()

    def fromCsv(self, path):
        for index, line in enumerate(open(path)):
            if index == 0:
                self.countries = line
            elif index == 1:
                self.parameters = line
            elif index == 2:
                self.coef = line.split(',')
                self.coef = list(map(float, self.coef))  # list is obsolete if only use is in iterators
            elif index == 3:
                self.score = line
        # set countries, parameters coefs and score

    # dataset is a dataframe with columns ["Indices", "Values"]
    def predictGrowthRate(self, dataset):
        # check if parameters of dataset are the same order as model
        # calculate growth Rate 1
        out = 0
        for c, d in zip(self.coef, dataset["Values"]):
            out += c * d
        return out

    # Create the Regression Model
    # Input:
    # inputdata = csv file containing country information (UN and growth rates)
    # pvar = names of variables to be used in the model (list of strings)
    def createRegressionModel(self, inputdata, pvar):

        df_hd = inData(inputdata)

        # Determine the selected variables to construct the model
        selvars = []
        colid = 0
        for pname in df_hd.columns:
            if pname in pvar:
                print(pname)
                selvars.append(colid)
            colid += 1

        print("Number of selection variables =", len(selvars))
        x = df_hd.iloc[:, selvars]
        y = df_hd["GrowthRate1"]

        model = LinearRegression().fit(x, y)

        r_sq = model.score(x, y)
        self.score = r_sq

        self.coef = list(model.coef_)
        print("Number of coefficients =", len(self.coef))

        return
if __name__=="__main__":
    predict(["sbc"])