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

def get_joint_space(femur, tibia):
	
	def value_max_width_len(values):
		j = values[np.fromiter(map(len, values), int).argmax()]
		return j
		
	x, y = numpy_identity(tibia)
	xmax = value_max_width_len(x)
	length = len(xmax)
	quads = length // 4
	
	z = length // 20
	quad_a = quads + xmax[0]
	quad_a_0 = quad_a - z
	quad_a_1 = quad_a + z
	
	half_point = xmax[0] + length // 2
	half_point_0 = half_point - z
	half_point_1 = half_point + z
	
	quad_b = abs(quads - xmax[-1])
	quad_b_0 = quad_b - z
	quad_b_1 = quad_b + z
	
	y_qa = y[quad_a][0]
	y_qa_0 = y[quad_a_0][0]
	y_qa_1 = y[quad_a_1][0]
	
	y_qb = y[quad_b][0]
	y_qb_0 = y[quad_b_0][0]
	y_qb_1 = y[quad_b_1][1]
	
	y_half = y[half_point][0]
	y_half_0 = y[half_point_0][0]
	y_half_1 = y[half_point_1][0]
	
	_, y = numpy_identity(femur)
	
	if y[quad_a_0].size > 0:
		yfqa0 = y[quad_a_0][-1]
	else:
		yfqa0 = 0
	
	yfqa = y[quad_a][-1]
	yfqa1 = y[quad_a_1][-1]
	
	yfha = y[half_point][-1]
	yfha0 = y[half_point_0][-1]
	yfha1 = y[half_point_1][-1]
	
	if y[quad_b_1].size > 0:
		yfqb1 = y[quad_b_1][-1]
	else:
		yfqb1 = 0
	
	yfqb = y[quad_b][-1]
	yfqb0 = y[quad_b_0][-1]
	
	_a = abs(y_qa - yfqa)
	_a1 = abs(y_qa_1 - yfqa1)

	if yfqa0 != 0:
		_a0 = abs(y_qa_0 - yfqa0)
	else:
		_a0 = _a + _a1 / 2
		
	_h = abs(y_half - yfha)
	_h0 = abs(y_half_0 - yfha0)
	_h1 = abs(y_half_1 - yfha1)
	
	_b = abs(y_qb - yfqb)
	_b0 = abs(y_qb_0 - yfqb0)
	
	if yfqb1 != 0:
		_b1 = abs(y_qb_1 - yfqb1)
	else:
		_b1 = _b + _b0 / 2

	_average = (_a + _a0 + _a1 + _h + _h0 + _h1 + _b + _b0 + _b1) / 9
	
	def normalize(*args):
		
		ans = []
		for a in args:
			an = a / length
			ans.append(an)
			
		return ans
				
	norms = normalize(_a, _a0, _a1, _h, _h0, _h1, _b, _b0, _b1, _average)
	
	a = (_a + _a0 + _a1) / 3
	b = (_h + _h0 + _h1) / 3
	c = (_b + _b0 + _b1) / 3
	
	if _average >= 100:
		print("\nWARNING: Need to supply femur, then tibia, or else calculations are off!\n")

	joint_space = {"quad_1_av": a, "quad_2_av": b, "quad_3_av": c, "average": _average, 'x_value_half':half_point, 'y_value_0':y_half, 'y_value_1':yfha, 'y_value_half':yfha + (_h0 // 2)}

	return joint_space

class LinAlger:

  def __init__(self, x_1, y_1, x_2, y_2):
    self.x1 = x_1
    self.x2 = x_2
    self.y1 = y_1
    self.y2 = y_2

    def vectorize(x1, y1, x2, y2):
      a = np.array([x1, y1])
      b = np.array([x2, y2])

      c = b - a
      return c

    self.vector = vectorize(self.x1, self.y1, self.x2, self.y2)
  
  def get_angle(vector_1, vector_2):

    ang1 = np.arctan2(*vector_1)
    ang2 = np.arctan2(*vector_2)
    ang = np.rad2deg(ang1-ang2) #+ 180
    
    return ang
    
def get_polygon_range(img_data, scale_val = 5):
	def value_max_width_len(values):
		j = values[np.fromiter(map(len, values), int).argmax()]
		return j
		
	def value_min_width_len(values):
		x = np.fromiter(map(len, values), int).argmin()
		z = values[x]
		return x, z
		
	x, y = numpy_identity(img_data)
	ymax = value_max_width_len(y)
	xmax = value_max_width_len(x)
	
	bottom = ymax[-1]
	top = ymax[0]
	height = bottom - top
	
	u = bottom - height // scale_val
	w = top + height // scale_val
	
	t = x[w]
	t_idx = len(t) // 2
	
	if t.size == 0:
		mid_1 = None
	else:
		mid_1 = t[t_idx]
	
	j = x[u]
	j_idx = len(j) // 2
	
	if j.size == 0:
		mid_2 = None
	else:
		mid_2 = j[j_idx]
	
	return mid_1, w, mid_2, u

def get_vector_line(img_data, x1, y1, x2, y2):
    
    #x1, y1, x2, y2 = get_polygon_range(img_data)

    l = LinAlger(x1, y1, x2, y2)
    vector = l.vector
    ymax, xmax = img_data.shape
    xd = vector[0]
    yd = vector[1]
    yvar = ymax // 10
    xvar = xmax // 10
    
    x1_ = x1 - (xvar*xd)
    y1_ = y1 - (yvar*yd)
    x2_ = x2 + (xvar*xd)
    y2_ = y2 + (yvar*yd)
    return x1_, y1_, x2_, y2_
    
def get_disp_xval(img_data, femur = True):
	
	xval = None
	top_x, top_y, bottom_x, bottom_y = get_polygon_range(img_data)
	
	if femur == True:
		xval = bottom_x
	elif femur == False:
		xval = top_x
	
	return xval

def get_disp_values(img_data, femur = True):
	
	xval = None
	top_x, top_y, bottom_x, bottom_y = get_polygon_range(img_data)
	
	if femur == True:
		values = [bottom_x, bottom_y]
	elif femur == False:
		values = [top_x, top_y]
	
	return values

def get_displacement(xval_1, xval_2):
	
	displacement = abs(xval_1 - xval_2)
	
	return displacement		

# provide a list of start minus end of array (differences)
# if return none, probably need to just discard the mask altogether or hand check it
def iter_x(diffs, threshold=0.25):

        med = np.median(diffs)
        # print(med)
        # print(med + med * threshold)
        # print(med - med * threshold)

        value = None; index = None
        for j in range(len(diffs)):
            i = diffs[j]
            # print(i)
            # print(i >= (med + med * threshold))
            # print(i <= (med - med * threshold))
            if i >= (med + med * threshold) or i <= (med - med * threshold):
                pass
            else:
                print('Take measurement', i)
                value = i
                index = j
                break

        if value == None or index == None:
            print('No index returned. Check descriptive statistics: Median=' + str(med), stats.describe(diffs))
            return None
        else:
            return index

def get_anchor(femur, tibia):
    
    def value_max_width_len(values):
        j = values[np.fromiter(map(len, values), int).argmax()]
        return j

    femur_x_array, femur_y_array = numpy_identity(femur)
    tibia_x_array, tibia_y_array = numpy_identity(tibia)

    def get_idx(x_array, y_array, sample = 20, femur=True):

        x_array = [x for x in x_array if x != []]
        ymax = value_max_width_len(y_array)

        if femur == True:
            x = x_array[0:sample]
            diffs = [abs(i[-1] - i[0]) for i in x]
            measurement_index = iter_x(diffs)
            fe_diff = abs(x_array[measurement_index][0] - x_array[measurement_index][-1])//2
            xval = x_array[measurement_index][0] + fe_diff
            yval = ymax[measurement_index]
        else:
            sample = -1 * sample
            x = x_array[sample:]
            diffs = [abs(i[-1] - i[0]) for i in x]
            measurement_index = iter_x(diffs[::-1])
            measurement_index = -1 * (measurement_index + 1)
            te_diff = abs(x_array[measurement_index][0] - x_array[measurement_index][-1])//2
            xval = x_array[measurement_index][0] + te_diff
            yval = ymax[measurement_index]

        return {'x':xval, 'y':yval, 'index':measurement_index}

    femur_vals = get_idx(femur_x_array, femur_y_array, sample = 25)
    tibia_vals = get_idx(tibia_x_array, tibia_y_array, sample=25, femur = False)

    return {'fx': femur_vals['x'], 'fy': femur_vals['y'], 'fidx':femur_vals['index'], 'tx': tibia_vals['x'], 'ty': tibia_vals['y'], 'tidx':tibia_vals['index']}

def runner(files, path, df):
    for f in files:
        input = path + f; print('\n' + input)
        image = Image.open(input)
        data = asarray(image)

        tibia = tibia_array(data)
        femur = femur_array(data)

        fx1, fy1, fx2, fy2 = get_polygon_range(femur)
        tx1, ty1, tx2, ty2 = get_polygon_range(tibia)

        if None in [fx2, tx1]:
            disp = None
        else:
            femur_dx, femur_dy = get_disp_values(femur)
            tibia_dx, tibia_dy = get_disp_values(tibia, femur = False)

            disp = get_displacement(femur_dx, tibia_dx)

        # print('\nDisplacement -')
        # print('Femur x, y:', femur_dx, femur_dy, '\nTibia x, y:', tibia_dx, tibia_dy)
        # print('Middle of Displacement X:', (femur_dx + tibia_dx) // 2)
        mid_x = (femur_dx + tibia_dx) // 2

        js = get_joint_space(femur, tibia)
        mid_y = js['y_value_half']

        anch = get_anchor(femur, tibia)
        print(anch)
        
        fx, fy, tx, ty = anch['fx'], anch['fy'], anch['tx'], anch['ty']
        cx = mid_x
        cy = mid_y

        if None in [fx, fy, tx, ty, cx, cy]:
            ang = None
        else:
            x, y, xv, yv = get_vector_line(femur, fx, fy, cx, cy)
            x1, y1, xv1, yv1 = get_vector_line(tibia, tx, ty, cx, cy)

            fem = LinAlger(x, y, xv, yv); tib = LinAlger(x1, y1, xv1, yv1)
            fem_vec = fem.vector; tib_vec = tib.vector

            ang = LinAlger.get_angle(tib_vec, fem_vec)
            ang = round(ang,6)
            if ang < 0:
                ang = ang + 360
            print("Angle:", ang)

        d = np.where(data == 0, data, 255); image = d
        line_thickness = 2
        cv2.circle(image, (fx, fy), 5, (100, 0, 0), thickness=5)
        cv2.circle(image, (cx, cy), 5, (100, 0, 0), thickness=5)
        cv2.circle(image, (tx, ty), 5, (100, 0, 0), thickness=5)
        cv2.line(image, (x, y), (xv, yv), (75,0,0), thickness=2)
        cv2.line(image, (x1, y1), (xv1, yv1), (75,0,0), thickness=2)
        cv2.imwrite(input[:-4] + '_center_axis_angle.png', image)
        print(input[:-4] + '_center_axis_angle.png', 'successfully written')

        vals = {'file': f, 'tibiofemoral_angle': ang}
        df = df.append(vals, True)

    return df

# path to the directory containing the annotations
path = sys.argv[1]
path = str(os.path.abspath(path)) + "/"
# textfile with list of names of files 
fname = path + sys.argv[2]

x = datetime.datetime.now()
dateTimeStr = str(x)
date = dateTimeStr[:10]
time = dateTimeStr[11:-7]

name = "tibiofemoral_angle_center_axis_" + date + "_" + time + ".csv"
fullname = path + name
print("... Attempting to write", fullname, "\n")

with open(fname, "r") as fd:
	lines = fd.read().splitlines()

col_list = ['file', 'tibiofemoral_angle']
df = data_init(col_list)    
data = runner(lines, path, df)
print(data)
