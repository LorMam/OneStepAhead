import pandas as pd
import numpy as np
import pycountry

from pytrends.request import TrendReq
from datetime import date
from dataProcessing import dataOut

from dataProcessing import column
pytrend = TrendReq()

#set with countries and start date


# https://pypi.org/project/pytrends/

def getGoogleTrends(InfoIn, toPath, wordsToSearch):
    # get international standard code for countries
    InfoIn['Countrycode'] = getCountrycodes(InfoIn['Country'])

    #Venezuela = VEN
    #Vietnam = VNM
    #WestBank and Gaza - none

    print(InfoIn)

    temp = "empty"
    for i, row in InfoIn.iterrows():
        time = str(row['Start Day']) + ' ' + str(row['Start Day'])
        code = row["Countrycode"]
        if (code != 'Unknown code'):
            data = pd.DataFrame(googleSearchTrends(wordsToSearch, code, time)).reset_index()
            data["Country"] = row["Country"]

            '''            for n in range(len(wordsToSearch)):
            print(data.iloc[n, :])
            print(data.iloc[4, :])
            data.loc[n] = data.loc[n] * (100 / data.loc[4])'''

            if (isinstance(temp, pd.DataFrame)):
                temp = temp.append(data)
            else:
                temp = data

        else:
            print(row["Country"] + " country code not found")

    return dataOut(toPath, temp)

def getCountrycodes(listOfCountries):
    countries = {}
    for country in pycountry.countries:
        countries[country.name] = country.alpha_2

    codes = [countries.get(country, 'Unknown code') for country in listOfCountries]
    return codes

def googleSearchTrends(search, code, time):
    pytrend.build_payload(kw_list=search, timeframe=time, geo=code)
    return pytrend.interest_over_time()

    '''
    #setup payload
    #timeframe
    frame1 = 'today 5-y' # Defaults to last 5 yrs,
    all = 'all' # Everything
    specific = '2020-02-06 2020-02-12' # 'YYYY-MM-DD YYYY-MM-DD'  Specific dates
    specific2 = '2017-02-06T10 2017-02-12T07'# 'YYYY-MM-DDTHH YYYY-MM-DDTHH' Specific datetimes,

    pytrend.build_payload(kw_list=wordsToSearch, timeframe=specific)

    # Interest by Region
    # pytrend.interest_by_region()
    df = pytrend.interest_over_time()
    print(df.head(10))

    # Get Google Hot Trends data
    #df = pytrend.trending_searches(pn='united_states')

    # df = pytrend.today_searches(pn=’US’)

    # Get Google Top Charts
    # df = pytrend.top_charts(2019, hl='en-US', tz=300, geo='GLOBAL')

    # related queries
    # pytrend.related_queries()
    # pytrend.related_topics()'''

if __name__ == '__main__':
    main()