# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 11:47:08 2019

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
import matplotlib.patches as mpatch


def visualiz_trends():
    df= pd.read_csv('Data/cubic_coeffs_w_spy.csv')
    df.set_index('Date',inplace=True)
    
    dates = df.index.values
    data1 = df['SPY'].values
    data2 = df['a'].values
    data3 = df['b'].values
    data4 = df['c'].values
    data5 = df['d'].values
    
    fig, ax1 = plt.subplots()
    
    #set Left axis for SPY Adj. Close Price
    #ax1.set_xlabel('Date')
    ax1.set_xticks(np.arange(0,df.shape[0],600))
    ax1.set_xticklabels(df.index[np.arange(0,df.shape[0],600)],rotation = 80)
    ax1.set_ylabel('SPY')
    SPY_adj_close = ax1.plot(range(len(data1)),data1, color = 'green')
    
    #set right axis for slope of best fit line for Interest Rate vs. log(Bond length)
    ax2= ax1.twinx()
    ax2.set_ylabel('Cubic Coeffs.')
    a_line = ax2.plot(range(len(data2)), data2, color = 'red')
    
    b_line = ax2.plot(range(len(data3)), data3, color = 'purple')
    
    c_line = ax2.plot(range(len(data4)), data4, color = 'orange')
    
    d_line = ax2.plot(range(len(data5)), data5, color = 'blue')
    
    #Plot constant line at a flat Yield Curve for reference
    zero_line = np.array([0 for i in range(len(dates))])
    ax2.plot(range(len(data1)),zero_line,color = 'black')
    
    #plt.legend([SPY_adj_close, a_line, b_line, c_line, d_line],['SPY Adj. Close','a','b','c','d'])
    
    SPY_patch = mpatch.Patch(color = 'green',label = 'SPY Adj. Close')
    a_patch = mpatch.Patch(color = 'red',label = 'a coeff.')
    b_patch = mpatch.Patch(color = 'purple',label = 'b coeff.')
    c_patch = mpatch.Patch(color = 'orange',label = 'c coeff.')
    d_patch = mpatch.Patch(color = 'blue',label = 'd coeff.')
    
    plt.legend(handles = [SPY_patch,a_patch,b_patch,c_patch,d_patch,])
    plt.savefig('Yield_Curve_cubic_coeffs_vs_SPY.png')
    plt.show()
    
visualiz_trends()