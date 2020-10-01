# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 13:43:33 2018

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
import ssl
ssl._create_default_https_context = ssl._create_unverified_context



def getYcData(year):
    #url of page of interst
    CSVFILE = "Data/yield_curve_data_{}.csv".format(year)

    file = Path(CSVFILE)
    if not file.exists():
        site = "https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yieldYear&year={}".format(year)

        #define page
        page = urllib.request.urlopen(site)

        #define html
        soup = BeautifulSoup(page, features='lxml')

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

        '''
        Leaving this in for possible future statistical analysis use
        bondLengths = []
        for i in all_rows[0]:
            i = numericDate(i)
            bondLengths.append(i)
        '''
        for row in all_rows:
            if row=="":
                row.pop

        bondLengths = []
        for i in all_rows[0]:
            i = numeric_length(i)
            bondLengths.append(i)

        all_rows[0] = bondLengths

    
    #csv file  + datetime.now().strftime('%Y-%m-%d %H-%M-%S') + 

        with open(CSVFILE, "w") as csv_file:
            writer = csv.writer(csv_file, lineterminator = '\n')
            #writer.writeheader()
            writer.writerows(all_rows)
    
    
    return CSVFILE

#converts bond length to number of months
def numericDate(bondLength):
    if bondLength[-2:len(bondLength)]=='mo':
        months = bondLength[0]
    elif bondLength[-2:len(bondLength)]=='yr':
        months = int(bondLength[0:2])*12
    else:
        months = bondLength
    
    return months

#converts date to numberic day of year
def getDayOfYear(date):
    date = datetime.strptime(date, '%m/%d/%y')
    day = date.timetuple().tm_yday
    return day

def numeric_length(bondLength):
    if bondLength[-2:len(bondLength)]=='mo':
        months = bondLength[0]
    elif bondLength[-2:len(bondLength)]=='yr':
        months = int(bondLength[0:2])*12
    else:
        months = bondLength
    return months

def get_data(y1, y2):
    for y in range(y1, y2+1):
        print('Getting data for year', y)
        getYcData(y)


