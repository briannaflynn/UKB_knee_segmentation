#!/usr/bin/python

from matrix_init import *
from anatomy import femur_array
from anatomy import tibia_array

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

    unit_1 = vector_1 / np.linalg.norm(vector_1)
    unit_2 = vector_2 / np.linalg.norm(vector_2)

    dot = np.dot(unit_1, unit_2)
    angle = np.arccos(dot)

    degrees = np.rad2deg(angle)

    return angle, degrees
    
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
	mid_1 = t[t_idx]
	
	j = x[u]
	j_idx = len(j) // 2
	mid_2 = j[j_idx]
	
	return mid_1, w, mid_2, u

def get_vector_line(img_data):
    
    x1, y1, x2, y2 = get_polygon_range(img_data)

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
	print(femur, top_x, top_y, bottom_x, bottom_y)
	if femur == True:
		xval = bottom_x
	elif femur == False:
		xval = top_x
	
	return xval

def get_displacement(xval_1, xval_2):
	
	displacement = abs(xval_1 - xval_2)
	
	return displacement		

##########################################################################################

path = sys.argv[1]
path = str(os.path.abspath(path)) + "/"

#get current date and time
x = datetime.datetime.now()
dateTimeStr = str(x)
date = dateTimeStr[:10]
time = dateTimeStr[11:-7]

name = "ftangle_disp_" + date + "_" + time + ".csv"
fullname = path + name
print("... Attempting to write", fullname, "\n")

# textfile with list of names of files 
fname = path + sys.argv[2]

with open(fname, "r") as fd:
	lines = fd.read().splitlines()

col_list = ['file', 'ft_angle', 'displacement']

df = data_init(col_list)

def runner(files, path, df):
    
    for f in files:
        input = path + f; print(input)
        image = Image.open(input)
        data = asarray(image)
        
        tibia = tibia_array(data)
        femur = femur_array(data)
        
        x, y, xv, yv = get_vector_line(femur)
        x1, y1, xv1, yv1 = get_vector_line(tibia)
        
        fem = LinAlger(x, y, xv, yv)
        tib = LinAlger(x1, y1, xv1, yv1)
        
        fem_vec = fem.vector
        tib_vec = tib.vector
        
        ang = LinAlger.get_angle(tib_vec, fem_vec)
        ang = 180 - round(ang[1], 2)
        fx = get_disp_xval(femur)
        tx = get_disp_xval(tibia, femur=False)
        disp = get_displacement(fx, tx)
        
        vals = {'ft_angle':ang, 'displacement': disp}
                
        image_name = {'file': f}
        
        j = {**image_name, **vals}
        
        df = df.append(j, True)
        
    return df
    
data = runner(lines, path, df)
print(data)
data.to_csv(fullname, index=False)
print("\n", fullname, "successfully written")