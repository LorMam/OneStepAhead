from dataProcessing import getDataFromJohnshopkinsGithub
from dataProcessing import joinData
from dataProcessing import getDataFromHDR
from dataProcessing import getDatafromProsperityDataset
from dataProcessing import WriteGrowthRates
from dataProcessing import getTemperatureData
from dataProcessing import getTestingData
from DataProcessing.googleAPI import getGoogleTrends

import predictionModel
from IPython import embed


import pandas as pd



# list of countries to be included in prediction model
# Country Names as in UN Data


closerLookat = ["China", "Japan", "United Kingdom", "United States", "Italy", "Germany", "Algeria", "Egypt",
                "South Africa", "Brazil", "Chile", "Australia"]

allCountries = ["Bolivia","Cabo Verde","Cote d'Ivoire","Congo","Czechia","Eswatini","France","Hong Kong","Iran",
                "South Korea","Moldova","Palestina","Russia","Saint Vincent and the Grenadines","Sao Tome and Principe",
                "Syria","Tanzania","Timor Leste","United Kingdom","Venezuela","Vietnam","Afghanistan","Albania",
                "Algeria","Andorra","Angola","Antigua and Barbuda","Argentina","Armenia","Australia","Austria",
                "Azerbaijan","Bahamas","Bahrain","Baker Island","Bangladesh","Barbados","Belarus","Belgium","Belize",
                "Benin","Bhutan","Bosnia and Herzegovina","Botswana","Brazil","Brunei Darussalam","Bulgaria",
                "Burkina Faso","Burma","Burundi","Cambodia","Cameroon","Canada","Central African Republic","Chad",
                "Chile","China","Colombia","Comoros","Costa Rica","Croatia","Cuba","Curacao","Cyprus","Denmark",
                "Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea"
                ,"Estonia","Ethiopia","Falkland Islands (Islas Malvinas)","Federated States Of Micronesia","Fiji","Finland",
                "French Guiana","French Southern And Antarctic Lands","Gabon","Gambia","Georgia","Germany","Ghana",
                "Greece","Grenada","Guam","Guatemala","Guinea","Guinea-Bissau","Guyana","Haiti",
                "Heard Island And Mcdonald Islands","Honduras","Hungary","Iceland","India","Indonesia","Iraq","Ireland",
                "Isle Of Man","Israel","Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kazakhstan","Kenya",
                "Kingman Reef","Kiribati","Kuwait","Kyrgyzstan","Lao People's Democratic Republic","Laos","Latvia",
                "Lebanon","Lesotho","Liberia","Libya","Libya","Liechtenstein","Lithuania","Luxembourg","Macedonia",
                "Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Martinique","Mauritania",
                "Mauritius","Mayotte","Mexico","Micronesia (Federated States of)","Monaco","Mongolia","Montenegro",
                "Morocco","Mozambique","Myanmar","Namibia","Nepal","Netherlands","New Caledonia","New Zealand",
                "Nicaragua","Niger","Nigeria","North Macedonia","Northern Mariana Islands","Norway","Oceania",
                "Oman","Pakistan","Palau","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland",
                "Portugal","Puerto Rico","Qatar","Romania","Rwanda","Saint Kitts And Nevis","Saint Lucia",
                "Saint Martin","Samoa","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore",
                "Slovakia","Slovenia","Solomon Islands","Somalia","South Africa","South Georgia And The South Sandwich Isla",
                "South Sudan","Spain","Sri Lanka","Sudan","Suriname","Svalbard And Jan Mayen","Swaziland","Sweden",
                "Switzerland","Taiwan","Tajikistan","Thailand","The Gambia","Togo","Tonga","Trinidad and Tobago",
                "Tunisia","Turkey","Turkmenistan","Uganda","Ukraine","United Arab Emirates","United States","Uruguay",
                "Uzbekistan","Vanuatu","Virgin Islands","Yemen","Zambia","Zimbabwe"]

atLeastProspData = ["Bolivia","Cabo Verde","Congo","Czechia","Eswatini","France","Hong Kong","Iran",
                "South Korea","Moldova","Russia","Syria","Tanzania","United Kingdom","Venezuela","Vietnam","Afghanistan","Albania",
                "Algeria","Angola","Argentina","Armenia","Australia","Austria",
                "Azerbaijan","Bahrain","Bangladesh","Belarus","Belgium","Belize",
                "Benin","Bosnia and Herzegovina","Botswana","Brazil","Bulgaria",
                "Burkina Faso","Burundi","Cambodia","Cameroon","Canada","Central African Republic","Chad",
                "Chile","China","Colombia","Comoros","Costa Rica","Croatia","Cuba","Cyprus","Denmark",
                "Djibouti","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea"
                ,"Estonia","Ethiopia","Finland", "French Southern And Antarctic Lands","Gabon","Georgia","Germany","Ghana",
                "Greece","Guatemala","Guinea","Guinea-Bissau","Guyana","Haiti",
               "Honduras","Hungary","Iceland","India","Indonesia","Iraq","Ireland",
               "Israel","Italy","Jamaica","Japan","Jordan","Kazakhstan","Kazakhstan","Kenya",
               "Kuwait","Kyrgyzstan","Laos","Latvia", "Lebanon","Lesotho","Liberia","Libya","Libya","Lithuania","Luxembourg",
                "Madagascar","Malawi","Malaysia","Mali","Malta","Mauritania",
                "Mauritius","Mexico","Mongolia","Montenegro", "Morocco","Mozambique","Myanmar","Namibia","Nepal","Netherlands","New Zealand",
                "Nicaragua","Niger","Nigeria","North Macedonia","Norway", "Oman","Pakistan","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland",
                "Portugal","Qatar","Romania","Rwanda","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore",
                "Slovakia","Slovenia","Somalia","South Africa", "South Sudan","Spain","Sri Lanka","Sudan","Suriname","Sweden",
                "Switzerland","Taiwan","Tajikistan","Thailand","The Gambia","Togo","Trinidad and Tobago",
                "Tunisia","Turkey","Turkmenistan","Uganda","Ukraine","United Arab Emirates","United States","Uruguay",
                "Uzbekistan","Yemen","Zambia","Zimbabwe"]

