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

# load the image
image = Image.open(sys.argv[1])
# convert image to numpy array
data = asarray(image)

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

def tibia_array(image_array, femur = 1, tibia = 2, fibula = None, patella = None):
  
  image_array = np.copy(image_array)
  np.place(image_array, image_array == femur, 0)
  if fibula != None:
    np.place(image_array, image_array == fibula, 0)
  if patella != None:
    np.place(image_array, image_array == patella, 0)

  np.place(image_array, image_array == tibia, 1)

  if len(np.unique(image_array)) != 2:
    print("\nIdentity matrix did not get made, check the number of unique elements in input matrix. Number of elements must be > 2\n") 
 
  assert len(np.unique(image_array)) == 2

  return image_array

def femur_array(image_array, femur = 1, tibia = 2, fibula = None, patella = None):
  
  image_array = np.copy(image_array)
  np.place(image_array, image_array == tibia, 0)
  if fibula != None:
    np.place(image_array, image_array == fibula, 0)
  if patella != None:
    np.place(image_array, image_array == patella, 0)

  np.place(image_array, image_array == femur, 1)

  if len(np.unique(image_array)) != 2:
    print("\nIdentity matrix did not get made, check the number of unique elements in input matrix. Number of elements must be > 2\n") 
 
  assert len(np.unique(image_array)) == 2

  return image_array

# def value_max_width_len(values):
#   j = values[np.fromiter(map(len, values), int).argmax()] # use this to get the longest array from an array of arrays
#   return j

def get_joint_space(femur, tibia):
  
  def value_max_width_len(values):
    j = values[np.fromiter(map(len, values), int).argmax()] # use this to get the longest array from an array of arrays
    return j
    
  x, y = numpy_identity(tibia)
  xmax = value_max_width_len(x)
  length = len(xmax)
  quads = length//4

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

  a = abs(y_qa - yfqa)
  h = abs(y_half - yfha)
  b = abs(y_qb - yfqb)

  average = (a + h + b) / 3

  if average >= 100:
    print("\nWARNING: Need to supply femur, then tibia, or else calculations are off!\n")

  joint_space = {"quad_1" : a, "quad_2" : h, "quad_3" : b, "average": average}

  return joint_space

tibia = tibia_array(data)
femur = femur_array(data)

get_joint_space(femur, tibia)

