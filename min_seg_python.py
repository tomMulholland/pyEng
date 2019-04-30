# -*- coding: utf-8 -*-
"""
Find movements less than l_min and interpolates the movements to avoid certain errors and slowdowns in prints.

@author: Tom
"""

# -*- coding: utf-8 -*-

#import os
import time
import tkinter as tk
from tkinter import filedialog
from tkinter.simpledialog import askfloat


"""MAIN"""
# Adjust these values

l_min = 0.01 #[mm] minimum segment length

#*************************************************
#os.chdir('C:/Users/Tom/Documents/Python Scripts')

#Prompt for a .gcode file with a Open File window
root = tk.Tk()
root.withdraw()
filename = filedialog.askopenfilename(title="Please select a gcode file")

l_min = askfloat("Input", "Minimum segment length (0.01 suggested):",
                                  parent=root, minvalue=0, maxvalue=1)

start = time.time()

f_out = open(filename[:-6] + '_shortened.gcode', 'w')

#print(str(len(lines)) + " lines at start")
prevline = ';';
strset0 = ';';
plB = 0; #previous line boolean
nlB = 0; #new line boolean, True when new line is an X or Y movement
x0 = 0;
x1 = 0;
y0 = 0;
y1 = 0;
lines_skipped=0;

#cycle through all lines
for line in open(filename, "r"):
  newline = line
    #ignore lines that are don't start with G1, or that are G1 E... or G1 Z...
  if (("G1" != newline[0:2]) or (newline[3] == "E") or (newline[3] == "Z")):
    f_out.write(prevline); 
    prevline = newline;
    plB = 0;
  else:
    #calculate distances
    nlB = 1;
    strset1 = newline.split();
    x1 = float(strset1[1][1:]);
    y1 = float(strset1[2][1:]);
    if plB == 1:
      distance = ((x1-x0)**2 + (y1-y0)**2)**(1/2);
      if distance > l_min:
        #if that distance was okay, write prevline to new file
        #prep for next cycle
        f_out.write(prevline);  
        prevline = newline;
        x0 = x1;
        y0 = y1;
        strset0 = strset1;
      else:
        lines_skipped += 1
    else:
      f_out.write(prevline);
      prevline = newline;
      plB = 1;

f_out.close()

end = time.time()
print(str(end-start) + " seconds to run")
print(str(lines_skipped) + " lines skipped / interpolated")

