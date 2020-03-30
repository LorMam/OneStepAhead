import csv
import os

import numpy as np
import pandas as pd
from datetime import date
import dateutil.parser

from scipy.optimize import curve_fit

from dataManagement import includedCountries
from dataManagement import sourcePaths
from dataManagement import growthRatesSource
from dataManagement import compactDataPath
from dataManagement import HopkinsData
from dataManagement import toBeNormalized

def main():
    #getDataFromJohnshopkinsGithub()
    #CalculateGrowthRates()
    data = exctractRelevantData()
    outToCsv(compactDataPath, data)
    #joinData()




#list of countries, list of Paths -> 2DArray of Countries and their data
def exctractRelevantData(): #may have been easier with using pandas
    latestYear = '2018'
    cleanData = np.append('Country', includedCountries)
    normalizer = 0
    #go through dataSources
    for i in range(len(sourcePaths)):
        import csv
        with open(sourcePaths[i], 'r') as file:
            reader = csv.reader(file)
            count = 0
            dataTemp = []
            for row in reader:
                #get Dataset Name in first line
                if (count == 0):
                    Name = "".join(row)
                    count += 1
                elif (count<196):
                    #cut off first and last lines with metadata
                    dataTemp.append(row)
                count += 1
        #get index of column with selected year
        dataCol = dataTemp[0].index(latestYear)
        #only keep country and 2018 data column
        dataNew = []
        dataNew.append(column(dataTemp, 1))
        dataNew.append(column(dataTemp, dataCol))

        #look up all countries in data and collect their data
        temp = [Name]
        for country in includedCountries:
            temp.append(column(dataNew, dataNew[0].index(country))[1])
        cleanData = np.append(cleanData, temp)

    cleanData = cleanData.reshape([len(sourcePaths) + 1, len(includedCountries) + 1])
    cleanData = np.transpose(cleanData)
    return cleanData

def joinData():
    from dataManagement import joinToFinalTable
    data = pd.DataFrame({"Country" : includedCountries})
    data = data.set_index("Country")
    #errors might originate from not having ',' as separator and '.' as decimal point
    for p in joinToFinalTable:
    #p = joinToFinalTable[2]
        toJoin = pd.read_csv(p)
        data = data.join(toJoin.set_index('Country'))
        from dataManagement import finalFilePath
    data.to_csv(finalFilePath)

# convert Data from all countries
# getting newest Data from github csv
# outfile has countries, start Date and case numbers relative from start date
def getDataFromJohnshopkinsGithub():
    Threshold = 100 #from which date on should be counted
    path = 'JohnsHopkins2020-03-29NotUsed.csv' # if offline use this
    url='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    data = pd.read_csv(url, error_bad_lines=False)
    data = data.groupby('Country/Region').sum()
    data = data.drop(columns=['Lat', 'Long'])
    size = data.shape[1]
    outData = pd.DataFrame({'Days since 100': range(size+1)})

    for index, row in data.iterrows():
        temp = []
        first = True
        for i in range(size):  # or len(line)
            # parse through line until case>=100
            if (row[i] > Threshold):
                if (first):
                    datetemp = dateutil.parser.parse(row.index[i]).date()
                    temp.append(datetemp)
                    first = False
                temp.append(row[i])
        temp = pd.DataFrame({index: temp})
        outData = outData.join(temp)
    outData.to_csv(HopkinsData, index=False)


def outToCsv(path, data):
    import csv
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def column(matrix, i):
    return [row[i] for row in matrix]

if __name__ == '__main__':
    main()


