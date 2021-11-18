#!/usr/bin/python
import json 
import os
from PIL import Image
import cv2
import numpy as np
from os import listdir
import argparse
from numpy import asarray
import sys
import pandas as pd
import datetime

def data_init(cols):
    
    df = pd.DataFrame()
    for i in range(len(cols)):
        c = cols[i]
        df[c] = None
        
    return df


def numpy_identity(matrix):
	
	rows = [i for i in range(len(matrix))] # get a list of indexes for all rows of the matrix
	
	columns = [j for j in range(len(matrix[0]))] # get a list of indexes for all columns of the matrix
	
	# convert the lists to numpy arrays
	r = np.array(rows)
	c = np.array(columns)


	def numpy2identity(matrix, index_array):
		
		mat = index_array * matrix # broadcast the array of indexes to all the arrays of the matrix, multiply together
		# will get matrix of 0s and the indexes
		
		mat = [n[n != 0] for n in mat] # remove all zeros, so now we have a matrix of arrays with either only indexes, or empty arrays
		# convert the list back into an array
		matrix = np.array(mat, dtype=object)
				
		return matrix
		
	x = numpy2identity(matrix, c) 
	
	trans_matrix = np.transpose(matrix) # transpose the matrix, so that the columns become the rows, and the rows become the columns
	y = numpy2identity(trans_matrix, r) # use the transposed matrix and the column index array to get y axis matrix

	return x, y
	
def tibia_array(image_array, femur = 1, tibia = 2, fibula = 3, patella = None):
	image_array = np.copy(image_array)
	np.place(image_array, image_array == femur, 0)
	
	if fibula != None:
		np.place(image_array, image_array == fibula, 0)
		
	if patella != None:
		np.place(image_array, image_array == patella, 0)
		
	np.place(image_array, image_array == tibia, 1)
		
	assert len(np.unique(image_array)) == 2, "Identity matrix did not get made, check the number of unique elements in input matrix. Number of elements must be > 2\n"
	
	return image_array

def femur_array(image_array, femur = 1, tibia = 2, fibula = 3, patella = None):
	image_array = np.copy(image_array)
	np.place(image_array, image_array == tibia, 0)
	
	if fibula != None:
		np.place(image_array, image_array == fibula, 0)
		
	if patella != None:
		np.place(image_array, image_array == patella, 0)
		
	np.place(image_array, image_array == femur, 1)
		
	assert len(np.unique(image_array)) == 2, "Identity matrix did not get made, check the number of unique elements in input matrix. Number of elements must be > 2\n"
	
	return image_array
	
def get_joint_space(femur, tibia):
	
	def value_max_width_len(values):
		j = values[np.fromiter(map(len, values), int).argmax()]
		return j
		
	x, y = numpy_identity(tibia)
	xmax = value_max_width_len(x)
	length = len(xmax)
	quads = length // 4
	
	quad_a = quads + xmax[0]
	half_point = xmax[0] + length // 2
	quad_b = abs(quads - xmax[-1])
	
	y_qa = y[quad_a][0]
	y_qb = y[quad_b][0]
	y_half = y[half_point][0]
	
	_, y = numpy_identity(femur)
	yfqa = y[quad_a][-1]
	yfha = y[half_point][-1]
	yfqb = y[quad_b][-1]
	
	_a = abs(y_qa - yfqa)
	_h = abs(y_half - yfha)
	_b = abs(y_qb - yfqb)
	
	_average = (_a + _h + _b) / 3
	
	def normalize(left, mid, right, av):
		
		a = left / length
		h = mid / length
		b = right / length
		average = av / length
		
		return a, h, b, average
		
	a, h, b, average = normalize(_a, _h, _b, _average)
	
	if average >= 100:
		print("\nWARNING: Need to supply femur, then tibia, or else calculations are off!\n")
		
	joint_space = {"quad_1" : a, "quad_2" : h, "quad_3" : b, "average": average, "not_normal_q1-q3": [_a, _h, _b], "not_normal_average": _average, "xmax": length}

	return joint_space

#########################################################################################

path = sys.argv[1]

#get current date and time
x = datetime.datetime.now()
dateTimeStr = str(x)
date = dateTimeStr[:10]
time = dateTimeStr[11:-7]

name = "joint_space_" + date + "_" + time + ".csv"
fullname = path + name
print("... Attempting to write", fullname)
fname = path + "joint_space.txt"

with open(fname, "r") as fd:
	lines = fd.read().splitlines()

col_list = ['file', 'quad_1', 'quad_2', 'quad_3', 'average', 'not_normal_q1-q3', 'not_normal_average', 'xmax']
df = data_init(col_list)

def runner(files, path, df):
    
    for f in files:
        input = path + f; print(input)
        image = Image.open(input)
        data = asarray(image)
        
        tibia = tibia_array(data)
        femur = femur_array(data)
        
        js = get_joint_space(femur, tibia)
        
        if js['average'] >= 100:
        	f = "WARNING_" + f
        elif js['not_normal_average'] >= 100:
        	f = "WARNING_" + f
        else:
        	pass
        
        image_name = {'file': f}
        
        j = {**image_name, **js}
        
        df = df.append(j, True)
        
    return df
    
data = runner(lines, path, df)
data.to_csv(fullname, index=False)
print(fullname, "successfully written")