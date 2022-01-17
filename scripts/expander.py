#!/usr/bin/python

import pandas as pd
import sys

f = sys.argv[1]
#df = pd.read_csv("/Users/brie/Desktop/UKB/UKB_knee_segmentation/data/predictions/cleaned/1pct_x_z3_y/right/right_joint_space.csv")
df = pd.read_csv(f)
fl = f.split("/")[-1]

outname = fl[:-4] + "_raw.csv"
pth = f.replace(fl, outname)

def list_2_rows(dataframe):
	
	df = dataframe[['file', 'not_normal_q1-q3']]
	f = df['file'].to_list()
	nn = df['not_normal_q1-q3'].to_list()
	nn = [x[1:-1] for x in nn]
	
	NN = []
	for n in nn:
		ln = n.split(", ")
		NN.append(ln)
	
	data = {'file':f}
	klist = ['q1.1', 'q1.2', 'q1.3', 'q2.1', 'q2.2', 'q2.3', 'q3.1', 'q3.2', 'q3.3']
	for i in range(9):
		l = [float(x[i]) for x in NN]
		k = klist[i]
		data[k] = l
	
	d = pd.DataFrame(data)
	
	d['quad_1_av'] = d[['q1.1', 'q1.2', 'q1.3']].mean(axis=1)
	d['quad_2_av'] = d[['q2.1', 'q2.2', 'q2.3']].mean(axis=1)
	d['quad_3_av'] = d[['q3.1', 'q3.2', 'q3.3']].mean(axis=1)
	d['quad_all_av'] = d[klist].mean(axis=1)
	
	return d

expanded_df = list_2_rows(df)
print(expanded_df)
print(pth)
expanded_df.to_csv(pth, index=False)