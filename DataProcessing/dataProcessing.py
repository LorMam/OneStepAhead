import csv
import os

import numpy as np
import pandas as pd
from datetime import date

from scipy.optimize import curve_fit

from dataManagement import includedCountries
from dataManagement import sourcePaths
from dataManagement import growthRatesSource
from dataManagement import compactDataPath
from dataManagement import HopkinsData

def main():
    #getDataFromJohnshopkinsGithub()
    #CalculateGrowthRates()
    #exctractRelevantData()
    #outToCsv(compactDataPath, data)
    #joinData()




#list of countries, list of Paths -> 2DArray of Countries and their data
def exctractRelevantData(): #may have been easier with using pandas
    latestYear = '2018'
    cleanData = np.append('Country', includedCountries)
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
        for i in includedCountries:
            temp.append(column(dataNew, dataNew[0].index(i))[1])
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
                    temp.append(row.index[i])
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


#Fit functions
def logistic_model(x,a,b,c):
    return c/(1+np.exp(-(x-b)/a))

def exponential_model(x,a,b,c):
    return a*np.exp(b*(x-c))

def linear_fit(x,m,c):
    return x*m + c

#Calculate chi-squared goodness of fit
def chisquare(data,expct):
    return sum((data-expct)**2 / expct)

# Calculate the Growth Rates from relative data that came from Hopkins download
def CalculateGrowthRates():
    data = pd.read_csv(HopkinsData)
    # print(data.columns[0])

    with open(growthRatesSource, mode='w') as growthrate_file:
        csv_writer = csv.DictWriter(growthrate_file,
                                    fieldnames=["Country", "GrowthRate1", "GrowthRate2", "DayOfChange"])
        # country_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writeheader()

        cid = 1
        while cid < len(data.columns):
            growthrate = ObtainGrowthRate(HopkinsData, data.columns[cid])
            print("Growth rate for", data.columns[cid], "is", growthrate[0])
            csv_writer.writerow({"Country": data.columns[cid], "GrowthRate1": format(growthrate[0], '.5g'),
                                 "GrowthRate2": format(growthrate[1], '.5g'),
                                 "DayOfChange": format(growthrate[2], '.5g')})
            cid += 1

# Function to obtain growth rate from data file, only called from other function
# Input:
# inputfile = days since 100 cases , total number of cases, csv format
# country = name of country of interest
# daterange = boolean : option for a user specified range of days
# daystart = 0  : first day for fit period
# dayend = 100 : last day for fit period
def ObtainGrowthRate(inputfile, country, daterange=False, daystart=0, dayend=100):
    # Read in data file
    df = pd.read_csv(inputfile)

    # Define date range to fit. Default = all days
    mask = np.ones(len(df["Days since 100"]), dtype=bool)

    df = df[1:]  # drop first line for now

    # Mask to only consider days with data
    dayend = df["Days since 100"][np.nanargmax(df[country])] #doesnt work...
    mask = (df["Days since 100"] < dayend)

    # Adjust if date range is specified
    if daterange:
        mask = (df["Days since 100"] > daystart) & (df["Days since 100"] < dayend)

    # Check for sufficient data points:
    if not sum(df[country][mask]):
        print("Empty data for", country)
        return 0., 0., 0.

    # Perform a linear fit to the data
    popt, pcov = curve_fit(polfit, df["Days since 100"][mask], np.log10(df[country][mask]))
    chi2 = chisquare(df[country][mask], 10. ** (df["Days since 100"][mask] * popt[0] + popt[1]))

    inflection_date = 0.
    logchi2 = 0
    # Need minimum number of approx. ten days for a logistic fit
    if len(df["Days since 100"][mask]) > 15.:
        # Perform a logistic fit to the data
        log_fit, log_cov = curve_fit(logistic_model, df["Days since 100"][mask], df[country][mask],
                                     p0=[2.5, 1, max(df[country][mask])])
        logchi2 = chisquare(df[country][mask], logistic_model(df["Days since 100"][mask], *log_fit))

        inflection_date = log_fit[1]

    if (chi2 < logchi2) or (inflection_date > max(df["Days since 100"][mask])) or not inflection_date:
        growthrate = popt[0]
        print("linear fit preferred for", country, "growth rate", growthrate)
        return growthrate, 0., inflection_date

    print("logistic fit preferred for", country)
    print("inflection date", inflection_date)

    # Perform linear fits pre and post inflection date to compare growth rates
    mask1 = mask & (df["Days since 100"] < inflection_date)
    mask2 = mask & (df["Days since 100"] > inflection_date)

    growthrate = 0.
    growthrate2 = 0.

    # Check for sufficient data points:
    if sum(mask1) > 5:
        popt, pcov = curve_fit(polfit, df["Days since 100"][mask1], np.log10(df[country][mask1]))
        chi2 = chisquare(df[country][mask1], 10. ** (df["Days since 100"][mask1] * popt[0] + popt[1]))
        growthrate = popt[0]

    if sum(mask2) > 5:
        popt2, pcov2 = curve_fit(polfit, df["Days since 100"][mask2], np.log10(df[country][mask2]))
        chi2_2 = chisquare(df[country][mask2], 10. ** (df["Days since 100"][mask2] * popt2[0] + popt2[1]))
        growthrate2 = popt2[0]

    return growthrate, growthrate2, inflection_date

def column(matrix, i):
    return [row[i] for row in matrix]

if __name__ == '__main__':
    main()


