# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 12:58:35 2019

@author: mczerwinski
"""
import pandas as pd

def sample_data(df, name):
    df_new = df.iloc[::3]
    
    print('Data reduced from', df.shape[0], 'rows to', df_new.shape[0], 'rows.')

    file = name[:len(name) - 4] + '_sample.csv'
    print('Sampled data filename:', file)
    df_new.to_csv(file)
    return df_new, file

