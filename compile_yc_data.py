# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 12:29:19 2019

@author: mczerwinski
"""

import pandas as pd
import os


def avgRates(df):
    #If the datatype condition is false, the .strip() will not be run so it won't throw an error on float types
    if isinstance(df['2 mo'], str) and df['2 mo'].strip() == 'N/A':
        return round((df['1 mo'] + df['3 mo'])/2, 2)
    else:
        return df['2 mo']

def compile_data(start_year, end_year):
    
    main_df = pd.DataFrame()
    years = range(start_year,end_year+1, 1)
    for i in years:
        df = pd.read_csv('Data/yield_curve_data_{}.csv'.format(i))
        df.set_index('Date',inplace=True)
        dfs =[main_df,df]
        main_df = pd.concat(dfs)
    
    
    #dropping 2 month bond due to n/a data

    float_cols = [x for x in main_df.columns if x != '2 mo']
    print(float_cols)
    for col in float_cols:
        main_df[col] = main_df[col].astype(float)

    main_df['2 mo'] = main_df[['1 mo', '2 mo', '3 mo']].apply(avgRates, axis = 1)



    #output to csv
    file_name = 'Data/yc_data_' + str(start_year) + '_' + str(end_year)+'.csv'
    os.remove(file_name)
    main_df.to_csv(file_name)
    
    return file_name

compile_data(2015,2019)