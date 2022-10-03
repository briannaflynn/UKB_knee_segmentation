#!/usr/bin/python
import json 
import os
from PIL import Image, ImageOps
import cv2
import numpy as np
from os import listdir
import argparse
from numpy import asarray
import sys
import pandas as pd
import datetime
from scipy import stats

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

print('check complete')