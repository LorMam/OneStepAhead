import pandas as pd
import numpy as np
import pycountry

from pytrends.request import TrendReq
from datetime import date
from dataProcessing import outToCsv

from dataProcessing import column
pytrend = TrendReq()

from dataManagement import includedCountries
from dataManagement import dayOfHundredCases

wordsToSearch = ['covid 19', 'corona', 'coronavirus']

#set with countries and start date
InfoIn =   pd.DataFrame({'Country': includedCountries,
            'Start': dayOfHundredCases}) #Data just Made up, import from source file later


# https://pypi.org/project/pytrends/

def main():
    # get international standard code for countries
    InfoIn['Countrycode'] = getCountrycodes(InfoIn['Country'])
    for i in range(len(InfoIn["Country"])):
        time = InfoIn['Start'][i] + ' ' + date.today().isoformat()
        code = InfoIn["Countrycode"][i]
        if (code != 'Unknown code'):
            data = pd.DataFrame(googleSearchTrends(wordsToSearch, code, time))
            data.to_csv('googleTrends/' + InfoIn["Country"][i] + ".csv")
        else:
            print(InfoIn["Country"][i] + " country code not found")

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