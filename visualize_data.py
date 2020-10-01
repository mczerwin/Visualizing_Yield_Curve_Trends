# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 15:49:06 2019

@author: mczerwinski
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import style
from pylab import meshgrid


style.use('ggplot')


def visualize_data(file):
    print('Visualizing data for', file)
    df = pd.read_csv(file)

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
    plt.savefig('Images/heatmap_{}.png'.format(file[6:len(file)-4]))
    plt.show()


def visualize_trends(file):
    df = pd.read_csv('Data/{}.csv'.format(file))
    df.set_index('Date', inplace=True)
    df = df[df['slope'] != 'None']
    df['slope'] = df['slope'].astype(float)

    dates = df.index.values
    data1 = df['Adj Close'].values
    data2 = df['slope'].values

    fig, ax1 = plt.subplots()

    # set Left axis for SPY Adj. Close Price
    ax1.set_xlabel('Date')
    ax1.set_xticks(np.arange(0, df.shape[0], 600))
    ax1.set_xticklabels(df.index[np.arange(0, df.shape[0], 600)], rotation=80)
    ax1.set_ylabel('SPY Adj. Close')
    ax1.plot(range(len(data1)), data1, color='green')

    # set right axis for slope of best fit line for Interest Rate vs. log(Bond length)
    ax2 = ax1.twinx()
    ax2.set_ylabel('Best fit slope of Rate vs. log(Bond Length)')
    ax2.plot(range(len(data2)), data2, color='red')

    # Plot constant line at a flat Yield Curve for reference
    zero_line = np.array([0 for i in range(len(dates))])
    ax2.plot(range(len(data1)), zero_line, color='blue')

    plt.savefig('Images/Yield_Curve_Trends_vs_SPY.png')
    plt.show()

def view_surface(df):
    cols = ['1','2','3','6','12','24','36','60','84','120','240','360']
    x = np.array([int(i) for i in cols])
    logx = np.log(x)
    y = np.flip(np.arange(0, len(df)))
    X, Y = meshgrid(logx, y)  # grid of point
    Z = np.flip(df[cols].to_numpy())
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap=cm.RdBu)
    ax.view_init(azim=20)

    # # ax.zaxis.set_major_locator(LinearLocator(5))
    ax.set_xlabel('Natural Log of Bond Length')
    ax.set_ylabel('Date')
    plt.show()
#
# view_surface(pd.read_csv('Data/cubic_fit.csv'))