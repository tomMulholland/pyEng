# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 00:08:00 2016
Random Walks in 3D
@author: tom
"""

import numpy as np
import random
from matplotlib import pyplot


random.seed(42)

N = (1, 3, 10, 32, 100, 320, 1000)    #number of steps
average_walks = [0]*len(N)
for j in range(0, len(N)):
    sign = (-1, 1) 
    step = (np.array([1, 0, 0]),
            np.array([0, 1, 0]),
            np.array([0, 0, 1]))
    total_trials = 1000
    walk_total = 0
    num_steps = N[j]
    for t in range(0, total_trials): #run 100 trials to find average number of required walks
        R_sq_avg = 0  #average R_squared distance
        alpha = 0     #initialize alpha
        num_walks = 0 #initialize number of walks of N steps already taken
        while(alpha < 0.99 or alpha > 1.01):
            current_pos = np.array([0,0,0])  #starting position
            for i in range(1, num_steps + 1): #for i from 1 to N steps
                direction = random.choice(sign)  #direction to move
                axis = random.choice(step)       #axis to move on
                current_pos = current_pos + (direction * axis)  #new position
            R_squared = (np.linalg.norm(current_pos))**2 #find magnitude of radius from origin
            R_sq_avg = (R_sq_avg * num_walks + R_squared) / (num_walks + 1)
            num_walks = num_walks + 1                     #number of walks of N steps already taken
            alpha = np.log(R_sq_avg)/np.log(num_steps)
        walk_total = walk_total + num_walks
    average_walks[j] = walk_total / total_trials


# PLOT
pyplot.plot(N, average_walks)
pyplot.show()
pyplot.ylabel('Average number of walks to show alpha = 1')
pyplot.xlabel('Number of Steps per Walk N')
pyplot.text(10, 20, '1000 Trials Conducted at each N')
pyplot.xscale('log')
pyplot.savefig("Random_3D_Walks_MORE_WALKS.png", format='png', dpi=450)

print(average_walks)
#average_walks = [1.0, 58.831, 35.652, 25.288] for 1000 total_trials

#average_walks = [1, 44, 77, 44, 39, 30, 25] with N
# N = (1, 3, 10, 32, 100, 320, 1000)
