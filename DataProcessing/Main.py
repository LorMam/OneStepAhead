
if __name__ == '__main__':
    main()

    from dataProcessing import getDataFromJohnshopkinsGithub
    from dataProcessing import joinData
    from dataProcessing import exctractRelevantData

    from dataProcessing import ObtainGrowthRate
    from dataProcessing import WriteGrowthRate
    from dataProcessing import WriteGrowthRates

    CountriesHopkins = ["China", "Japan", "United Kingdom", "Italy", "Germany", "Algeria", "Egypt", "Burkina Faso",
     "South Africa", "Brazil", "Chile", "Australia", "US", "Iran", "Korea, South"]

def main():

    getDataFromJohnshopkinsGithub()
    #WriteGrowthRates("CountryCases.csv")

    #exctractRelevantData()

    #calculate growth rate function

    joinData()


    #perform modeling