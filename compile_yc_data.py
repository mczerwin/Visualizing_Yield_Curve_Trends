# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 12:29:19 2019

@author: mczerwinski
"""

import pandas as pd
import os
from datetime import datetime


def avgRates(df):
    #If the datatype condition is false, the .strip() will not be run so it won't throw an error on float types
    if isinstance(df['2'], str) and df['2'].strip() == 'N/A':
        return round((df['1'] + df['3'])/2, 2)
    else:
        return df['2']

def compile_data(start_year, end_year, fillgap = False):
    
    main_df = pd.DataFrame()
    years = range(start_year,end_year+1, 1)
    for i in years:
        df = pd.read_csv('Data/yield_curve_data_{}.csv'.format(i))
        df.set_index('Date',inplace=True)
        dfs =[main_df,df]
        main_df = pd.concat(dfs)

    if fillgap:
        float_cols = [x for x in main_df.columns if x != '2']
        for col in float_cols:
            main_df[col] = main_df[col].astype(float)

        main_df['2'] = main_df[['1', '2', '3']].apply(avgRates, axis = 1)
        main_df['2'] = main_df['2'].astype(float)



    #output to csv
    file_name = 'yc_data_' + str(start_year) + '_' + str(end_year)
    full_file_name = 'Data/'+file_name+'.csv'
    if os.path.exists(full_file_name):
        os.remove(full_file_name)
    main_df.to_csv(full_file_name)
    
    return main_df, full_file_name

def add_spy_data():
    yc_df = pd.read_csv('Data/all_slopes.csv')

    spy_df = pd.read_csv('Data/SPY.csv')

    yc_date = []
    spy_date = []

    for x in yc_df['Date'].tolist():

        if x[-3] == '/':
            x = datetime.strptime(x, '%m/%d/%y')
        else:
            x = datetime.strptime(x, '%m/%d/%Y').strftime('%m/%d/%y')
        yc_date.append(x)

    yc_df['Date1'] = yc_date

    for y in spy_df['Date'].tolist():
        y = datetime.strptime(y, '%Y-%m-%d')
        spy_date.append(y)



    spy_df['Date1'] = spy_date
    final_df_outer = spy_df.merge(yc_df, how='outer', on='Date1')
    # print(final_df.head(5))

    final_df_outer.to_csv('Data/final_out_join.csv')

    final_df_inner = spy_df.merge(yc_df, how='inner', on='Date1')
    final_df_inner.drop(columns = ['Date_x', 'Date_y'], inplace = True)
    final_df_inner.rename(columns = {'Date1': 'Date'}, inplace = True)
    file_name = 'SPY_YC_inner'
    final_df_inner.to_csv('Data/{}.csv'.format(file_name))
    return file_name