#but Temperature and/or HDR
noProsperityData = ["Cote d'Ivoire", "Palestina", "Saint Vincent and the Grenadines","Sao Tome and Principe", "Timor Leste", "Andorra", "Antigua and Barbuda", "Bahamas", "Baker Island", "Barbados",
                "Bhutan", "Brunei Darussalam", "Burma", "CuraÃ§ao", "Dominica", "Falkland Islands (Islas Malvinas)", "Federated States Of Micronesia", "Fiji", "French Guiana", "Gambia", "Grenada","Guam", "Heard Island And Mcdonald Islands", "Isle Of Man",
                "Jersey", "Kingman Reef","Kiribati", "Liechtenstein", "Macedonia", "Maldives", "Marshall Islands","Martinique","Mayotte","Micronesia (Federated States of)","Monaco", "New Caledonia", "Northern Mariana Islands", "Oceania","Palau",
                "Puerto Rico", "Saint Kitts And Nevis","Saint Lucia", "Saint Martin","Samoa", "Solomon Islands", "South Georgia And The South Sandwich Isla","Svalbard And Jan Mayen","Swaziland", "Tonga", "Vanuatu","Virgin Islands"]


sourcePaths = [
        # all datasets from http://hdr.undp.org/en/data#
        'DataResources/HDR/Population, total (millions).csv',
        'DataResources/HDR/Education Index.csv',
        'DataResources/HDR/Human development index (HDI).csv',
        'DataResources/HDR/Life expectancy at birth.csv',
        'DataResources/HDR/Population, ages 15to64 (millions).csv',
        'DataResources/HDR/Population, ages 65 and older (millions).csv',
        'DataResources/HDR/Population, under age 5 (millions).csv',
        'DataResources/HDR/Population, urban (%).csv',
        'DataResources/HDR/Unemployment, total (% of labour force).csv',
        'DataResources/HDR/Gross domestic product (GDP) per capita (2011 PPP $).csv',
        'DataResources/HDR/Mobile phone subscriptions (per 100 people) 2018.csv'
    ]

'''toBeNormalized = [
        'DataResources/HDR/Population, ages 15to64 (millions).csv',
        'DataResources/HDR/Population, ages 65 and older (millions).csv',
        'DataResources/HDR/Population, under age 5 (millions).csv'
    ]
    NormalizeBy = 'Population, total (millions).csv'
'''
compactDataPath = 'PipelineIntermediates/humanDevelopmentDataCompact.csv'
growthRatesSource = 'PipelineIntermediates/GrowthRatesAll.csv'
InterventionDataPath = 'DataResources/InterventionAndDate.csv'

# paths to all data Files to be joined (for given countries)
# gives the order of joining
joinToFinalTable = [
        growthRatesSource,
        compactDataPath,
        InterventionDataPath]
ProsperityDataPath = "DataResources/cleanDataProsperityIndex.CSV"
TemperatureDataPath = "DataResources/rawGlobalLandTemperaturesByCountry.csv"

HopkinsData = 'PipelineIntermediates/CountryCasesFromHopkins.csv'
googleDataFolder = 'PipelineIntermediates/googleTrends/'

staticDataOut = 'PipelineIntermediates/staticDataTotal.csv'



def main():

    #STATIC DATA - DONE (for now) see staticDataOut

    #ProsperityData = getDatafromProsperityDataset(ProsperityDataPath, "PipelineIntermediates/ProspData.csv")
    #print(ProsperityData) #looks fine

    #HDR_Data = getDataFromHDR(sourcePaths, "none")
    #print(HDR_Data) #looks fine

    #TemperatureData = getTemperatureData(TemperatureDataPath, "none")
    #print(TemperatureData) # looks fine

    #toJoin = [ProsperityData, HDR_Data, TemperatureData]
    #toJoin = ["PipelineIntermediates/ProspData.csv", "PipelineIntermediates/TempData.csv", "PipelineIntermediates/HDRData.csv"]

    #joinData(toJoin, staticDataOut, allCountries)



    #DYNAMIC DATA

    HopkinsData = getDataFromJohnshopkinsGithub("none")
    #print(HopkinsData) #looks fine

    #TestingData = getTestingData("none")
    #print(TestingData)

    #GoogleWords for Start Dates
    wordsToSearch=['covid19', 'corona', 'coronavirus', 'google']
    df = pd.DataFrame(HopkinsData.iloc[0,1:]).reset_index()
    df.columns = ['Country','Start Day']
    df = df[df['Start Day'].notna()]

    googleTrends = getGoogleTrends(df, 'PipelineIntermediates/googleData.csv', wordsToSearch)
    print(googleTrends)

    #calculate growth rate function
    GrowthRateData = 'PipelineIntermediates/GrowthRates.csv'

    #GrowthRates = WriteGrowthRates(HopkinsData, "none")
    #TODO maybe do the print() as log somewhere in .txt
    #print(GrowthRates)
    #Perhaps call some data visulisation / plotting here





    #perform modeling
    #tst = predictionModel.main(finalFilePath)


    #Intervention - to second chain

    #embed()


if __name__ == '__main__':
    main()

