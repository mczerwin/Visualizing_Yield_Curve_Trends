# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 23:23:25 2019

@author: mczerwinski
"""

from datetime import datetime
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import os.path
from pathlib import Path
import math

def main(start,end):
    main_df = pd.DataFrame()
    slopes_df = pd.DataFrame()
    years = range(start,end+1, 1)    
    for i in years:
        print(i)
        CSVFILE = "Data/yield_curve_data_{}.csv".format(i)
        file = Path(CSVFILE)
        if not file.exists():
            getYcData(i)
        df = pd.read_csv(CSVFILE)
        df.set_index('Date',inplace=True)
        dfclean=drop_na_cols(df)
        cleanfile = 'Data/yield_curve_clean_{}.csv'.format(i)
        if not Path(cleanfile).exists():
            dfclean.to_csv(cleanfile)
            
        #method to get slopes of fits
        df_stats = get_stats(dfclean)
        df_stats.drop(dfclean.columns.difference(['log_slope']), 1, inplace=True)
        #compile all dataframes, but only columns date, and slope of log(length) vs rate
        data_df =[main_df,dfclean]
        main_df = pd.concat(data_df)
        
        slopes = [slopes_df,df_stats]
        slopes_df = pd.concat(slopes)
    main_df.to_csv('alldata.csv')
    slopes_df.to_csv('all_slopes.csv')
    
    
    
def drop_na_cols(df):
   # print(df[0,0])
    # i is rows
    drop_cols = []
    for i in df.columns:
        for x in df[i].tolist():
            try:
                x = float(x)
                if type(x) != float:
                    drop_cols.append(i)
                    break
            except:
                drop_cols.append(i)
                break
    dfnew = df.drop(columns = drop_cols)
    return dfnew


def get_stats(df):
   
   data = df.values
   X = []
   for i in range(len(df.columns)):
       X.append(int(df.columns[i]))
   logX = np.log(X)
   Y = data.transpose()
   slope,intercept = np.polyfit(X,Y,1)
   slope1,intercept1 = np.polyfit(logX,Y,1)
   
   df['log_slope'] = slope1
   
   return df
   
    
def getYcData(year):
    #url of page of interst
    site = "https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yieldYear&year={}".format(year)
    
    #define page
    page = urllib.request.urlopen(site)
    
    #define html
    soup = BeautifulSoup(page)
    
    writesoup = soup.encode("utf-8")
    
    html = soup.prettify()
    
    #name of html file  (optional)
    '''FILENAME = "Data\html_data" + datetime.now().strftime('%Y-%m-%d %H-%M-%S') + ".html"
    Html_file = open(FILENAME, "w")
    Html_file.write(str(writesoup))
    Html_file.close()'''
    
    #pull table of interest
    all_tables = soup.find_all('table')
    yield_table = soup.find('table',class_='t-chart')
   
    #create data
    all_rows = []
    for row in yield_table.find_all('tr'):
        data = []
        #print("row" + str(len(all_rows)))
        for elements in row.find_all('td'):
            data.append(elements.string)
        if len(data)!=0:
            all_rows.append(data)
        else:
            for elements in row.find_all('th'):
                data.append(elements.string)
            if len(data)!=0:
                all_rows.append(data)
    
    
    #Leaving this in for possible future statistical analysis use
    bondLengths = []
    for i in all_rows[0]:
        i = numeric_length(i)
        bondLengths.append(i)
    
    all_rows[0] = bondLengths
    for row in all_rows:
        if row=="":
            row.pop
            
    CSVFILE = "Data/yield_curve_data_{}.csv".format(year)
    file = Path(CSVFILE)
    if not file.exists():
    #csv file  + datetime.now().strftime('%Y-%m-%d %H-%M-%S') + 
    
        with open(CSVFILE, "w") as csv_file:
            writer = csv.writer(csv_file, lineterminator = '\n')
            #writer.writeheader()
            writer.writerows(all_rows)
    
    
    #return CSVFILE

#converts bond length to number of months
def numeric_length(bondLength):
    if bondLength[-2:len(bondLength)]=='mo':
        months = bondLength[0]
    elif bondLength[-2:len(bondLength)]=='yr':
        months = int(bondLength[0:2])*12
    else:
        months = bondLength
    
    return months

#converts date to numeric day of year, i.e. Feb 2 = 33
def getDayOfYear(date):
    date = datetime_object = datetime.strptime(date, '%m/%d/%y')
    day = date.timetuple().tm_yday
    return day

def add_spy_data():
    yc_df = pd.read_csv('all_slopes.csv')
    
    spy_df = pd.read_csv('Data/SPY.csv')
    
    yc_date = []
    spy_date = []
    
    for x in yc_df['Date'].tolist():
        
        if x[-3] =='/':
            x = datetime.strptime(x,'%m/%d/%y')
        else:
            x = datetime.strptime(x,'%m/%d/%Y').strftime('%m/%d/%y')
            print(x)
        yc_date.append(x)
        
    yc_df['Date1']=yc_date
    print('yc df formatted')


    print(yc_df['Date'])
    print('---------------------------------------------')
    print(yc_df['Date1'])
        
        
        
    for y in spy_df['Date'].tolist():
        y = datetime.strptime(y,'%m/%d/%Y').strftime('%m/%d/%y')
        spy_date.append(y)
    
    spy_df['Date1']=spy_date
    #(yc_df.set_index('Date',inplace=True)).join(spy_df.set_index('Date',inplace=True))
    
    
   # spy_df.set_index('Date',inplace=True)
    #yc_df.set_index('Date',inplace=True)
    
    final_df_outer = spy_df.merge(yc_df,how='outer', on = 'Date1')
    #print(final_df.head(5))
    
    final_df_outer.to_csv('final_out_join.csv')
    
    final_df_inner = spy_df.merge(yc_df,how='inner', on = 'Date1' )
    final_df_inner.to_csv('final_inner_join.csv')
    
    
def visualiz_trends():
    df= pd.read_csv('Data/Compiled_data.csv')
    df.set_index('Date',inplace=True)
    
    dates = df.index.values
    data1 = df['Adj. Close'].values
    data2 = df['yc_slope'].values
    
    fig, ax1 = plt.subplots()
    
    #set Left axis for SPY Adj. Close Price
    ax1.set_xlabel('Date')
    ax1.set_xticks(np.arange(0,df.shape[0],600))
    ax1.set_xticklabels(df.index[np.arange(0,df.shape[0],600)],rotation = 80)
    ax1.set_ylabel('SPY Adj. Close')
    ax1.plot(range(len(data1)),data1, color = 'green')
    
    #set right axis for slope of best fit line for Interest Rate vs. log(Bond length)
    ax2= ax1.twinx()
    ax2.set_ylabel('Best fit slope of Rate vs. log(Bond Length)')
    ax2.plot(range(len(data2)), data2, color = 'red')
    
    #Plot constant line at a flat Yield Curve for reference
    zero_line = np.array([0 for i in range(len(dates))])
    ax2.plot(range(len(data1)),zero_line,color = 'blue')
    
    
    plt.savefig('Yield_Curve_Trends_vs_SPY.png')
    plt.show()
    
visualiz_trends()
#main(1993,2019) 
#add_spy_data()
    

    
    