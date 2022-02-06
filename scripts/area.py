#!/usr/bin/python
from matrix_init import *
from anatomy import femur_array
from anatomy import tibia_array

def get_joint_area(femur, tibia):
	
	def value_max_width_len(values):
		j = values[np.fromiter(map(len, values), int).argmax()]
		return j
		
	tibia_area = sum(np.sum(tibia, axis = 0))
	femur_area = sum(np.sum(femur, axis = 0))
	
	x, y = numpy_identity(tibia)
	xmax = value_max_width_len(x)
	length = len(xmax)
	quads = length // 4
	
	z = length // 20
	chunk = z * 2
	quad_a = quads + xmax[0]
	quad_a_0 = quad_a - z
	quad_a_1 = quad_a + z
	_quad_1_points = [i for i in range(quad_a_0, quad_a_1 + 1)]

	half_point = xmax[0] + length // 2
	half_point_0 = half_point - z
	half_point_1 = half_point + z
	_half_points = [i for i in range(half_point_0, half_point_1 + 1)]
	
	quad_b = abs(quads - xmax[-1])
	quad_b_0 = quad_b - z
	quad_b_1 = quad_b + z
	_quad_3_points = [i for i in range(quad_b_0, quad_b_1 + 1)]

	y_qa = y[quad_a][0]
	y_qa_0 = y[quad_a_0][0]
	y_qa_1 = y[quad_a_1][0]
	_y_qa = [y[x][0] for x in _quad_1_points]
	
	y_qb = y[quad_b][0]
	y_qb_0 = y[quad_b_0][0]
	y_qb_1 = y[quad_b_1][0]
	_y_qb = [y[x][0] for x in _quad_3_points]

	y_half = y[half_point][0]
	y_half_0 = y[half_point_0][0]
	y_half_1 = y[half_point_1][0]
	_y_half = [y[x][0] for x in _half_points]

	_, y = numpy_identity(femur)
	
	if y[quad_a_0].size > 0:
		yfqa0 = y[quad_a_0][-1]
	else:
		yfqa0 = 0
	
	yfqa = []
	for x in _quad_1_points:
		
		if y[x].size > 0:
			yfqa.append(y[x][-1])
		else:
			yfqa.append(0)
   
	yfha = [y[x][-1] for x in _half_points]

	yfqb = []
	for x in _quad_3_points:
		
		if y[x].size > 0:
			yfqb.append(y[x][-1])
		else:
			yfqb.append(0)
   
	_y_qa.reverse()
	yfqa.reverse()
 
	_a = []
	for i in range(len(_y_qa)):
		if yfqa[i] != 0:
			_a.append(abs(_y_qa[i] - yfqa[i]))
		else:
			_a.append(abs(_y_qa[0] - yfqa[0]))
   	
	_a_area = sum(_a)
 
	_half = []
	for i in range(len(_y_half)):
		_half.append(abs(_y_half[i] - yfha[i]))
	
	_half_area = sum(_half)

	_b = []
	for i in range(len(_y_qb)):
		
		if yfqb[i] != 0:
			_b.append(abs(_y_qb[i] - yfqb[i]))
		else:
			_b.append(abs(_y_qb[0] - yfqb[0]))

	_b_area = sum(_b)
		
	_average_area = (_a_area + _b_area + _half_area) / 3

	femur_tibia_area = (femur_area + tibia_area)/2

	_a_area_normal = _a_area / femur_tibia_area
	_b_area_normal = _b_area / femur_tibia_area
	_half_area_normal = _half_area / femur_tibia_area
	_average_area_normal = _average_area / femur_tibia_area
		
	joint_area = {'quad_1_area': _a_area, 'quad_2_area':_half_area, 'quad_3_area':_b_area, "quad_all_area": _average_area, "quad_1_area_norm": _a_area_normal, "quad_2_area_norm":_half_area_normal, "quad_3_area_norm":_b_area_normal, "quad_all_area_norm":_average_area_normal, "femur_area":femur_area, "tibia_area":tibia_area, "all_area_average":femur_tibia_area, "all_area":femur_area+tibia_area, "length": chunk, "xmax":len(xmax)}
	
	return joint_area

##########################################################################################

path = sys.argv[1]
path = str(os.path.abspath(path)) + "/"

#get current date and time
x = datetime.datetime.now()
dateTimeStr = str(x)
date = dateTimeStr[:10]
time = dateTimeStr[11:-7]

name = "joint_area_" + date + "_" + time + ".csv"
fullname = path + name
print("... Attempting to write", fullname, "\n")

fname = path + sys.argv[2]

with open(fname, "r") as fd:
	lines = fd.read().splitlines()

col_list = ['quad_1_area', 'quad_2_area', 'quad_3_area', "quad_all_area", "quad_1_area_norm", "quad_2_area_norm", "quad_3_area_norm", "quad_all_area_norm", "femur_area", "tibia_area", "all_area_average", "all_area", "length", "xmax"]
	
df = data_init(col_list)

def runner(files, path, df):
    
    for f in files:
        input = path + f; print(input)
        image = Image.open(input)
        data = asarray(image)
        
        tibia = tibia_array(data)
        femur = femur_array(data)
        
    	tibia_area = area(tibia)
    	femur_area = area(femur)
    	areas = [tibia_area, femur_area]
        
        image_name = {'file': f}
        
        j = {**image_name, **areas}
        
        df = df.append(j, True)
        
    return df
    
data = runner(lines, path, df)
print(data)
# data.to_csv(fullname, index=False)
print("\n", fullname, "successfully written")
