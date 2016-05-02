# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 12:24:08 2014

@author: IPC
"""

typeEOS = 'junk'
typeMolecule = 'junk'

R = 8314.0  #J/kmol/K

def getaandb():
    Pc = typeMolecule.Pc
    Tc = typeMolecule.Tc
    OmegaA = typeEOS.OmegaA
    OmegaB = typeEOS.OmegaB
    a = OmegaA*(R*Tc)**2/Pc
    b = OmegaB*(R*Tc)/Pc   
    return a, b
    
def alpha(T):
    Tc = typeMolecule.Tc
    acc = typeMolecule.acc
    return typeEOS.alpha(T/Tc, acc)    
    
def P(T, v):
    a, b = getaandb()
    pp = R*T/(v-b) - a*alpha(T)/(v+typeEOS.epsilon*b)/(v+typeEOS.sigma*b)
    return pp