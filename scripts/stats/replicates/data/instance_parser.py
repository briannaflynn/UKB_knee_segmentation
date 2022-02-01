#!/usr/bin/python

import pandas as pd
import sys

# example: Use Quotes for Third Argument 
# python instance_parser.py right long "right_joint_space_zero_norm_by_height.csv right_joint_space_norm_by_height.csv"
# python instance_parser.py right stacked "right_joint_space_zero_norm_by_height.csv"
# python instance_parser.py left long "left_joint_space_zero_norm_by_height.csv left_joint_space_norm_by_height.csv left_joint_space_norm_by_ft_average.csv"

type = sys.argv[1] # right or left
data_layout = sys.argv[2] # OPTIONS: stacked or long. Stacked means instance is represented in one column. Long means every variable is renamed based on the instance it belongs to. 
ifile = '_i2i3_filter.csv'

f = sys.argv[3] # string containing filenames separated by spaces (or one filename) with double quotes
files = f.split(" ")

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
	
for file in files:
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
    	outfile = type+"/inst_" + file
    	d = parse_inst(df)
    	print(d); print(outfile)
    	d.to_csv(outfile, index=False)
    