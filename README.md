pyEng
=====

Scripts for some engineering problems

##convective_cooling.py
####Convective cooling of a cylinder in air crossflow
This script analyzes a hot, plastic cylinder being cooled by air at a certain velocity. The analytical equations are solved numerically (to avoid direct solution with an equation solver package). The equations were taken from Icropera, DeWitt, Bergman, and Lavine's textbook *Fundamentals of Heat and Mass Transfer*
Output is a graph of the cooling curves through the cylinder at the center and 1/10, 2/10...10/10 of the radius.

##coordinate_transform.py
####Rotate a coordinate system
This script was created to solve a problem in an injection molding simulation software. Local coordinate systems are defined in terms of the global system, and the local system needed to be rotated by some angle. The input are points which define the local origin, a point on the local x-axis, and a point on the local x-y plane. The output are these same points, rotated with respect to the local coordinate system, defined in the global coordinates.

##stiffness_matrix.py
####Orthotropic stiffness matrix and basic stress-strain calculation
This script helps the user define the 6x6 stiffness matrix of an orthotropic material. It also includes an example of the basic stress-strain calculation.
