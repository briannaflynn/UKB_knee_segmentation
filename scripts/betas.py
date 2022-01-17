#!/usr/bin/python

import pandas as pd
import sys

fname = sys.argv[1]
orientation = sys.argv[2]
data = pd.read_csv(fname)
outname = fname[:-7] + "norm_by_height.csv"
cols = ['q1.1', 'q1.2', 'q1.3', 'q2.1', 'q2.2', 'q2.3', 'q3.1', 'q3.2', 'q3.3', 'quad_1_av', 'quad_2_av', 'quad_3_av', 'quad_all_av']

def get_betas(df, orient):

	uni = df['x'].unique()
	
	def extract_est(id:str, uni):
		xdata = id + "_" + str(uni) + "_xmax_height.csv"
		xd = pd.read_csv("stats/" + xdata)	
		beta = xd.estimate.to_list()[1]
		return beta
	
	dataobj = []
	for u in uni:
		beta = None
	
		if orient == "right":
			beta = extract_est("r", u)
		else:
			beta = extract_est("l", u)
		
		data = df.loc[df['x'] == u]
		data = data.copy(deep=True)
		data['beta'] = beta
		dataobj.append(data)
		
	dataset = pd.concat(dataobj)
	
	return dataset
		
def multiply_by_betas(df, col_list):
	
	df = df.copy(deep=True)
	
	for z in col_list:
	
		df[z] = df[z].astype(float)
		name = z + "_norm"
		df[name] = df[z] * df["beta"]
	
	print(df)
	return df

betadata = get_betas(data, orientation)	
betadata = multiply_by_betas(betadata, cols)
betadata.to_csv(outname, index = False)
	
