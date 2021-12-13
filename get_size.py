#!/usr/bin/python
import PIL
import cv2 as cv
import pandas as pd
import numpy as np
import datetime
import sys

path = sys.argv[1]

x = datetime.datetime.now()
dateTimeStr = str(x)
date = dateTimeStr[:10]
time = dateTimeStr[11:-7]

name = "coordinates_" + date + "_" + time + ".csv"
fullname = path + name
print("... Attempting to write", fullname)
fname = path + "joint_space.txt"

d = pd.DataFrame(columns=['file', 'x','y'])

with open(fname, "r") as fd:
	lines = fd.read().splitlines()
 
def get_size(init_df, im_path_list):

  for i in im_path_list:
    print(i)
    img = PIL.Image.open(i)
    j = {'file': i, 'x': img.size[0], 'y': img.size[1]}
    assert [i for i in j.keys()] == [i for i in init_df.columns], "Init dataframe columns must match dictionary keys: file, x and y"
    init_df = init_df.append(j, ignore_index=True)

  return init_df

df = get_size(d, lines)
df.to_csv(fullname, index = False)
print(fullname, "successfully written")