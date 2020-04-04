import csv
import os

import numpy as np
import pandas as pd
from datetime import date
import dateutil.parser
from dataAnalysis import ObtainGrowthRate

# list of countries, list of Paths -> 2DArray of Countries and their data
def getDataFromHDR(countries, fromFiles, toPath):  # may have been easier with using pandas
    latestYear = '2018'
    cleanData = np.append('Country', countries)
    normalizer = 0  #TODO normalize given datasets by population
    # go through dataSources
    for path in fromFiles:
        import csv
        with open(path, 'r') as file:
            reader = csv.reader(file)
            dataTemp = []
            for count, row in enumerate(reader):
                # get Dataset Name in first line
                if (count == 0): # get Name of Dataset from all cells in first line
                    Name = "".join(row)
                elif (count < 196): #TODO remove magic number, (cut off before 'world,...')
                    dataTemp.append(row)
        # get index of column with selected year
        dataCol = dataTemp[0].index(latestYear)
        # only keep country and 2018 data column
        dataNew = []
        dataNew.append(column(dataTemp, 1))
        dataNew.append(column(dataTemp, dataCol))

        # look up all countries in data and collect their data
        temp = [Name]
        for country in countries:
            temp.append(column(dataNew, dataNew[0].index(country))[1])
        cleanData = np.append(cleanData, temp)

    cleanData = cleanData.reshape([len(fromFiles) + 1, len(countries) + 1]).transpose()
    
    outData = pd.DataFrame(cleanData, index=column(cleanData, 0), columns=cleanData[0])
    outData = outData.drop("Country",axis=0).drop("Country", axis=1)
    if (toPath == "none"):
        return outData
    else:
        outData.to_csv(toPath)

#join Data of difference files by column "Country"
def joinData(fromFiles, fromCountries, toPath):

    data = pd.DataFrame({"Country": fromCountries})
    data = data.set_index("Country")
    # errors might originate from not having ',' as separator and '.' as decimal point
    for p in fromFiles:
        # p = joinToFinalTable[2]
        toJoin = pd.read_csv(p)
        data = data.join(toJoin.set_index('Country'))

    if (toPath == "none"):
        return data
    else:
        data.to_csv(toPath)


# convert Data from all countries
# getting newest Data from github csv
# outfile has countries, start Date and case numbers relative from start date
def getDataFromJohnshopkinsGithub(toPath):
    Threshold = 100  # from which date on should be counted
    path = 'PipelineIntermediates/JohnsHopkins2020-03-29NotUsed.csv'  # if offline use this
    try:
        url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
        data = pd.read_csv(url, error_bad_lines=False)
    except:
        data = pd.read_csv(path)
        print("use offline dataset")
    data = data.groupby('Country/Region').sum()
    data = data.drop(columns=['Lat', 'Long'])
    size = data.shape[1]
    outData = pd.DataFrame({'Days since 100': range(size + 1)})

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

    if (toPath == "none"):
        return outData
    else:
        outData.to_csv(toPath, index=False)

def inData(PathOrDF):
    if (isinstance(PathOrDF, str)):
        data = pd.read_csv(PathOrDF)
    else:
        data = PathOrDF
    return data

# reformats ProsperityIndexData: [area name, indicator name, score] in lines -> table
#takes [path or Dataframe] and [path or "none"], returns data or writes to File
def getDatafromProsperityDataset(FromData, toPath):
    data = inData(FromData)

    out = []
    outData = pd.DataFrame({"area_name" : data["area_name"].unique()})
    outData = outData.set_index("area_name")
    for indic in data["indicator_name"].unique(): # for every indicator
        mask = data["indicator_name"] == indic
        out = pd.DataFrame({indic: data[mask]["score_2019"], "area_name" : data[mask]["area_name"]})
        #print(out)
        #print(outData)
        outData = outData.join(out.set_index("area_name"))

    if (toPath == "none"):
        return outData
    else:
        outData.to_csv(toPath)

#takes [path or Dataframe] and [path or "none"], returns data or writes to File
def WriteGrowthRates(FromData, toPath):
    data = inData(FromData)

    gr1 = []
    gr2 = []
    dc = []

    outname = toPath
    with open(outname,mode='w') as toPath:
        csv_writer = csv.DictWriter(toPath,fieldnames=["Country","GrowthRate1","GrowthRate2","DayOfChange"])
        csv_writer.writeheader()

        cid = 1
        while cid < len(data.columns):
            growthrate = ObtainGrowthRate(data,data.columns[cid])

            csv_writer.writerow({"Country":data.columns[cid],"GrowthRate1":format(growthrate[0],'.5g'),
                                "GrowthRate2":format(growthrate[1],'.5g'),"DayOfChange":format(growthrate[2],'.5g')})
            gr1.append(growthrate[0])
            gr2.append(growthrate[1])
            dc.append(growthrate[2])
            
            cid += 1

    #Also return growth rate information
    growthrateinfo = data.columns,gr1,gr2,dc
    
    return growthrateinfo
    
def column(matrix, i):
    return [row[i] for row in matrix]
