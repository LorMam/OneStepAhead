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
    countriesForModel = ["China", "Japan", "United Kingdom", "United States", "Italy", "Germany", "Algeria", "Egypt",
                    "South Africa", "Brazil", "Chile"]#, "Australia"] #TODO must be somehow changeable?

    dataallpath = "dataProcessing/PipelineIntermediates/finalCleanDataCopyPasteBasic.csv"  # TODO must be the same that Frontend gets

    df = pd.read_csv(dataallpath)

    #only use selected countries for making the prediction model
    mask = df.Country.isin(countriesForModel)
    df=df[mask]

    x = Model(countriesForModel, Parameters)
    x.createRegressionModel(df, Parameters)

    out = x.toDF()
    print('funktion läuft')
    print(out.to_csv(header=False, index=False))
    return out.to_csv(header=False, index=False)


class Model():
    def __init__(self, countriesInModel, parametersInModel):  #
        self.countries = countriesInModel
        self.parameters = parametersInModel

    def toDF(self):
        out = pd.DataFrame({'0': self.countries})
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