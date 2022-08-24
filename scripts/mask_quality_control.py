#!/usr/bin/python

from matrix_init import *
from anatomy import femur_array
from anatomy import tibia_array
import pandas as pd
import numpy as np
import sys
import os

# PROVIDE PATHS TO XY RESOLUTION DATAFRAME (XY_COVARIATE_LINKING_FILE), PATH TO FOLDER WITH IMAGES, AND NAME OF FILE
size = sys.argv[1] # ~/Desktop/UKB/UKB_knee_segmentation/data/tableau_data/xy_covariate_linking_file.csv'
pth = sys.argv[2]  # '/Users/brie/Desktop/UKB/UKB_knee_segmentation/data/predictions/'
#f = sys.argv[3] # '1.2.840.113619.2.110.210419.20150904160158.2.9.12.1_prediction.png'
files = []
for file in os.listdir(pth):
    if file.endswith("_prediction.png"):
    	files.append(file)
	
size_df = pd.read_csv(size)
dir_files = pd.DataFrame()
dir_files['file'] = files
files = size_df.merge(dir_files, on = 'file', how = 'inner')['file'].to_list()
print(files)

path = pth

def get_area_for_resolution(path, file, size_df):
	
	# modify the string so that can now grab the png with the mask 
	png_file = file
	file = png_file[:-15] + '.jpg'
	
	# determine each resolution group (i.e. by X coords)
	# get x and y coordinate information from table lookup
	#size = size_df[size_df['file'] == png_file, ][['x', 'y']]
	size = size_df.loc[size_df['file'] == png_file][['x', 'y']]
	size = size.to_dict('records')[0]
	
	input = path + png_file
	image = Image.open(input)
	
	data = asarray(image)
	
	tibia = tibia_array(data)
	femur = femur_array(data)
	
	tibia_area = np.sum(tibia)	
	femur_area = np.sum(femur)
	
	def value_max_width_len(values):
		j = values[np.fromiter(map(len, values), int).argmax()]
		return j

	def get_max(img_data):
		x, y = numpy_identity(img_data)
		ymax = value_max_width_len(y)
		xmax = value_max_width_len(x)
		return(len(xmax), len(ymax))
	
	fx, fy = get_max(femur)
	tx, ty = get_max(tibia)	
	
	data = {'file':file, 'mask':png_file, 'x': size['x'], 'y':size['y'], 'femur_area':femur_area, 'tibia_area':tibia_area, 'femur_xmax':fx, 'femur_ymax':fy, 'tibia_xmax':tx, 'tibia_ymax':ty}
	
	return data

# data is a dataframe produced from the dict produced by function: get_area_for_resolution
# bone is 'femur' or 'tibia' (string)	
def compute_statistics(data, bone='femur'):
	
	def _z_score(y, mean, std):
		z = (y - mean) / std
		return z
		
	def find_outliers(column, data):
		
		# get mean, sd, and z score
		data = data.copy(deep=True)
		me = data[column].mean()
		sd = data[column].std()
		z = [_z_score(y, me, sd) for y in data[column].to_list()]
		
		# add column with z score to dataframe
		zname = column + '_z_score'
		data[zname] = z
		
		# get z percentiles - 25th and 75th will be summary[4] and summary[6]
		summary = data[zname].describe().to_list()
		print(data[zname].describe())
		pname = column + '_summary'
		row_count = data.shape[0]
		rows = abs(row_count - len(summary))
		fill = [None] * rows
		
		summary = summary + fill
		
		data[pname] = summary
		
		return data
		
	xmax = find_outliers(bone+'_xmax', data)
	ymax = find_outliers(bone+'_ymax', xmax)
	area = find_outliers(bone+'_area', ymax)
			
	return area
	
def runner(path, files, size_df):
	
	keys = ['file', 'mask', 'x', 'y', 'femur_area', 'tibia_area', 'femur_xmax', 'femur_ymax', 'tibia_xmax', 'tibia_ymax']
	vals = [None] * len(keys)
	data_init = dict(zip(keys, vals))
	
	def append_data(dict, key, value):
		if not isinstance(dict[key], list):
			dict[key] = [dict[key]]
			dict[key].append(value)
		else:
			dict[key].append(value)
			
		return dict
	
	for f in files:
		
		data = get_area_for_resolution(path, f, size_df)
		for k, v in data.items():
			data = append_data(data_init, k, v)
		data_init = data
	
	data = pd.DataFrame.from_dict(data).dropna()
	
	results = compute_statistics(data)
	results = compute_statistics(results, bone = 'tibia')
	
	def compute_statistics_per_x(data, x):
		
		df = data.loc[data['x'] == x]
		x = int(x)
		results = compute_statistics(df)
		results = compute_statistics(results, bone = 'tibia')
		results.to_csv(path + 'seg_mask_qc_'+str(x)+'.csv', index = False)
		
		return results
	
	for xi in data['x'].unique():	
		compute_statistics_per_x(data, xi)

	return results

# GIVE FILE AS PNG 
quality_check = runner(path, files, size_df)
quality_check.to_csv(pth + "seg_mask_qc.csv", index = False)
