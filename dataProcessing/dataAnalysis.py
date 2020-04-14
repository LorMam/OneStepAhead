import csv
import os,sys

import numpy as np
import pandas as pd
from datetime import date, timedelta
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit


def inData(PathOrDF):
    if (isinstance(PathOrDF, str)):
        data = pd.read_csv(PathOrDF)
    else:
        data = PathOrDF
    return data


#Fitting functions
def logistic_model(x,a,b,c):
    return c/(1+np.exp(-(x-b)/a))

def exponential_model(x,a,b,c):
    return a*np.exp(b*(x-c))

def linear_fit(x,m,c):
    return x*m + c

#Chi-square goodness of fit
def chisquare(data,expct):
    return sum((data-expct)**2 / expct)

#check day is in date format, or convert to date from string
def get_date(day):
    if not isinstance(day,date): 
        dinfo = day.split("-")
        ddate = date(int(dinfo[0]), int(dinfo[1]), int(dinfo[2]))
    else:
        ddate = day
    
    return ddate    

#Function to find the number of days between two dates
def days_diff(date1,date2):

    d1 = get_date(date1)
    d2 = get_date(date2)
        
    delta = d2 - d1
    
    return(delta.days)

#Function to perform linear fit to obtain growth rate
def fitlineargrowth(fitdays,fitcases,fitmask):
    gr = 0.
    chi2 = 0.

    if sum(fitmask) > 5:
        popt, pcov = curve_fit(linear_fit, fitdays[fitmask],np.log10(fitcases[fitmask]))
        chi2 = chisquare(fitcases[fitmask],10.**(fitdays[fitmask]*popt[0] + popt[1]))
        gr = popt[0]

    return gr, chi2

#Function to obtain growth rate from data file
#Input: 
# inputfile = days since 100 cases , total number of cases, csv format
# country = name of country of interest
# daterange = boolean : option for a user specified range of days
# interventiondate = "YYYY-MM-DD" date of intervention
def ObtainGrowthRate(inputfile,country,daterange=False,interventiondate="2000-01-01"):
    
    #initialise date range
    daystart=0
    dayend=100
    #data file already read in 
    df = inputfile
    
    date100 = df[country][df["Days since 100"] == daystart]
    #print("Date of 100th case in country",country,"is",date100[0])
    
    #Find intervention date in days after day of case 100
    if not isinstance(date100[0],np.float64):
        inter_date = days_diff(date100[0],interventiondate)
   
    
    #Define date range to fit. Default = all days
    mask = np.ones(len(df["Days since 100"])-1,dtype=bool)
    daymask = (df["Days since 100"] > daystart) 

    #copy to a list for same length
    days100 = df["Days since 100"][daymask]
    
    #Now case remaining information to integers
    cases100 = list(map(float,df[country][daymask]))
    cases100 = np.array(cases100)
    mask = mask & np.logical_not(np.isnan(cases100))
   
    if not sum(mask):
        #print("Insufficient data for",country)
        return 0., 0., 0.
    
    #Mask to only consider days with data
    dayend = days100[np.argmax(cases100)]
    mask = mask & (days100 < dayend) & (cases100 > 0.)

    #Adjust if date range is specified
    if daterange:
        mask = (days100 > daystart) & (days100 < dayend)
        
    #Perform a linear fit to the data
    growthrate, chi2 = fitlineargrowth(days100,cases100,mask)

    #Check for sufficient data points:
    if not growthrate:
        #print("Insufficient data for",country)
        return 0., 0., 0.

    inflection_day = 0.
    logchi2 = 0
    #Need minimum number of approx. ten days for a logistic fit
    if len(days100[mask]) > 15.:
        #Perform a logistic fit to the data
        try:
            log_fit, log_cov = curve_fit(logistic_model,days100[mask],cases100[mask],
                                 p0=[2.5,1,max(cases100[mask])],maxfev=1200)
            logchi2 = chisquare(cases100[mask],logistic_model(days100[mask],*log_fit))
            
            inflection_day = log_fit[1]
        except RuntimeError:
            print("Logistic function fit failed for",country)
            

    inflection_date = date100[0] + timedelta(days=inflection_day)

    if ((chi2 < logchi2) or (inflection_day > max(days100[mask])) or not inflection_day) and not (inter_date > 5):
        print("linear fit preferred for",country,"growth rate",growthrate)
        return growthrate, 0., inflection_date

    if (logchi2 < chi2) and (inflection_day < max(days100[mask])):
        print("logistic fit preferred for",country,"inflection date",inflection_date)
    
        #Alternatively, calculate pre and post intervention date:
    if inter_date > 5.:
        mask1 = mask & (days100 < inter_date)
        mask2 = mask & (days100 > inter_date)
    else:
        #Perform linear fits pre and post inflection date to compare growth rates
        mask1 = mask & (days100 < inflection_day)
        mask2 = mask & (days100 > inflection_day)

    
    #Perform linear fits
    growthrate, chi2 = fitlineargrowth(days100,cases100,mask1)
    
    growthrate2, chi2_2 = fitlineargrowth(days100,cases100,mask2)
        
    if inter_date > 5:
        print("intervention date",inter_date)
        return growthrate, growthrate2, inter_date

    
    return growthrate, growthrate2, inflection_date


#Function to read in interventions and investigate
#Input:
#datefile = csv format countries & intervention dates
#country_file = days since 100 cases , total number of cases, csv format
def interventionGrowthRates(datefile,country_file,toPath):

    df = inData(datefile)
    cf = inData(country_file)
    
    gr_ratios = np.zeros(df.shape)
    num_ratios = np.zeros(df.shape[1])
    
    inter_types = []
    itt = 0
    for col in df.columns:
        if not (col=="Country") and itt % 2:
            inter_types.append(col)
        itt += 1
    #print(inter_types)

    clist = []
    gr1list = []
    gr2list = []
    idlist = []
    ratiolist = []

    
    for row in df.iterrows():
        cnt = 0 # counter
        country = row[1][0]
        for column in row[1]:
            if not cnt:
                print(country)
            elif cnt % 2:
                flag = int(column)
            elif flag:
                date = column
                #print("Obtaining Growth rate for",country,date)
                igr = ObtainGrowthRate(cf,country,True,date)
                #print("Intervention Date",date,"growth rate before=",igr[0],"growth rate after = ",igr[1])
                ratio = 0.
                if igr[0] and igr[1]:
                    ratio = igr[1]/igr[0]
                    gr_ratios[row[0]][cnt] = ratio
                    num_ratios[cnt] += 1
                    
                clist.append(country)
                gr1list.append(igr[0])
                gr2list.append(igr[1])
                idlist.append(date)
                ratiolist.append(ratio)
            cnt += 1
            
    outData = pd.DataFrame({"Country":clist,"GrowthRate1":gr1list,"GrowthRate2":gr2list,
                            "DayOfChange":idlist,"GrowthRateRatio":ratiolist})

    if (toPath == "none"):
        return outData
    else:
        outData.to_csv(toPath)
        

'''
    it = 0
    mean_ratio_values = []
    num_ratio_values = []
    min_ratio_values = []
    max_ratio_values = []
    while it < len(num_ratios):
        if it and not it % 2:
            mean_ratio_values.append(np.mean(gr_ratios.T[it]))
            num_ratio_values.append(num_ratios[it])
            min_ratio_values.append(min(gr_ratios.T[it][gr_ratios.T[it]>0]))
            max_ratio_values.append(max(gr_ratios.T[it]))
        it += 1
            
    
    return inter_types, mean_ratio_values, num_ratio_values, min_ratio_values, max_ratio_values
'''

