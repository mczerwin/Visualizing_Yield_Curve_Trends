# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 12:58:35 2019

@author: mczerwinski
"""
import pandas as pd

def sample_data():
    
    df = pd.read_csv('Data/yc_data_2015_2019.csv')
    
    df.set_index('Date', inplace = True)
    df_new = df.iloc[::3]
    
    print(df_new.shape)
    
    df_new.to_csv('Data/yc_data_2015_2019_sample.csv')
    
sample_data()
