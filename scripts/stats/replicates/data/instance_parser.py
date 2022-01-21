#!/usr/bin/python

import pandas as pd
import sys

type = sys.argv[1]
data_layout = sys.argv[2] # OPTIONS: stacked or long. Stacked means instance is represented in one column. Long means every variable is renamed based on the instance it belongs to. 
ifile = '_i2i3_filter.csv'

files = ['_joint_space.csv','_joint_space_zero_norm_by_height.csv','_joint_space_norm_by_height.csv','_joint_space_norm_by_ft_average.csv']
inst = pd.read_csv(type+ifile)

def parse_inst(inst):
	
	og = [x for x in inst.columns.to_list()]
	og.remove('eid')
	two = [x + "_2" for x in inst.columns.to_list()]
	two.remove('eid_2')
	
	three = [x + "_3" for x in inst.columns.to_list()]
	three.remove('eid_3')
	
	i2 = inst.loc[inst['instance'] == 2]
	i2 = i2.rename(columns = dict(zip(og, two)))
	
	i3 = inst.loc[inst['instance'] == 3]
	i3 = i3.rename(columns = dict(zip(og, three)))
	
	i23 = i2.merge(i3, on = "eid")
	
	return i23
	
for file in [type+z for z in files]:
    df = pd.read_csv(type+"/"+file)
    df['file'] = df['file'].str.replace("_prediction.png", ".jpg")
    
    if file == type + "_joint_space.csv":
    	df = df.merge(inst, on = "file")
    else:
    	df = df.merge(inst, on = ["file", "eid"])

    if data_layout == "stacked":
    	outfile = type+"/stacked_inst_" + file
    	df.to_csv(outfile, index=False)
    else:
    	outfile = type+"/long_inst_" + file
    	d = parse_inst(df)
    	d.to_csv(outfile, index=False)
    

