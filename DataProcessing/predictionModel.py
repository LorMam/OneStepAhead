import pandas as pd
import numpy as np
from dataProcessing import inData
from sklearn.linear_model import LinearRegression
import csv

class predictionModel():
    def __init__(self, countriesInModel, parametersInModel):#, coefficients, score):
        self.countries = countriesInModel
        self.parameters = parametersInModel
        #self.coef = coefficients
        #self.score = score

    def toCsv(self, path):
        out = []
        out.append(self.countries)
        out.append(self.parameters)
        out.append(self.coef)
        #out.append(self.score)
        print("Model R^2",self.score)

        outdf = pd.DataFrame(out, columns = ['Countries', 'Parameters', 'Coefficients']) 
        outdf.to_csv(path)
        #with open(path, 'w', newline='') as file:	
        #    writer = csv.writer(file)	
        #    writer.writerows(out)
            

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

    
    #TODO @ Lorenz - don't understand what these functions are meant to do?
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


    def predictGrowthRate(self,dataset):
        #Return predicted initial growth rates given values from UN dataset
        return self.model.predict(dataset)
        
    #Create the Regression Model
    #Input:
    #inputdata = csv file containing country information (UN and growth rates)
    #pvar = names of variables to be used in the model (list of strings)
    def createRegressionModel(self,inputdata,pvar):

        df_hd = inData(inputdata)

        #Determine the selected variables to construct the model
        selvars = []
        colid = 0
        for pname in df_hd.columns:
            if pname in pvar:
                print(pname)
                selvars.append(colid)
            colid += 1
            
        print("Number of selection variables =",len(selvars))
        x = df_hd.iloc[ : , selvars]
        y = df_hd["GrowthRate1"]

        model = LinearRegression().fit(x, y)

        r_sq = model.score(x, y)
        self.score = r_sq

        self.coef = model.coef_
        print("Number of coefficients =",len(self.coef))
        
        self.model = model

        return
        
        
    
def main():
    c = ["China", "Japan",  "United Kingdom", "United States", "Italy", "Germany", "Algeria", "Egypt", "South Africa", "Brazil", "Chile", "Australia"]
    p = ["Prosperity Index Health Score", "Population using at least basic drinking-water services (%)", "Human development index (HDI)", "Population. total (millions)",
             "Population. under age 5 (%)", "Population. ages 65 and older (%)", "yearly anual Temperature"]
    coef = [-2.36494606e-03,  2.15270501e-03,  2.80678716e-01,  3.49335911e-05, -1.39790582e+00, -5.83476662e-01,  1.63075352e-03]
    score = [0.8777857786441605]

    #Need to read this in generically / match generically
    PredictionDataset = pd.DataFrame({ "Indices": ["Prosperity Index Health Score", "Population using at least basic drinking-water services (%)", "Human development index (HDI)", "Population. total (millions)",
             "Population. under age 5 (%)", "Population. ages 65 and older (%)",  "yearly anual Temperature"],
                                       "Values": [3, 0.3, 6, 6, 0.1, 0.2, 20]})
    
    dataallpath = "PipelineIntermediates/finalCleanDataCopyPasteBasic.csv"
    x = predictionModel(c, p)# coef, score)
    x.createRegressionModel(dataallpath,p)
    #Need to fix formatting here...
    #x.toCsv("savedModels/testModel.csv")
    #x.fromCsv("savedModels/testModel.csv")

    x.runModelGR1(PredictionDataset)

    #Need to read in data we want to test for different countries
    testvals = np.array([[3, 0.3, 6, 6, 0.1, 0.2, 20]])
    gr = x.predictGrowthRate(testvals)
    
    print("Predicted growth rate for",PredictionDataset["Values"],"is",gr)
#https://medium.com/datadriveninvestor/a-simple-guide-to-creating-predictive-models-in-python-part-2a-aa86ece98f86
#Tensor Flow guide
#https://medium.com/datadriveninvestor/a-simple-guide-to-creating-predictive-models-in-python-part-2b-7be3afb5c557

if __name__ == '__main__':
    main()
