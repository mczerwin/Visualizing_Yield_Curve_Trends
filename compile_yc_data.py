# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 12:29:19 2019

@author: mczerwinski
"""

import pandas as pd

def compile_data(start_year, end_year):
    
    main_df = pd.DataFrame()
    years = range(start_year,end_year+1, 1)
    for i in years:
        df = pd.read_csv('Data/yield_curve_data_{}.csv'.format(i))
        df.set_index('Date',inplace=True)
        dfs =[main_df,df]
        main_df = pd.concat(dfs)
    
    
    #dropping 2 month bond due to n/a data
    main_df.drop(['2 mo'], axis = 1,inplace = True )
    
    #output to csv
    file_name = 'Data/yc_data_' + str(start_year) + '_' + str(end_year)+'.csv'
    main_df.to_csv(file_name)
    
    return file_name

compile_data(2015,2019)