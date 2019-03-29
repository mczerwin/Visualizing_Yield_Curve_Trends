# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 09:42:26 2019

@author: mczerwinski
"""
import numpy as np
import matplotlib.pyplot as plt



def visualize_best_fits():
    
    '''
    10/03/2003
    Positive sloping Yield Curve
    '''
    x_03 = [1,3,6,12,24,36,60,84,120,240]
    log_x_03 = np.log(x_03)
    #10/03/2003
    y_03 = [0.87,0.94,1.01,1.2,1.65,2.17,3.12,3.69,4.21,5.15]
    slope_03,intercept_03 = np.polyfit(log_x_03,y_03,1)
   
    y_03_plt = [0.87,10,0.94,1.01,1.2,1.65,2.17,3.12,3.69,4.21,5.15,10]
    
    plt.figure(1)
    plt.plot(log_x_03,y_03,'o',color = 'red')
    
    best_fit_03 = [slope_03*x + intercept_03 for x in log_x_03]
    plt.plot(log_x_03,best_fit_03,color = 'red')
    
    xlabels03 = [months_to_years(x) for x in x_03]
   
    plt.xticks(log_x_03,xlabels03,rotation = 80)
    plt.xlabel('Bond Lenghths in Months(Logarithmic Scale)')
    
    plt.ylabel('Interest Rate')
    plt.ylim(bottom=0)
    
    plt.title('Treasury Rates as of Oct 3, 2003')
    plt.savefig('10032003_bestfit.png')
    plt.show()
    
    
    '''
    03/05/2007
    Negative sloping Yield Curve
    '''
    x_07 = [1,3,6,12,24,36,60,84,120,240,360]
    log_x_07 = np.log(x_07)
    
   
    #03/05/2007
    y_07 = [5.22,5.1,5.08,4.89,4.53,4.47,4.45,4.46,4.51,4.74,4.64]
    slope_07,intercept_07 = np.polyfit(log_x_07,y_07,1)
    
    best_fit_07 = [slope_07*x + intercept_07 for x in log_x_07]
    
    plt.figure(2)
    plt.plot(log_x_07,y_07,'o',color = 'blue')
    plt.plot(log_x_07,best_fit_07,color = 'blue')
    
    xlabels07 = [months_to_years(x) for x in x_07]
    plt.xticks(log_x_07,xlabels07,rotation = 80)
    plt.xlabel('Bond Lenghths in Months(Logarithmic Scale)')
    
    plt.ylabel('Interest Rate')
    plt.ylim(bottom=0,top=6)
    
    plt.title('Treasury Rates as of Mar 5, 2007')
    plt.savefig('03052007_bestfit.png')
    plt.show()
    
    '''
    03/29/2019
    Current Yield Curve
    '''
    
    x_19 = [1,2,3,6,12,24,36,60,84,120,240,360]
    log_x_19 = np.log(x_19)
    
    #03/29/2019
    y_19 = [2.44,2.45,2.43,2.44,2.40,2.23,2.18,2.20,2.29,2.39,2.62,2.81]
    slope_19,intercept_19 = np.polyfit(log_x_19,y_19,1)
    best_fit_19 = [slope_19*x + intercept_19 for x in log_x_19]
   
    plt.figure(3)  
    plt.plot(log_x_19,y_19,'o',color = 'green')
    plt.plot(log_x_19,best_fit_19,color = 'green')
    
    
    xlabels19 = [months_to_years(x) for x in x_19]
    plt.xticks(log_x_19,xlabels19,rotation = 80)
    plt.xlabel('Bond Lenghths in Months(Logarithmic Scale)')
    
    plt.ylabel('Interest Rate')
    plt.ylim(bottom=0)
    
    plt.title('Treasury Rates as of Mar 29, 2019')
    plt.savefig('03292019_bestfit.png')
    plt.show()
    
    
    
def months_to_years(mo):
    if mo%12==0:
        return str(int(mo/12)) + ' yr'
    else:
        return str(mo) + ' mo'
    
    
visualize_best_fits()
