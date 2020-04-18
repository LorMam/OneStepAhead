import csv
import os

import numpy as np
import pandas as pd
import datetime
from datetime import date
import dateutil.parser
from app.dataProcessing.dataAnalysis import ObtainGrowthRate

def __init__():
    pass

# list of Paths -> 2DArray of Countries and their data
def getDataFromHDR(fromFiles, toPath):
    latestYear = '2018'
    outData = pd.DataFrame()
    normalizer = 0  #TODO normalize given datasets by population

    # go through dataSources
    for path in fromFiles:
        import csv
        with open(path, 'r') as file:
            reader = csv.reader(file)
            data = []
            for count, row in enumerate(reader):
                # get Dataset Name in first line
                if (count == 0): # get Name of Dataset from all cells in first line
                    Name = "".join(row)
                elif (count == 1):
                    headers = row
                else:
                    try:
                        int(row[0]) # take all lines having a rank number
                        data.append(row)
                    except:
                        None
        dat = pd.DataFrame(data, columns=headers)
        if (outData.empty):
            outData['Country'] = dat['Country']
        dataCol = dat[['Country', latestYear]]
        dataCol.columns = ['Country', Name]

        outData = outData.merge(dataCol, on='Country', how='left')
    normalizer = 1 #"Population, total (millions)"
    normalize = [5,6,7] #["Population, ages 15â€“64 (millions)", "Population, ages 65 and older (millions)", "Population, under age 5 (millions)"]
    outData=outData.replace('..', float("nan"))

    for n in normalize:
        series1 = outData.iloc[:,n]
        series2 = outData.iloc[:,normalizer]
        outData.iloc[:,n] = pd.to_numeric(series1).div(pd.to_numeric(series2),fill_value=None)

    return dataOut(toPath, outData)

#join Data of difference files by column "Country"
def joinData(fromFiles, toPath, allCountries):

    outData = pd.DataFrame({"Country": allCountries})
    outData = outData.set_index("Country")
    # errors might originate from not having ',' as separator and '.' as decimal point
    for p in fromFiles:
        data = inData(p)

        data = replace(data)

        outData = outData.merge(data, on='Country', how='left')

    return dataOut(toPath, outData)

def replace(data):
    # in extra function... and Iterate through df
    data = data.replace(to_replace="Bolivia (Plurinational State of)", value="Bolivia")
    data = data.replace(to_replace="Cape Verde", value="Cabo Verde")
    data = data.replace(to_replace="Cï¿½te d'Ivoire", value="Cote d'Ivoire")
    data = data.replace(to_replace="Democratic Republic of Congo", value="Congo")
    data = data.replace(to_replace="Congo (Democratic Republic of the)", value="Congo")
    data = data.replace(to_replace="Czech Republic", value="Czechia")
    data = data.replace(to_replace="Eswatini (Kingdom of)", value="Eswatini")
    data = data.replace(to_replace="France (Europe)", value="France")
    data = data.replace(to_replace="Hong Kong, China (SAR)", value="Hong Kong")
    data = data.replace(to_replace="Iran (Islamic Republic of)", value="Iran")
    data = data.replace(to_replace="Korea (Republic of)", value="South Korea")
    data = data.replace(to_replace="Moldova (Republic of)", value="Moldova")
    data = data.replace(to_replace="Palestine, State of", value="Palestina")
    data = data.replace(to_replace="Russian Federation", value="Russia")
    data = data.replace(to_replace="Saint Vincent And The Grenadines", value="Saint Vincent and the Grenadines")
    data = data.replace(to_replace="Sï¿½o Tomï¿½ and Prï¿½ncipe", value="Sao Tome and Principe")
    data = data.replace(to_replace="Sao Tome And Principe", value="Sao Tome and Principe")
    data = data.replace(to_replace="Syrian Arab Republic", value="Syria")
    data = data.replace(to_replace="Tanzania (United Republic of)", value="Tanzania")
    data = data.replace(to_replace="Timor-Leste", value="Timor Leste")
    data = data.replace(to_replace="United Kingdom (Europe)", value="United Kingdom")
    data = data.replace(to_replace="Venezuela (Bolivarian Republic of)", value="Venezuela")
    data = data.replace(to_replace="Viet Nam", value="Vietnam")
    data = data.replace(to_replace="Lao People's Democratic Republic", value="Laos")
    data = data.replace(to_replace="CuraÃ§ao", value="Curacao")

    return data

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

    return dataOut(toPath, outData)



