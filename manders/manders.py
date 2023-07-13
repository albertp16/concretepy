# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 08:41:08 2023

@author: albert pamonag
"""

import matplotlib.pyplot as plt
import numpy as np
import math

def compStrConfCon(fpco,fpl):
    # fpco = unconfined concrete strength
    A = 2.254*math.sqrt(1+((7.92*fpl)/fpco)) 
    B = 2*(fpl/fpco)
    fpcc = fpco*(-1.254+A-B)
    return fpcc 

def effeLateralConfStress(ke,px,fyh):
    fpl = ke*px*fyh
    return fpl

ratio_arr = []
value_arr = []
value2_arr = []
i = 0 
## when f1x == f1y are equal 
# i = 0 
# while i < 0.3:
#     ratio = i
#     A = 2.254*math.sqrt(1+(7.92*ratio)) 
#     B = 2*ratio
#     fpcc = (-1.254+A-B)
#     ratio_arr.append(i*-1)
#     value_arr.append(fpcc)
#     i+= 0.01

#     i = 0 




while i <= 0.3:
    ratio = i
    A = 2.254*math.sqrt(1+(7.92*ratio)) 
    B = 2*ratio
    fpcc = (-1.254+A-B)
    ratio_arr.append(i*-1)
    value_arr.append(fpcc)

#     if(ratio > 0.2):
#         init = i
# #         print(init)
#         Ap = 2.254*math.sqrt(1+(7.92*init)) 
#         Bp = 2*init
#         fpccp = (-1.254+Ap-Bp)
#         value2_arr.append(fpcc - (fpccp*0.2))
#     else:
#         value2_arr.append(fpcc)
    i+= 0.01

x = value_arr
y = ratio_arr

# plot
fig, ax = plt.subplots()

# ax.plot(value2_arr, y, linewidth=2.0)
ax.plot(x, y, linewidth=2.0)
plt.title('Confined Strength Determination from Lateral \n Confining Stresses for Rectangular Section')
plt.xlabel("Confined Strength Ratio, $f^{'}_{cc}/f^{'}_{co}$")
plt.ylabel("Largest Confining Stress Ratio,$f^{'}_{l2}/f^{'}_{co}$ ")
plt.grid()
plt.show()

# print(ratio_arr)
# print(value_arr)