#!/usr/bin/python

import pandas as pd
import sys
import numpy as np

input=sys.argv[1]
fname = pd.read_csv(input)
outpath = sys.argv[2]
l = input.split("/")[-1]
print(l)
type = l.split("_")[0]
val1 = fname.shape[0]
wba = pd.read_csv("../../data/fid_data/21000_wba_only.csv")
wba = wba[['eid']]
fname = wba.merge(fname, on = 'eid')
val2 = fname.shape[0]
wba_diff = val1 - val2
right_raw = pd.read_csv('../../data/pre-processed/raw/right/joint_space_10_2021-11-30_15:32:09_CLEANED.csv')
left_raw = pd.read_csv('../../data/pre-processed/raw/left/joint_space_10_2021-11-18_12:48:10_CLEANED.csv')

# Removing the outliers
def remove_outliers(data, col, outliers = False):
    Q3 = np.quantile(data[col], 0.75)
    Q1 = np.quantile(data[col], 0.25)
    IQR = Q3 - Q1

    lower_range = Q1 - 1.5 * IQR
    upper_range = Q3 + 1.5 * IQR
    
    outlier_free_list = [x if ((x > lower_range) & (x < upper_range)) else None for x in data[col]]
    
    outlier_list = [x if ((x < lower_range) & (x > upper_range)) else None for x in data[col]]
    
    files = None
    if outliers == False:
    	files = outlier_free_list
    elif outliers == True:
    	files = outlier_list
    	#print(files)
    
    return files

data = fname[["file", "x", "y", "xmax"]].to_dict('list')

cols = ['q1.1', 'q1.2', 'q1.3', 'q2.1', 'q2.2', 'q2.3', 'q3.1', 'q3.2', 'q3.3', 'quad_1_av', 'quad_2_av', 'quad_3_av', 'quad_all_av']

def outlier_processing(data, cols, type:bool):
	
	for col in cols:
		data[col] = remove_outliers(fname, col, type)
	df = pd.DataFrame(data)
	return df

outliers_df = outlier_processing(data, cols, True)
no_outliers_df = outlier_processing(data, cols, False)

columns = ['quad_1_av', 'quad_2_av', 'quad_3_av', 'quad_all_av']

def get_count(data, columns, raw, val1, val2):
	
	wba_diff = val1 - val2
	counts = {}
	counts['starting'] = raw.shape[0]
	counts['wba_only'] = val2
	counts['wba_diff'] = wba_diff
	counts['filter_x'] = raw.shape[0] - val1
	for c in columns:
		col = c + "_iqr"
		#print(data.dropna(subset=[c]).shape[0])
		counts[col] = data.dropna(subset=[c]).shape[0]
	print(counts)	
	count_data = pd.DataFrame(counts, index=[1])
	return count_data
	
if type == "right":
	count_data = get_count(no_outliers_df, columns, right_raw, val1, val2)
	
elif type == "left":
	count_data = get_count(no_outliers_df, columns, left_raw, val1, val2)

count_data.to_csv(type + "_joint_space_1pct_x_z3_y_iqr_counts.csv", index = False)
no_outliers_df.to_csv(outpath + type + "_no_outliers.csv", index = False)
outliers_df.to_csv(outpath + type + "_outliers.csv", index = False)

