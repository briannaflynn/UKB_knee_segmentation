#!/usr/bin/python

import pandas as pd
import sys
import numpy as np

input=sys.argv[1]
fname = pd.read_csv(input)
outpath = sys.argv[2]
l = input.split("/")[-1]
print(l)
print(fname.shape[0])

# Removing the outliers
def remove_outliers(data, col):
    Q3 = np.quantile(data[col], 0.75)
    Q1 = np.quantile(data[col], 0.25)
    IQR = Q3 - Q1

    lower_range = Q1 - 1.5 * IQR
    upper_range = Q3 + 1.5 * IQR
    outlier_free_list = [x if ((x > lower_range) & (x < upper_range)) else None for x in data[col]]
    
    return outlier_free_list

data = fname[["file", "x", "y", "xmax"]].to_dict('list')
if l == "right_joint_space.csv" or "left_joint_space.csv":
	cols = ['quad_1_av', 'quad_2_av', 'quad_3_av', 'average']
else:
	cols = ['q1.1', 'q1.2', 'q1.3', 'q2.1', 'q2.2', 'q2.3', 'q3.1', 'q3.2', 'q3.3', 'quad_1_av', 'quad_2_av', 'quad_3_av', 'quad_all_av']

for col in cols:
	data[col] = remove_outliers(fname, col)

df = pd.DataFrame(data)
df = df.dropna()
df.to_csv(outpath + l, index = False)
