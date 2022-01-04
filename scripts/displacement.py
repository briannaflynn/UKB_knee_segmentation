#!/usr/bin/python
from matrix_init import *
from anatomy import femur_array
from anatomy import tibia_array

def get_displacement(femur, tibia):

	def value_max_width_len(values):
		j = values[np.fromiter(map(len, values), int).argmax()]
		return j
		
	def half_pt(anatomy, type = 'tibia'):
		x, y = numpy_identity(anatomy)
		xmax = value_max_width_len(x)
		length = len(xmax)
		
		half_point_x = xmax[0] + length // 2
		half_point_y = y[half_point_x][0] # may also be negative one, check this
		if type == 'femur':
			half_point_y = y[half_point_x][-1]
		
		return half_point_x, half_point_y
		
	def normalize(*args, l):
		
		ans = []
		for a in args:
			an = a / l
			ans.append(an)
			
		return ans
		
	# tibia length for normalization
	length = len(value_max_width_len(numpy_identity(tibia)[0]))
	
	tx, ty = half_pt(tibia)
	fx, fy = half_pt(femur, type = 'femur')
	
	linear_dist = abs(fx - tx)
	tib = np.array((tx, ty))
	fem = np.array((fx, fy))
	euchlidian_dist = np.linalg.norm(tib - fem)
	
	norms = normalize(linear_dist, euchlidian_dist, l = length)
	
	distances = {'linear_distance': norms[0], 'euchlidian_distance': norms[1]}
	
	return distances
	
#########################################################################################

path = sys.argv[1]
path = str(os.path.abspath(path)) + "/"

#get current date and time
x = datetime.datetime.now()
dateTimeStr = str(x)
date = dateTimeStr[:10]
time = dateTimeStr[11:-7]

name = "displacement_" + date + "_" + time + ".csv"
fullname = path + name
print("... Attempting to write", fullname, "\n")

fname = path + sys.argv[2]

with open(fname, "r") as fd:
	lines = fd.read().splitlines()
	
col_list = ['file', 'linear_distance', 'euchlidian_distance']
df = data_init(col_list)

def runner(files, path, df):
    
    for f in files:
        input = path + f; print(input)
        image = Image.open(input)
        data = asarray(image)
        
        tibia = tibia_array(data)
        femur = femur_array(data)
        
        ds = get_displacement(femur, tibia)
        
        if ds['linear_distance'] >= 100:
        	f = "WARNING_" + f
        elif ds['euchlidian_distance'] >= 100:
        	f = "WARNING_" + f
        else:
        	pass
        
        image_name = {'file': f}
        
        j = {**image_name, **ds}
        
        df = df.append(j, True)
        
    return df
    
data = runner(lines, path, df)
data.to_csv(fullname, index=False)
print("\n", fullname, "successfully written")

	
	
	

	