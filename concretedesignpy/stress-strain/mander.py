import matplotlib.pyplot as plt
import numpy as np
import math

# http://www.jdcui.com/?p=11858
# http://www.jdcui.com/?p=952
def compStrConfCon(fpco,fpl):
    # fpco = unconfined concrete strength
    A = 2.254*math.sqrt(1+((7.92*fpl)/fpco)) 
    B = 2*(fpl/fpco)
    fpcc = fpco*(-1.254+A-B)
    return fpcc 

def rSolver(fl1,fl2):
    r = fl1/fl2
    return r 

def barX(fl1,fl2,fc):
    bar_x = (fl1 + fl2)/(2*fc)
    return bar_x

def equationA(r):
    A = 6.8886-(0.6069+(17.275*r))*math.exp(-4.989*r)
    return A

def equationB(A,r):
    B2 = ((5/A)*(0.9849-0.6306*math.exp(-3.8939*r)))-0.1
    B = (4.5/B2)-5
    return B

def confinedStrength(A,B,bar_x):
    K = 1 + A*bar_x*(0.1 + (0.9/(1+B*bar_x)))
    return K

def compStrConfConRatio(ratio):
    A = 2.254*math.sqrt(1+(7.92*ratio)) 
    B = 2*ratio
    fpcc = (-1.254+A-B)
    return fpcc 

def effeLateralConfStress(ke,px,fyh):
    fpl = ke*px*fyh
    return fpl

ratio_arr = []
value_arr = []
value0_arr = []
value02_arr = []
value04_arr = []
value06_arr = []
value08_arr = []
value1_arr = []
value12_arr = []
value14_arr = []
value16_arr = []
value18_arr = []
value2_arr = []
value22_arr = []
value24_arr = []
value26_arr = []
value28_arr = []

i = 0 

def group(r):
    Aindex = equationA(r)
    Bindex = equationB(Aindex,r)
    fpccfc = confinedStrength(Aindex,Bindex,ratio)
    return fpccfc

def solver(r,xi):
    Aindex = equationA(r)
    Bindex = equationB(Aindex,r)
    k1 = Aindex*(0.1 + 0.9/(1 + (Bindex*xi)))
    K = 1 + (k1*xi)
    return K

while i <= 0.3:
    small_r2 = 0.2 
    small_r1 = 0.1 
    small_r0 = 0 
    ratio = i

    value0_arr.append(solver(0,ratio))
#     value02_arr.append(group(0.02))
#     value04_arr.append(group(0.04))
#     value06_arr.append(group(0.06))
#     value08_arr.append(group(0.08))
    value1_arr.append(group(.1))
#     value12_arr.append(group(0.12))
#     value14_arr.append(group(0.14))
#     value16_arr.append(group(0.16))
#     value18_arr.append(group(0.18))    
    value2_arr.append(group(.2))
#     value22_arr.append(group(0.22))
#     value24_arr.append(group(0.24))
#     value26_arr.append(group(0.26))
#     value28_arr.append(group(0.28))  
    
    #when fl1 = fl2
    fpcc = compStrConfConRatio(ratio) 
    ratio_arr.append(i*-1)
    value_arr.append(fpcc)

    i += 0.01
    
# print(ratio_arr)
print(value0_arr)