def dataOut(toPath, outData):
    if (toPath == "none"):
        return outData
    else:
        outData.to_csv(toPath)

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
    outData = pd.DataFrame({"Country" : data["Country"].unique()})
    outData = outData.set_index("Country")
    for indic in data["indicator_name"].unique(): # for every indicator
        mask = data["indicator_name"] == indic
        out = pd.DataFrame({indic: data[mask]["score_2019"], "Country" : data[mask]["Country"]})
        #print(out)
        #print(outData)
        outData = outData.join(out.set_index("Country"))

    return dataOut(toPath, outData)

#dt, AverageTemperature, AverageTemperatureUncertainty, Country -> Yearly, Monthly avg temperature per country
def getTemperatureData(FromData, toPath):
    data = inData(FromData)
    data = data.drop(columns='AverageTemperatureUncertainty')

    startdate = datetime.datetime.strptime('1990-01-01', '%Y-%m-%d')
    datemask = data['dt'].apply(lambda d: datetime.datetime.strptime(d, '%Y-%m-%d')) > startdate##datetime.datetime > date('1990-01-01')
    data=data[datemask]

    dates = data['dt'].apply(lambda d: str.split(d, "-"))

    data['year'] = column(dates,0)
    data['month'] = column(dates, 1)

    outData = data.groupby(['Country']).mean().reset_index()
    monthlyAvg = data.groupby(['Country', 'month'],).mean().reset_index()

    monthlyAvg=pd.DataFrame(monthlyAvg['AverageTemperature'].values.reshape([monthlyAvg['Country'].nunique(), 12]))
    monthlyAvg.columns=range(1,13)
    outData = outData.join(monthlyAvg)

    return dataOut(toPath, outData)


def getTestingData(toPath):
    #covid-testing-05-Apr-all-observations.csv from google drive - does Filename stay the same?????
    #https://drive.google.com/open?id=19WI7vvzlrZvD_CnydUq5Zt0uw1aky_sT
    file_id = '19WI7vvzlrZvD_CnydUq5Zt0uw1aky_sT'
    destination = 'DataResources/OurWorldInDataTesting.csv'
    download_file_from_google_drive(file_id, destination)

    f=pd.read_csv('DataResources/OurWorldInDataTesting.csv')

    '''#try to get from website directly
    import urllib.request as request
    url = 'blob:https://ourworldindata.org/5f603fc2-9a59-4e00-8422-1df3333cbc18'
    # fake user agent of Safari
    fake_useragent = 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25'
    r = request.Request(url, headers={'User-Agent': fake_useragent})
    f = request.urlopen(r)'''

    #'https://covid.ourworldindata.org/data/ecdc/full_data.csv'
    #'http://localhost:8080/data/tests/latest/data.csv'

    f=f.drop(columns=['Source URL','Source label','Notes'])

    country = f['Entity'].apply(lambda d: str.split(d, " - "))
    f['Country']=column(country,0)
    f['Unit']=column(country,1)
    
    #average of all new test per day
    outData = f.groupby(['Country']).mean().reset_index()

    #keep Cumulative total per million, Country
    outData = outData[['Country', 'Daily change in cumulative total per million']]

    return dataOut(toPath, outData)


'''#taken from this StackOverflow answer: https://stackoverflow.com/a/39225039
import requests

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)'''

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

#takes [path or Dataframe] and [path or "none"], returns data or writes to File
def WriteGrowthRates(FromData, toPath):
    data = inData(FromData)

    gr1 = []
    gr2 = []
    dc = []

    cid = 1
    while cid < len(data.columns):
        
        growthrate = ObtainGrowthRate(data,data.columns[cid])
        
        gr1.append(growthrate[0])
        gr2.append(growthrate[1])
        dc.append(growthrate[2])
            
        cid += 1
    
    #Also return growth rate information

    outData = pd.DataFrame({"Country":data.columns[1:],"GrowthRate1":gr1,"GrowthRate2":gr2,"DayOfChange":dc})

    return dataOut(toPath, outData)

        
def column(matrix, i):
    return [row[i] for row in matrix]

