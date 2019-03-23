# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 15:49:06 2019

@author: mczerwinski
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style


style.use('ggplot')


def visualize_data():
    
    df = pd.read_csv('Data/yc_data_2015_2019_sample.csv')
    
    #set row and column labels
    row_labels_df = df[df.index % 50 == 0]
    row_labels_df.set_index('Date', inplace = True)
    row_labels = row_labels_df.index
    
    
    #get data
    df.set_index('Date', inplace = True)
    data = df.values
    
    column_labels=df.columns
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_ylabel('Daily Treasury Yield Curve Rates', va="center",labelpad=-400,rotation=-90)
    heatmap = ax.pcolor(data, cmap = plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[1]) + 0.5, minor=False)  
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    plt.savefig('Yield_Curve_15_19.png')
    plt.show()


visualize_data()