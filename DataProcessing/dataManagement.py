

#list of countries to be included in prediction model
#Country Names as in UN Data
includedCountries = ["China", "Japan", "Korea (Republic of)", "United Kingdom", "United States", "Italy", "Iran (Islamic Republic of)", "Germany", "Algeria", "Egypt", "Burkina Faso", "South Africa", "Brazil", "Chile", "Australia"]


#data just made up!!!!
dayOfHundredCases = ['2020-03-06', '2020-02-25', '2020-02-01', '2020-01-03', '2020-03-06', '2020-02-25', '2020-02-01', '2020-01-03', '2020-03-06', '2020-02-25', '2020-02-01', '2020-01-03', '2020-03-06', '2020-02-25', '2020-02-01']


sourcePaths = [
    #all datasets from http://hdr.undp.org/en/data#
    'resources/Education Index.csv',
    'resources/Human development index (HDI).csv',
    'resources/Life expectancy at birth.csv',
    'resources/Population, ages 15to64 (millions).csv',
    'resources/Population, ages 65 and older (millions).csv',
    'resources/Population, total (millions).csv',
    'resources/Population, under age 5 (millions).csv',
    'resources/Population, urban (%).csv',
    'resources/Unemployment, total (% of labour force).csv']

compactDataPath = 'compactData.csv'

#potentially from other python script?
growthRatesSource = 'GrowthRateMadeUp.csv'

#paths to all data Files
joinToFinalTable = [
    compactDataPath
]