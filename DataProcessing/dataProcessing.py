import numpy as np
import pandas as pd
from datetime import date

from dataManagement import includedCountries
from dataManagement import sourcePaths
from dataManagement import compactDataPath

def main():
    #getDataFromJohnshopkinsGithub()
    #data = exctractRelevantData(includedCountries, sourcePaths)
    #outToCsv(compactDataPath, data)
    joinData()




#list of countries, list of Paths -> 2DArray of Countries and their data
def exctractRelevantData(countries, sourcePaths): #may have been easier with using pandas
    latestYear = '2018'
    cleanData = np.append('Country', countries)
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
                    count = 1
                elif (len(row)>10):
                    #cut off first and last lines with metadata
                    dataTemp.append(row)
        #get index of column with selected year
        dataCol = dataTemp[0].index(latestYear)
        #only keep country and 2018 data column
        dataNew = []
        dataNew.append(column(dataTemp, 1))
        dataNew.append(column(dataTemp, dataCol))

        #look up all countries in data and collect their data
        temp = [Name]
        for i in countries:
            temp.append(column(dataNew, dataNew[0].index(i))[1])
        cleanData = np.append(cleanData, temp)


    cleanData = cleanData.reshape([len(sourcePaths) + 1, len(countries) + 1])
    cleanData = np.transpose(cleanData)
    return cleanData

def joinData():
    from dataManagement import joinToFinalTable
    data = pd.DataFrame({"Country" : includedCountries})
    print(data)
    for path in joinToFinalTable:
        data.set_index("Country").join(path)
        print(data)

def getDataFromJohnshopkinsGithub():
    url='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    data = pd.read_csv(url, error_bad_lines=False)
    data.to_csv("JohnsHopkins"+date.today().isoformat()+"NotUsed.csv")

def outToCsv(path, data):
    import csv
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


    #writer.writerow(["SN", "Name", "Contribution"])

def column(matrix, i):
    return [row[i] for row in matrix]

if __name__ == '__main__':
    main()


