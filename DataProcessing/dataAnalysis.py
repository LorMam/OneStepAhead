import csv
import os,sys

import numpy as np
from datetime import date
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
from dataProcessing import inData

from sklearn.linear_model import LinearRegression

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

#Function to find the number of days between two dates
def days_diff(date1,date2):
    
    d1info = date1.split("-")
    d2info = date2.split("-")
    d1 = date(int(d1info[0]), int(d1info[1]), int(d1info[2]))
    d2 = date(int(d2info[0]),int(d2info[1]),int(d2info[2]))
    delta = d2 - d1
    
    return(delta.days)


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
    #Read in data file 
    df = inData(inputfile)
    
    date100 = df[country][df["Days since 100"] == daystart]
    
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
        print("Insufficient data for",country)
        return 0., 0., 0.
    
    #Mask to only consider days with data
    dayend = days100[np.argmax(cases100)]
    mask = mask & (days100 < dayend) & (cases100 > 0.)

    #Adjust if date range is specified
    if daterange:
        mask = (days100 > daystart) & (days100 < dayend)
    
    #Check for sufficient data points:
    if len(cases100[mask]) < 5:
        print("Insufficient data for",country)
        return 0., 0., 0.
    
    #Perform a linear fit to the data
    popt, pcov = curve_fit(linear_fit, days100[mask],np.log10(cases100[mask]))
    chi2 = chisquare(cases100[mask],10.**(days100[mask]*popt[0] + popt[1]))

    inflection_date = 0.
    logchi2 = 0
    #Need minimum number of approx. ten days for a logistic fit
    if len(days100[mask]) > 15.:
        #Perform a logistic fit to the data
        try:
            log_fit, log_cov = curve_fit(logistic_model,days100[mask],cases100[mask],
                                 p0=[2.5,1,max(cases100[mask])],maxfev=1200)
            logchi2 = chisquare(cases100[mask],logistic_model(days100[mask],*log_fit))
            
            inflection_date = log_fit[1]
        except RuntimeError:
            print("Logistic function fit failed for",country)
            
            
    if ((chi2 < logchi2) or (inflection_date > max(days100[mask])) or not inflection_date) and not (inter_date > 5):
        growthrate = popt[0]
        print("linear fit preferred for",country,"growth rate",growthrate)
        return growthrate, 0., inflection_date

    if (logchi2 < chi2) and (inflection_date < max(days100[mask])):
        print("logistic fit preferred for",country)
        print("inflection date",inflection_date)
    
        #Alternatively, calculate pre and post intervention date:
    if inter_date > 5.:
        mask1 = mask & (days100 < inter_date)
        mask2 = mask & (days100 > inter_date)
    else:
        #Perform linear fits pre and post inflection date to compare growth rates
        mask1 = mask & (days100 < inflection_date)
        mask2 = mask & (days100 > inflection_date)


    growthrate = 0.
    growthrate2 = 0.
    
    #Check for sufficient data points:
    if sum(mask1) > 5:
        popt, pcov = curve_fit(linear_fit, days100[mask1],np.log10(cases100[mask1]))
        chi2 = chisquare(cases100[mask1],10.**(days100[mask1]*popt[0] + popt[1]))
        growthrate = popt[0]
    
    if sum(mask2) > 5:
        popt2, pcov2 = curve_fit(linear_fit, days100[mask2],np.log10(cases100[mask2]))
        chi2_2 = chisquare(cases100[mask2],10.**(days100[mask2]*popt2[0] + popt2[1]))
        growthrate2 = popt2[0]
        
    if inter_date > 5:
        print("intervention date",inter_date)
        return growthrate, growthrate2, inter_date
    
    return growthrate, growthrate2, inflection_date


#Function to read in interventions and investigate
#Input:
#datefile = csv format countries & intervention dates
#country_file = days since 100 cases , total number of cases, csv format
def intervention_analysis(datefile,country_file):

    df = inData(datefile)
    
    gr_ratios = np.zeros(df.shape)
    num_ratios = np.zeros(df.shape[1])
    
    inter_types = []
    itt = 0
    for col in df.columns:
        if not (col=="Country") and itt % 2:
            inter_types.append(col)
        itt += 1
    print(inter_types)
    
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
                print("Obtaining Growth rate for",country,date)
                igr = ObtainGrowthRate(country_file,country,True,date)
                print("Intervention Date",date,"growth rate before=",igr[0],"growth rate after = ",igr[1])
                
                if igr[0] and igr[1]:
                    gr_ratios[row[0]][cnt] = igr[1]/igr[0]
                    num_ratios[cnt] += 1
                    
            cnt += 1
            
    #meanratios = np.mean(gr_ratios.T)
    
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


