#!/usr/bin/python

import pandas as pd
from os.path import abspath
import numpy as np
import sys

pth = sys.argv[1] # path to imsize.csv input files
orient = sys.argv[2] # right, left or both
pct = sys.argv[3] #True or False if want to filter by 25th and 75th z-score percentiles
z_score = int(sys.argv[4]) # z_score i.e. 1, 2 or 3

if pct == "False":
	params = "_z" + str(z_score)
elif pct == "True":
	params = "_percentile"

l = pd.read_csv(abspath(pth + "left_imsize.csv"))
r = pd.read_csv(abspath(pth + "right_imsize.csv"))

def filter_x(data, percent = 0.01):

    df = data['x'].value_counts(normalize=True).to_frame()
    df.reset_index(level=0, inplace=True)
    df.columns = ['x', 'x_percentage_of_total']

    df = df[df['x_percentage_of_total'] >= percent]
    filtered_df = df.merge(data,)


    return filtered_df

def filter_z(data, xval:int, percentiles = "False", z_score = 3):

    def _z_score(y, mean, std):
        z = (y - mean) / std
        return z

    data = data.copy(deep=True)

    data = data[data['x'] == xval]
    me = data['y'].mean()
    sd = data['y'].std()
    z = [_z_score(y, me, sd) for y in data['y'].to_list()]

    data['y_z_score'] = z

    summary = data['y_z_score'].describe().to_list()
  
    if percentiles == "True":
        filtered_df = data[(data['y_z_score'] >= summary[4]) & (data['y_z_score'] <= summary[6])]
    else:
        neg_z_score = -1 * z_score
        filtered_df = data[(data['y_z_score'] >= neg_z_score) & (data['y_z_score'] <= z_score)]

    return filtered_df

# pth = "./"
# orient = "right"
# pct = False
# z_score = 3

def _filter_all(df, pct, z):

    data = []
    d = filter_x(df)
    for x in d['x'].unique():
        df = filter_z(d, x, percentiles = pct, z_score = z)
        data.append(df)
    
    filtered_df = pd.concat(data)

    return filtered_df

data = []
if orient == "right":
    filtered_dataframe = _filter_all(r, pct, z_score)

elif orient == "left":
    filtered_dataframe = _filter_all(l, pct, z_score)

elif orient == "both":
    right_fltr = _filter_all(r, pct, z_score)
    left_fltr = _filter_all(l, pct, z_score)
    filtered_dataframe = pd.concat([right_fltr, left_fltr])

outname = pth + orient + params + "_imsize_filtered.csv"
print("Writing", outname)
filtered_dataframe.to_csv(outname, index = False)

'''
# Left data frame

### Dataset sizes before and after filtering:
*   Original size - 39757
*   After 1% filter on x - 39118

### With 1% filter on x values:
*   After filtering y for within 3 z-scores of mean (99.7%) - 38204
*   After filtering y for within 2 z-scores of mean (95%) - 36535
*   After filtering y for within 1 z-score of mean (68%) - 31584
*   After filtering y to between 25th and 75th percentiles - 22970


# Right data frame

### Dataset sizes before and after filtering:
*   Original size - 39745
*   After 1% filter on x - 39146

### With 1% filter on x values:
*   After filtering y for within 3 z-scores of mean (99.7%) - 38140
*   After filtering y for within 2 z-scores of mean (95%) - 36582
*   After filtering y for within 1 z-score of mean (68%) - 31476
*   After filtering y to between 25th and 75th percentiles - 23896

'''