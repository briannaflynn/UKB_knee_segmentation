#!/usr/bin/python
from matrix_init import *
from anatomy import femur_array
from anatomy import tibia_array

class linalger:

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
    
