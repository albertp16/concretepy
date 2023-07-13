# -*- coding: utf-8 -*-
"""
Created on Mon May 22 16:55:53 2023

@author: albert pamonag
"""
import math 
import numpy as np

def eRF(exposure,type):
    data = {
        "interior" : {
            "carbon" : 0.95,
            "glass" : 0.75,
            "aramid" : 0.85
        },
        "exterior" : {
            "carbon" : 0.85,
            "glass" : 0.65,
            "aramid" : 0.75
        },
        "aggressive" : {
            "carbon" : 0.85,
            "glass" : 0.50,
            "aramid" : 0.70
            },
    }
    results = data[exposure][type]
    return results

# def beta_1(fc): 
#     ##NSCP 2015 422.2.2.4.3
#     value = 1.05 - 0.05*(fc/1000)
#     if(17 <= fc and fc <= 28):
#         value = 0.85
#     elif (28 <= fc and fc < 55):
#         value = 0.85 - ((0.05*(fc-28))/7)
#     else:
#         value = 0.65

#     return value

def strengthFactor(es,ey):
    '''
    
    '''
    phi_factor = 0.64 + 0.25*(es - ey) / (0.005 - ey)
    if phi_factor >= 0.90:
        phi, classify = 0.90, 'Tension-controlled'
    elif phi_factor <= 0.65:
        phi, classify = 0.90, 'Compression-controlled'
    else:
        phi, classify = phi_factor, 'Transition' 
    return phi, classify

    
def areaCircle(db):
    pi = math.pi
    value = (pi/4)*(math.pow(db,2))
    return value

# def strain():
#     # ebi = ( MDL * (df - (k*d)) )  /( Icr * ec_convert ) 
#     return "Hello"

# def modulus


params = {
    "b" : 305, #mm
    "h" : 609.6, #mm
    "db" : {
        "main" : 28.6, #MPa
        "secondary" : 10 #MPa
    },
    "n" : 3,
    "fc" : 34.5, #MPA
    "fy" : 414, #MPa
    "Es" : 200000 #MPa
    }

class beamFlexure():
    def __init__(self,params):
        self.params = params
    def effectiveDepth(self):
        
        depth = self.params['h'] - self.params['cc'] - self.params['dbs'] - self.param['db']
        return depth
    def steelRatio(self):
        #work on the top parameters
        ratio = self.params['area_steel']/(self.params['b']*self.params['h'])
        return ratio
    def modulusElasticityConcrete(self): ## Modulus Elascity of Concrete ##TODO review the ACI
        '''
        Modulus of elasticity of concrete 
        reference: ACI 19.2.2.1
        '''
        if np.isnan(self.params['fc']) == True:
            return "variable fc in not a number, check your input"
        EC_CONST = 4700
        output = EC_CONST*math.sqrt(self.params['fc'])
        return output
    def betaOne(self):
        '''
        NSCP 2015 422.2.2.4.3
        '''
        if np.isnan(self.params['fc']) == True:
            return "variable fc in not a number, check your input"
        
        if self.params['fc'] > 55: 
            return 0.65
        if 17 <= self.params['fc'] and self.params['fc'] <= 28:
            return  0.85
        elif  28 <= self.params['fc'] and self.params['fc'] < 55 :
            return 0.85 - ((0.05*(self.params['fc']-28))/7)
    def nominalMomentwithFRD():
        return "checking"

test = beamFlexure(params)
beta_one = test.betaOne()
ec = test.modulusElasticityConcrete()

