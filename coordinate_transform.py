"""
This script takes three points which are used to define a local coordinate 
system (CS) in a simulation software. The three points are rotated with respect
to the LCS at some angle. The three points, which produce a new LCS, are output
in the global CS (GCS).

local_origin is the origin of the LCS defined in the GCS

p_x is a point on the x-axis of the original LCS, defined in the GCS

p_xy is a point on the x-y plane in the original LCS, defined in the GCS

p_x_rot and p_xy_rot the rotations of p_x and p_xy by theta with respect to 
the LCS

rotate is the axis over which to do the rotation: 'x', 'y', or 'z'

theta is the angle *FROM THE NEW LCS TO THE ORIGINAL LCS*
Note: Pay attention to the positive or negative sign, especially at small angles 
which are difficult to visually verify.

local_origin, p_x_rot, and p_xy_rot are printed out, which are three points
which can be used to define the new, rotated LCS with respect to the GCS
"""

import numpy as np
from math import pi
from math import cos as cos
from math import sin as sin


## ORIGINAL LOCAL COORDINATE SYSTEM
# Defined by points in the global coordinate system
local_origin = np.array([427.421, 517.918, 3330.297])
# point on the x axis
p_x = np.array([336.977, 517.849, 3330.073])
# point on the x-y plane
p_xy = np.array([397.253, 525.524, 3341.374])


## ROTATION PARAMETERS
rotate = 'x'
theta = -72.7 * (pi / 180) # rotation angle in radians


## DEFINE COORDINATE SYSTEM
# x vector
local_x_axis = p_x - local_origin
# x unit vector
local_x_axis = local_x_axis / (sum(local_x_axis**2)**0.5)
local_z_axis = np.cross(local_x_axis, p_xy - p_x)
local_z_axis = local_z_axis / (sum(local_z_axis**2)**0.5)
local_y_axis = np.cross(local_z_axis, local_x_axis)
# local_y_axis already has unit length
local_CS = np.array([local_x_axis, local_y_axis, local_z_axis])
local_CS_inv = np.linalg.inv(local_CS)


# TESTS
# the point in the original local coordinate system
test_point = np.dot(local_CS, (p_x - local_origin))
test_point = np.dot(local_CS, (p_xy - local_origin))


## ROTATION MATRIX
if rotate == 'x':
    R_matrix = np.array([[1, 0, 0],
                        [0, cos(theta), -sin(theta)],
                        [0, sin(theta), cos(theta)]])
    print("Using x-axis rotation")                    
elif rotate == 'y':
    R_matrix = np.array([[cos(theta), 0, sin(theta)],
                        [0, 1, 0],
                        [-sin(theta), 0, cos(theta)]])
    print("Using y-axis rotation")
elif rotate == 'z':
    R_matrix = np.array([[cos(theta), -sin(theta), 0],
                        [sin(theta), cos(theta), 0],
                        [0, 0, 1]])
    print("Using z-axis rotation")                    
else:
    error_text = "Only Cartesian rotations are supported. Please choose " \
                    + "either x, y, or z"
    raise Exception(error_text)                  


## ROTATED POINTS
p_x_local = np.dot(local_CS, p_x - local_origin)
p_x_rot = local_origin + np.dot(local_CS_inv, np.dot(R_matrix, p_x_local))
p_xy_local = np.dot(local_CS, p_xy - local_origin)
p_xy_rot = local_origin + np.dot(local_CS_inv, np.dot(R_matrix, p_xy_local))


## PRINT ANSWERS
print("Origin (same as original): " + str(local_origin))
print("Point on the new axis: " + str(p_x_rot))
print("Point on the new x-y plane: " + str(p_xy_rot))
