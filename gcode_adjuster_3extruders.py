# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 21:23:24 2017

@author: Tom

In order to precisely control the toolpath on an FFF part, the part was subdivided into 3 pieces.
Using Slic3r or another common slicer, each piece can be sliced with its own set of parameters by 'pretending' the printer has 3 different extruders.
Then, the user can delete the tool changes. However, the slicer tries to minimize tool changes, so each layer starts with a different piece.
In order to begin each layer with the same piece, the Gcode must be reorganized.
This script finds the tool changes and layer changes, then reorganizes based on each case.
After reorganization, it's possible that the code tries to print with the filament in the "retracted" state.
The script checks for this and corrects it. After correction, the Gcode is rechecked.
"""

#import os
import time
import tkinter as tk
from tkinter import filedialog
#from math import isclose
from bisect import bisect_left

def get_tool_changes(gcode_array):
    layer_change=[]
    tool = [] #indices where tool changes occur
    tool_num = [] #the tool invoked at those indices
    tool0 = [] #indices where tool0 is invoked
    tool1 = [] #indices where tool1 is invoked
    tool2 = [] #indices where tool2 is invoked
    layer_code = [] #indices for comments that begin with ";Layer"
    for i in range(len(gcode_array)):
        if gcode_array[i][2:7] == "Layer":
            layer_change.append(i)
        if gcode_array[i][0:2] == "T0":
            tool.append(i)
            tool0.append(i)
            tool_num.append("T0")
            layer_code.append(0)
        if gcode_array[i][0:2]== "T1":
            tool.append(i)
            tool_num.append("T1")
            tool1.append(i)
        if gcode_array[i][0:2]== "T2":
            tool.append(i)
            tool_num.append("T2")
            tool2.append(i)
    del layer_change[0] #delete Layer0 index, for ease of use
    del tool[0]
    del tool0[0]
    del tool_num[0]
    return [layer_change, tool, tool_num, tool0, tool1, tool2, layer_code]

# Adjust these values

retraction = 1 #[mm] retraction length
priming = 1 #[mm] prime length
remove_tool_change = True #[mm] should tool changes (T0, T1, T2) be removed?
#extruders = 3 #[-] how many extruders?
#layer_height = 0.1 #[mm] primary layer height
#tool1_z_offset = 0
#tool2_z_offset = 0
#tool0_xy_offset = 0

#*************************************************
#os.chdir('C:/Users/Tom/Documents/Python Scripts')

#Prompt for a .gcode file with a Open File window
root = tk.Tk()
root.withdraw()
filename = filedialog.askopenfilename()

start = time.time()

f = open(filename, "r")
lines = f.readlines()
f.close()

#Get all the indices and tool callouts
layer_change, tool, tool_num, tool0, tool1, tool2, layer_code = get_tool_changes(lines)

print(str(len(lines)) + " lines at start")
##### Add tool changes after every line change
#For all layer changes, add line number to tool and label to tool_num
additional_lines = 0
for i in range(len(layer_change)):
    ind = bisect_left(tool, layer_change[i])
    tool.insert(ind, layer_change[i])
    tool_num.insert(ind, tool_num[ind-1])
    lines.insert(layer_change[i]+i+1, tool_num[ind]+"\n")
    additional_lines += 1

print(str(len(lines)) + " lines after")  
##### Redefine indices with new line numbers
layer_change, tool, tool_num, tool0, tool1, tool2, layer_code = get_tool_changes(lines)
gcode = [] 
gcode.extend(lines[0:layer_change[0]])

#check order on all layers except last layer
for i in range(0, len(layer_change)-1):
    
    lo = "" #layer order string
    ind0 = bisect_left(tool, layer_change[i]) #Find index of first tool change in layer
    ind1 = bisect_left(tool, layer_change[i+1])-1 #Find index of last line before tool change in layer
    
    # Get layer order based on the tool_num array
    for j in tool_num[ind0:ind1+1]:
        lo = lo + j[1]
    
    # Rearramge based on the order and append to gcode array   
    if ((lo == "0") or (lo == "01") or (lo == "02") or (lo == "12") or (lo == "012")):
        gcode.extend(lines[layer_change[i]:layer_change[i+1]])
    elif ((lo == "10") or (lo == "20") or (lo == "21") or (lo == "120")): 
        gcode.append(lines[layer_change[i]]) # Don't forget the Layer number!
        gcode.extend(lines[tool[ind1]:layer_change[i+1]-1])
        gcode.extend(lines[tool[ind0]:tool[ind1]])
        gcode.append(lines[layer_change[i+1]-1])    #add the G0 Z-up line
        #print("Change 10 on " + str(lines[layer_change[i]]))
    elif (lo == "201"):
        gcode.append(lines[layer_change[i]])
        gcode.extend(lines[tool[ind0+1]:layer_change[i+1]-1])
        gcode.extend(lines[tool[ind0]:tool[ind0+1]])
        gcode.append(lines[layer_change[i+1]-1])    #add the G0 Z-up line
        #print("Change 201 on " + str(lines[layer_change[i]]))
    elif (lo == "210"): 
        gcode.append(lines[layer_change[i]])
        gcode.extend(lines[tool[ind1]:layer_change[i+1]-1])
        gcode.extend(lines[tool[ind0+1]:tool[ind1]])
        gcode.extend(lines[tool[ind0]:tool[ind0+1]])
        gcode.append(lines[layer_change[i+1]-1])    #add the G0 Z-up line
        #print("Change 210 on " + str(lines[layer_change[i]]))
    elif (lo == "102"): 
        gcode.append(lines[layer_change[i]])
        gcode.extend(lines[tool[ind0+1]:tool[ind1]])
        gcode.extend(lines[tool[ind0]:tool[ind0+1]])
        gcode.extend(lines[tool[ind1]:layer_change[i+1]])
        #print("Change 102 on " + str(lines[layer_change[i]]))
    elif (lo == "021"): 
        gcode.append(lines[layer_change[i]])
        gcode.extend(lines[tool[ind0]:tool[ind0+1]])
        gcode.extend(lines[tool[ind1]:layer_change[i+1]-1])
        gcode.extend(lines[tool[ind0+1]:tool[ind1]])
        gcode.append(lines[layer_change[i+1]-1])    #add the G0 Z-up line
        #print("Change 021 on " + str(lines[layer_change[i]]))
    else: 
        print("Unhandled Layer at " + str(lines[layer_change[i]]))
   
#add on all the last lines of gcode
gcode.extend(lines[layer_change[-1]:]) 

#print out the number of lines in the edited code    
print(str(len(gcode)) + " lines in gcode")
#==============================================================================
#removes all lies that contain only "T0", etc
if remove_tool_change:
    gcode = [line for line in gcode if (line[0:2] != "T0") and (line[0:2] != "T1") and (line[0:2] != "T2")]
    print(str(len(gcode)) + " lines in gcode after removing tool callouts")
#Check for retraction problems
prev = 0
curr = 0
retracted = False
errors = False
 
#run this loop twice. First time - add priming
#second time - check whole code again
for j in [0,1]:
    for i in range(len(gcode)):
        curr_line = i
        if "M104 S0" in gcode[i]:
            print("End of print")
            break
        elif "E" in gcode[i]:
            split_line = gcode[i].split('\n') #in case multiple commands on single line, split line
            for line in split_line:
                if ("E" in line) and ("Extruder" not in line): #check for any commands that involve extrusion
                    tmp = line + " "
                    ind0 = tmp.find("E")
                    ind1 = tmp[ind0:].find(" ")
                    no_move = ((line.find("X") == -1) and (line.find("Y") == -1))
                    #print(tmp[ind0+1:ind0+ind1])
                    try:
                        curr = float(tmp[ind0+1:ind0+ind1])
                    except ValueError:
                        print("ValueError at line" + str(i) + ": " + line)
                        errors = True
                    if line[0:3] == "G92":
                        retracted = retracted #no change
                    elif curr < prev:
                        retracted = True
                        #print("Retraction line " + str(curr_line))
                    elif (prev == 0) and no_move and (curr >= 0): #if last line had E0 and curr line has no move, it's priming
                        retracted = False #primed
                        #print("Primed line " + str(curr_line))
                    elif retracted and (curr - prev > 0):
                        retracted = False #reset to false for following tests
                        if j == 0:
                            gcode[i] = " G92 E0\nG0 E" + str(priming) + "\nG92 E0\n " + gcode[i]
                        if j == 1:   
                            print("Nozzle not primed at line " + str(curr_line))
                            errors = True
                    prev = curr #set previous to current before next iteration
                    
#==============================================================================
   
f_out = open(filename[:-6] + '_reordered.gcode', 'w')

#for line in gcode:
for line in gcode:
    f_out.write(line)

f_out.close()

end = time.time()
print(end-start)
print(str(additional_lines) + " lines added")
if errors:
    print("Errors were encountered. Please revise")
