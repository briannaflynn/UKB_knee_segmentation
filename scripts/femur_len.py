#!/usr/bin/python
from matrix_init import *
from anatomy import femur_array
from anatomy import tibia_array

path = sys.argv[1]
path = str(os.path.abspath(path)) + "/"

#get current date and time
x = datetime.datetime.now()
dateTimeStr = str(x)
date = dateTimeStr[:10]
time = dateTimeStr[11:-7]

def value_max_width_len(values):
	j = values[np.fromiter(map(len, values), int).argmax()]
	return j
		
name = "femur_length_" + date + "_" + time + ".csv"
fullname = path + name
print("... Attempting to write", fullname, "\n")

fname = path + sys.argv[2]

with open(fname, "r") as fd:
	lines = fd.read().splitlines()

def runner(files, path):
    xmaxes = []; count = 0
    for f in files:
        input = path + f
        count += 1
        perc = count / len(files) * 100
        print(input, perc)
        image = Image.open(input)
        data = asarray(image)
        
        femur = femur_array(data)
        x, y = numpy_identity(femur)
        xmax = len(value_max_width_len(x))
        xmaxes.append(xmax)
       
    df = pd.DataFrame({'file': files, 'femur_xmax': xmaxes})
    return df
    
data = runner(lines, path)
print(data)
data.to_csv(fullname, index=False)
print("\n", fullname, "successfully written")