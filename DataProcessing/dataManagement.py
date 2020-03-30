

#list of countries to be included in prediction model
#Country Names as in UN Data
closerLookat = ["China", "Japan",  "United Kingdom", "United States", "Italy", "Germany", "Algeria", "Egypt", "Burkina Faso", "South Africa", "Brazil", "Chile", "Australia"]
# kicked out becasue their names do problems... "Iran (Islamic Republic of)", "Korea (Republic of)",
allCountries = ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia (Plurinational State of)", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei Darussalam", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Congo (Democratic Republic of the)", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czechia", "CÃ´te d'Ivoire", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini (Kingdom of)", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hong Kong, China (SAR)", "Hungary", "Iceland", "India", "Indonesia", "Iran (Islamic Republic of)", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea (Republic of)", "Kuwait", "Kyrgyzstan", "Lao People's Democratic Republic", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia (Federated States of)", "Moldova (Republic of)", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Palestine, State of", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russian Federation", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syrian Arab Republic", "Tajikistan", "Tanzania (United Republic of)", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela (Bolivarian Republic of)", "Viet Nam", "Yemen", "Zambia", "Zimbabwe"]
includedCountries = closerLookat
# excluded because data missing: "Korea (Democratic People's Rep. of)", , "Somalia",

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
    'resources/Unemployment, total (% of labour force).csv',
    'resources/Gross domestic product (GDP) per capita (2011 PPP $).csv',
    'resources/Internet users, total (% of population) 2017.csv',
    'resources/Mobile phone subscriptions (per 100 people) 2018.csv',
    'resources/Population using at least basic drinking-water services (%) 2017.csv',
    'resources/Rural population with access to electricity (%) 2017.csv']
toBeNormalized = [
    'resources/Population, ages 15to64 (millions).csv',
    'resources/Population, ages 65 and older (millions).csv',
    'resources/Population, under age 5 (millions).csv'
]
NormalizeBy = 'Population, total (millions).csv'

compactDataPath = 'humanDevelopmentDataCompact.csv'

#potentially from other python script?
growthRatesSource = 'GrowthRates.csv'

#must be added later
InterventionDataPath = 'InterventionsMadeUp.csv'

#paths to all data Files
#gives the order of joining
joinToFinalTable = [
    growthRatesSource,
    compactDataPath,
    InterventionDataPath
]

HopkinsData = 'CountryCasesFromHopkins.csv'

#Final Merged clean File
finalFilePath = 'finalCleanData.csv'