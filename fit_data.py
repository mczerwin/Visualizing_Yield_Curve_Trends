import pandas as pd
import numpy as np
from pathlib import Path


def fit_data(df, degree = 1):

    if degree == 1:
        df['slope'] = df.apply(get_slope, axis = 1)
        return df

    elif degree == 3:
        df = df.apply(get_cubic_fit, axis = 1)
        return df


def get_slope(df):
    x = []
    y = []
    for i in range(1, len(df.values)):
        val = df.values[i]
        if not (isinstance(val, str) and val.strip() == 'N/A'):
            y.append(float(val))
            x.append(int(df.index[i]))
    if min(len(x), len(y)) == 0:
        return 'None'
    x = np.log(x)
    slope, intercept = np.polyfit(x, y, 1)
    return slope


def get_cubic_fit(df):
    x = []
    y = []
    for i in range(1, len(df.values)):
        val = df.values[i]
        if not (isinstance(val, str) and val.strip() == 'N/A'):
            y.append(float(val))
            x.append(int(df.index[i]))
    if min(len(x), len(y)) == 0:
        return 'None'
    x = np.log(x)
    coeffs = np.polyfit(x, y, 3)

    # coeffs = [a,b,c,d] for ax^3 + bx^2 + cx + d
    df['a'] = coeffs[0]
    df['b'] = coeffs[1]
    df['c'] = coeffs[2]
    df['d'] = coeffs[3]

    return df

