#!/usr/bin/python

import pandas as pd
import sys

# example:
# python betas.py ../data/predictions/cleaned/1pct_x_z3_y_iqr/right/right_joint_space_xygroup_raw.csv right nonzero xy_group betas
# python betas.py ../data/predictions/cleaned/1pct_x_z3_y_iqr/right/right_joint_space_xygroup_raw.csv right zero xy_group betas
# example for ratio of betas: 
# python betas.py ../data/predictions/cleaned/1pct_x_z3_y_iqr/right/right_joint_space_xygroup_raw.csv right zero xy_group ratio
# fname is the source of your raw data, orientation is left right or both, type is zero or non zero intercept for betas calculation, 
# column is the name of the column in the dataframe corresponding to the grouping (by x coordinate, y coordinate, xy groups, etc), 
# ratio is to determine if multiplying raw values by betas, or if multiplying raw values by ratio of betas to each other

fname = sys.argv[1]
orientation = sys.argv[2]
type = sys.argv[3]
column = sys.argv[4]
ratio = sys.argv[5]
outname = fname[:-8] + type + "_norm_by_DXA_area.csv"
	
data = pd.read_csv(fname)

cols = ['quad_1_area', 'quad_2_area', 'quad_3_area', 'quad_all_area']
	
def get_betas(df, orient, col):

	uni = df[col].unique()
	
	def extract_est(id:str, uni, type):
		# example: xdata = id + "_" + str(uni) + "_xmax_height.csv"
		
		if type == "zero":
			xdata = id + "_" + str(uni) + "_zero_area.csv"
			xd = pd.read_csv("stats/" + xdata)
			beta = xd.estimate.to_list()[0]
			
		else:
			xdata = id + "_" + str(uni) + "_area.csv"
			xd = pd.read_csv("stats/" + xdata)
			beta = xd.estimate.to_list()[1]
		
		return beta
	
	dataobj = []
	for u in uni:
		beta = None
		
		if orient == "both":
			beta = extract_est("xy_groups", u, type)
		elif orient == "right":
			beta = extract_est("r", u, type)
		elif orient == "left":
			beta = extract_est("l", u, type)
		
		data = df.loc[df[col] == u]
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
		# changed to division
		df[name] = df[z] / df["beta"]
	
	print(df)
	return df
	
def multiply_by_ratio(data, col_list):

	betas = data['beta'].to_list()
	
	# if orientation == "right":
# 		data_A = data.loc[~data['xy_group'].str.startswith("B"), ]
# 		data_B = data.loc[data['xy_group'].str.startswith("B"), ]
# 		
# 	elif orientation == "left":
# 		data_A = data.loc[~data['xy_group'].str.startswith("G"), ]
# 		data_B = data.loc[data['xy_group'].str.startswith("G")]

	data_A = data.loc[data['AB_groups'].str.startswith("A"), ]
	data_B = data.loc[data['AB_groups'].str.startswith("B"), ]


	A = data_A['beta'].mean()
	B = data_B['beta'].mean()
	
	ratio_a = [y * (1 / B) for y in data_A.beta.to_list()]
	ratio_b = [y * (1 / A) for y in data_B.beta.to_list()]
	
	# to avoid SettingWithCopyWarning
	data_A = data_A.copy(deep=True); data_B = data_B.copy(deep = True)
	data_A["ratio"] = ratio_a
	data_B["ratio"] = ratio_b
	
	df = pd.concat([data_A, data_B])
	
	df = df.copy(deep=True)
	
	for z in col_list:
	
		df[z] = df[z].astype(float)
		name = z + "_norm"
		df[name] = df[z] * df["ratio"]
	
	print(df)
	return df
	
betadata = get_betas(data, orientation, column)	

if ratio == "ratio":
	betadata = multiply_by_ratio(betadata, cols)
	outname = fname[:-4] + "_" + type + "_" + ratio + "_norm_by_DXA_area.csv"
elif ratio == "betas" and column == "AB_groups":
	betadata = multiply_by_betas(betadata, cols)
	outname = fname[:-4] + "_" + type + "1.1_norm_by_DXA_area.csv"
else:
	betadata = multiply_by_betas(betadata, cols)

print(outname)
print(betadata.columns)
betadata.to_csv(outname, index = False)
	
