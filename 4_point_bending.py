"""
Created on Tue Apr  7 16:58:33 2015
4 point beam deflection calculator for round tube
Assume symmetric loading
units are kg, N, m, Pa
@author: tom mulholland
"""
from math import pi as pi
P = 111 #1/2 of total load [N]
L = 1.83 # distance between supports
a = 0.0762 # distance between support and load (3")
E = 68.9E9 # elastic modulus of 6061-T6 aluminum
x = 1.83/2 # point of interest for deflection calculation
           # L/2 is max deflection, since loading is symmetric
Do = 0.01905 # outer diameter of tube (0.75")
#t = 0.000889 # thickness of tube (0.035")
t = 0.058*2.54/100 # thickness of tube (0.058")

# CALCULATIONS
I = pi/4*((Do/2)**4 - (Do/2-t)**4)

delta = (P*(L-a))/(6*L*E*I)*(L/(L-a)*(x-a)**3-x**3+(L**2-(L-a)**2)*x) + \
(P*a)/(6*L*E*I)*(L/a*(x-(L-a))**3-x**3+(L**2-a**2)*x)

print "The deflection is %f" % (delta*1000), " millimeters"
