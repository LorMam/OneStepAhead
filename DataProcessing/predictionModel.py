import pandas as pd
from dataProcessing import outToCsv


class predictionModel():
    def __init__(self, countriesInModel, parametersInModel, coefficients, score):
        self.countries = countriesInModel
        self.parameters = parametersInModel
        self.coef = coefficients
        self.score = score

    def toCsv(self, path):
        out = []
        out.append(self.countries)
        out.append(self.parameters)
        out.append(self.coef)
        out.append(self.score)
        outToCsv(path, out)

    def fromCsv(self, path):
        for index, line in enumerate(open(path)):
            if index == 0:
                self.countries = line
            elif index == 1:
                self.parameters = line
            elif index == 2:
                self.coef = line.split(',')
                self.coef = list(map(float, self.coef)) # list is obsolete if only use is in iterators
            elif index == 3:
                self.score = line
        #set countries, parameters coefs and score

    #dataset is a dataframe with columns ["Indices", "Values"]
    def runModelGR1(self, dataset):
        #check if parameters of dataset are the same order as model
        #calculate growth Rate 1
        out = 0
        for c, d in zip(self.coef, dataset["Values"]):
            out += c*d
        return out

    #must be different from GR1 if something must be done with Date of Intervention?
    #but how does this come in to effect?
    def runModelGR2(self, dataset):
        #
        #return table with [country, GR2]
        return 'dummy'
def main():
    c = ["China", "Japan",  "United Kingdom", "United States", "Italy", "Germany", "Algeria", "Egypt", "Burkina Faso", "South Africa", "Brazil", "Chile", "Australia"]
    p = ["Prosperity Index Health Score", "Population using at least basic drinking-water services (%)", "Human development index (HDI)", "Population. total (millions)"
             "Population. under age 5 (%)", "Population. ages 65 and older (%)", "yearly anual Temperature"]
    coef = [-2.36494606e-03,  2.15270501e-03,  2.80678716e-01,  3.49335911e-05, -1.39790582e+00, -5.83476662e-01,  1.63075352e-03]
    score = [0.8777857786441605]

    PredictionDataset = pd.DataFrame({ "Indices": ["Prosperity Index Health Score", "Population using at least basic drinking-water services (%)", "Human development index (HDI)", "Population. total (millions)",
             "Population. under age 5 (%)", "Population. ages 65 and older (%)",  "yearly anual Temperature"],
                                       "Values": [3, 0.3, 6, 6, 0.1, 0.2, 20]})

    x = predictionModel(c, p, coef, score)
    x.toCsv("savedModels/bestModel.csv")
    x.fromCsv("savedModels/bestModel.csv")

    x.runModelGR1(PredictionDataset)

#https://medium.com/datadriveninvestor/a-simple-guide-to-creating-predictive-models-in-python-part-2a-aa86ece98f86
#Tensor Flow guide
#https://medium.com/datadriveninvestor/a-simple-guide-to-creating-predictive-models-in-python-part-2b-7be3afb5c557

if __name__ == '__main__':
    main()