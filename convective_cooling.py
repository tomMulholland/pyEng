"""
A script to numerically solve for the temperature profile in a cylinder 
in cross flow with transient convective heat loss
@author: tomMulholland
23-April-2014
"""

from scipy.optimize import minimize
import numpy as np
from scipy.special import jn # Bessel function of the first kind
import matplotlib
from matplotlib import pyplot
from time import gmtime, strftime

def roots(x):
    return((x*numpy.tan(x)+2-1)**2)
    
def roots_zeta(x, Bi):
    # We will do a minimization of the equation (should equal zero)
    # squared, to eliminate negative numbers
    return((x*jn(1, x) / jn(0, x) - Bi)**2)

def C_n_func(x):
    return((2/x) * jn(1, x) / (jn(0, x)**2 + jn(1, x)**2))
    

start_time = (strftime("%Y-%m-%d %H:%M:%S", gmtime()))

# DEFINE CONSTANTS
D = 0.004 # diameter of cylinder [m]
k_cyl = 0.16 # thermal conductivity of cylinder (polypropylene) [W/m-K]
alpha_cyl = 7.30167E-08
T_inf = 28
T_initial = 250
T_final_surface = 40
total_time = 150
mesh = 2000
round_to = 4

# CONSTANTS FOR AIR
v = 1 # velocity 2 [m/s]
nu = 15.89E-6 # dynamic viscosity of air at 26 °C [m**2/s]
Pr = 0.707 # Prandtl number of air at 26 °C [-]
k_air = 26.3E-3 # thermal conductivity of air at 26 °C [W/m-K]
n_Pr = 0.37 # exponent for Prandtl number
Pr_350 = .697 # Prandtl number of air at 77 °C [-]
Pr_400 = 0.690 # Prandtl number of air at 127 °C [-]
Pr_450 = 0.686 # Prandtl number of air at 177 °C [-]
Re = v*D/nu # Reynold's number

# check that Reynold's number is in the range of known interpolations
if (40 <= Re and Re <= 1000):
    m = 0.5 #exponent for Reynold's number
    C = 0.51 # coefficient to calculate Nusselt
elif (1000 < Re and Re <= 2E5):
    m = 0.6 
    C = 0.26 
elif (2E5 < Re and Re <= 2E6):
    m = 0.7
    C = 0.076
else:
    raise IndexError("Reynold's number outside range")

Nusselt = C*(Re**m)*(Pr**n_Pr)*(Pr/Pr_450)**(1/4) # Nusselt number [-]
h_avg = Nusselt * k_air / D # convective heat transfer coefficient [W/m**2-K]
Bi = h_avg * (D/2) / k_cyl

# SOLVE FOR ROOTS
initial = np.linspace(0,200, num=mesh)
answer = np.zeros((mesh, 1))

for i in range(len(answer)):
    answer[i] = minimize(roots_zeta, initial[i], 
                         args = (Bi,)).x
    if (i % 100 == 0):
        print("Run " + str(i) + " of " + str(len(answer)))
        print("Working.......")


# GET UNIQUE ROOTS
zeta = np.array([])
for number in answer:
    if roots_zeta(number, Bi) < 0.1:
        if number.round(round_to) not in zeta.round(round_to):
            if number > 0:
                zeta = np.append(zeta, number)
                

# COEFFICIENTS FOR THE EXACT SOLUTION
C_n = C_n_func(zeta) # Equation coefficients
Fourier = alpha_cyl / (D/2)**2 * np.linspace(0,total_time, num=total_time+1) # Fourier number
r_dim = np.linspace(0, 1, num=11) # Dimensionless radius
T = [] # a list of temperature data corresponding to the various radii

# CALCULATE TEMPERATURE RESULTS AT VARIOUS r
for r in r_dim:
    theta_partial = np.array([])
    
    for i in range(len(zeta)):
        result = C_n[i] * np.exp(-1*zeta[i] * Fourier) * jn(0, zeta[i]*r)
        theta_partial = np.append(theta_partial, [[result]])
                
    theta_partial.shape = (len(zeta), total_time+1)
    theta = np.zeros((1, total_time+1))
    for partial in theta_partial:
        theta = theta + partial
        
                
    T.append(theta * (T_initial - T_inf) + T_inf)

# CHECK SURFACE TEMPERATURE
surface_temp = T[len(r_dim)-1][0]
condition = (surface_temp < T_final_surface + 0.5) * \
  (surface_temp > T_final_surface - 0.5)
result = np.extract(condition, surface_temp)
index = np.where(surface_temp == result[0])
time_to_final_temp = int(time[index])

# FINAL ANSWER
print("It takes " + str(time_to_final_temp) + \
" seconds to reach a surface " +\
"temperature of {0:.1f}".format(float(surface_temp[index])) + \
" °C")

# PERFORMANCE
end_time = (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print("Start Time: " + start_time)
print("End Time: " + end_time)

# PLOT RESULTS
time = np.linspace(0,total_time, num=total_time+1)
for i in range(len(T)):
    pyplot.plot(time, T[i][0], label=("r* = " + str(r_dim[i])))

pyplot.legend()
pyplot.show()
pyplot.savefig("cylinder_cooling1.png", format='png', dpi=450)
