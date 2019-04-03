# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 19:45:17 2019

@author: mczerwinski
"""

import pandas as pd
import numpy as np
from pathlib import Path

def main():
    
    df_coeffs = pd.DataFrame()
    for i in range(1993,2020,1):
        print(i)
        csv_file  = Path("Data/yield_curve_clean_{}.csv".format(i))
        df = pd.read_csv(csv_file)
        df.set_index('Date',inplace=True)
        df_coeff = get_stats(df)
        df_coeff.drop(df.columns.difference(['a','b','c','d']), 1, inplace=True)
        
        coeffs= [df_coeffs,df_coeff]
        df_coeffs = pd.concat(coeffs)
        
    if not Path('all_coeffs.csv').exists():
        df_coeffs.to_csv('all_coeffs.csv')
        
def get_stats(df):
    
    #comment 24 and 25 out
    #df = pd.read_csv('Data/yield_curve_clean_1993.csv')
    #df.set_index('Date',inplace=True)
    data = df.values
    X = []
    for i in range(len(df.columns)):
        X.append(int(df.columns[i]))
    logX = np.log(X)
    Y = data.transpose()
    coeffs = np.polyfit(logX,Y,3)
   
    #coeffs = [a,b,c,d] for ax^3 + bx^2 + cx + d
   
    df['a'] = coeffs[0]
    df['b'] = coeffs[1]
    df['c'] = coeffs[2]
    df['d'] = coeffs[3]
    '''
    if not Path('Data/1993_coeffs.csv').exists():
        df.to_csv('Data/1993_coeffs.csv')
    '''
   
    return df


main()