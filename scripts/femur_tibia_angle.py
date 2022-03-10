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
    x1, y1, x2, y2 = get_polygon_range(img_data)
    # print(x1, x2)
    # print(y1, y2)

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

# load the image
image = Image.open("../data/predictions/1.2.840.113619.2.110.210419.20150911150314.1.9.12.1_prediction.png")
# convert image to numpy array
femur = femur_array(asarray(image))
tibia = tibia_array(asarray(image))

#get_polygon_range(femur)
x, y, xv, yv = get_vector_line(femur)
x1, y1, xv1, yv1 = get_vector_line(tibia)

fem = LinAlger(x, y, xv, yv)
tib = LinAlger(x1, y1, xv1, yv1)

fem_vec = fem.vector
tib_vec = tib.vector

ang = LinAlger.get_angle(tib_vec, fem_vec)

print("The tibiofemoral angle is", 180 - round(ang[1]), "degrees" )

data = asarray(image)

d = np.where(data == 0, data, 255)

image = d
line_thickness = 2
cv2.line(image, (x, y), (xv, yv), (75, 0, 0), thickness=line_thickness)
cv2.line(image, (x1, y1), (xv1, yv1), (0, 0, 255), thickness=line_thickness)
# cv2.line(image, (439, 643), (441, 878), (0, 0, 255), thickness=line_thickness)
# cv2.circle(image, (439,643), radius=10, color=(0, 0, 255), thickness=2)
# cv2.circle(image, (441,878), radius=10, color=(0, 0, 255), thickness=2)
cv2.imshow(image)
#cv2.imwrite("test.png", image)

