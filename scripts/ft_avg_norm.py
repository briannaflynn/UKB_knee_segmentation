#!/usr/bin/python

import pandas as pd
import sys

femur = sys.argv[1]
fname = sys.argv[2]
fem = pd.read_csv(femur)
f = pd.read_csv(fname)
outname = fname[:-7] + "norm_by_ft_average.csv"
data = f.merge(fem, on = "file")
cols = ['q1.1', 'q1.2', 'q1.3', 'q2.1', 'q2.2', 'q2.3', 'q3.1', 'q3.2', 'q3.3', 'quad_1_av', 'quad_2_av', 'quad_3_av', 'quad_all_av']

def normal_by_ft(dataframe):

	df = dataframe.copy(deep=True)
	name = "fem_tib_average"
	df[name] = df["femur_xmax"] + df["xmax"]
	df[name] = df[name] / 2
	
	for c in cols:
		n = c + "_norm"
		df[c] = df[c].astype(float)
		df[n] = df[c] / df[name]
	
	return df

df = normal_by_ft(data)
print(outname)	
print(df)

df.to_csv(outname, index=False)
