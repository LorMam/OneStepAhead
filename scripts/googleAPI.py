import pandas as pd
import numpy as np
from googletrans import Translator
from pytrends.request import TrendReq
from datetime import date
from dataProcessing import dataOut

from dataProcessing import column

pytrend = TrendReq()


# pytrend = TrendReq(hl='en-US', tz=360)

# set with countries and start date


# https://pypi.org/project/pytrends/
# https://pypi.org/project/googletrans/ not official
# https://cloud.google.com/translate/docs/basic/translating-text#translate_translate_text-python official, but not used now
def getGoogleTrends(InfoIn, toPath, wordsToSearch):
    # get international standard code for countries
    temp = getCountryInfo(InfoIn['Country'])
    InfoIn = InfoIn.merge(temp, on='Country', how='left')
    translator = Translator()
    temp = "empty"

    for i, row in InfoIn.iterrows():
        time = str(row['Start Day']) + ' ' + str(row['Start Day'])
        code = row["Countrycode"]
        if (code != 'Unknown code'):
            mainLang = row['Languages'].split(',')[0]
            mainLang = mainLang[0:2]  # cut second language specification

            try:
                translations = translator.translate(wordsToSearch[1], dest=mainLang, src='en')
                languageSpecific = []
                for trans in translations:
                    languageSpecific.append(str(trans.text))
            except:
                print("language" + mainLang + "not available")

            originalWords = []

            for i in wordsToSearch[0]:
                originalWords.append(i)

            # print(languageSpecific)
            # print(originalWords)
            allWords = languageSpecific + originalWords

            groups = np.split(allWords, [4])

            print(allWords)
            # print(originalWords)
            # print(languageSpecific)
            # print(code)
            # print(time)
            # ["ایستگاه قطار", "اتوبوس", "test", "test1", "test2"],
            # pytrend.build_payload(["اتوبوس"], timeframe=time, geo=code)
            # print(pytrend.interest_over_time())
            # print('ENDE')

            data = "empty"
            for i in groups:
                i = np.append(i, "google")
                pytrend.build_payload(i, timeframe=time, geo=code)
                outcome = pytrend.interest_over_time().reset_index()

                if (isinstance(data, pd.DataFrame)):
                    data = data.merge(outcome, on='date')
                else:
                    data = outcome
            # print("language or google doesnt work")
            # data = pd.DataFrame(columns=['Country'])
            # print(data)
            data["Country"] = row["Country"]
            for i, word in enumerate(wordsToSearch[1]):
                data['searched' + word] = languageSpecific[i]

            '''            for n in range(len(wordsToSearch)):
            print(data.iloc[n, :])
            print(data.iloc[4, :])
            data.loc[n] = data.loc[n] * (100 / data.loc[4])'''

            if (isinstance(temp, pd.DataFrame)):
                temp = temp.append(data)
            else:
                temp = data
            # print(temp)
        else:
            print(row["Country"] + " country code not found")

    return dataOut(toPath, temp)


# gets country languages and country Iso alpha 2 codes
def getCountryInfo(listOfCountries):
    path = 'DataResources/countriesLookUp.csv'
    LookUp = pd.read_csv(path)
    countries = pd.DataFrame(columns=['Country', 'Countrycode', 'Languages'])
    # print(LookUp['name'])
    for country in listOfCountries:
        lang = 'Unknown code'
        code = 'Unknown code'
        if country in LookUp['name'].unique():
            row = LookUp[LookUp['name'] == country]
            code = row['ISO3166-1-Alpha-2'].values[0]
            lang = row['Languages'].values[0]
        elif country in LookUp['official_name_en'].unique():
            row = LookUp[LookUp['official_name_en'] == country]
            code = row['ISO3166-1-Alpha-2'].values[0]
            lang = row['Languages'].values[0]

        countries = countries.append({'Country': country, 'Countrycode': code, 'Languages': lang}, ignore_index=True)
    return countries
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