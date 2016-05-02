# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 11:22:45 2014

@author: IPC
"""
R = 8314.0  #J/kmol/K
T=350 #K

def getaandb(T,pr,benzene):
    Pc = benzene.Pc
    Tc = benzene.Tc
    OmegaA = pr.OmegaA
    OmegaB = pr.OmegaB
    acc = benzene.acc
    alpha = pr.alpha(T/Tc, acc)
    a = OmegaA*(R*Tc)**2/Pc
    b = OmegaB*(R*Tc)/Pc   
    return a, b, alpha

def P(T, v, pr,benzene):
    a, b, alpha = getaandb(T, pr, benzene)
    pp = R*T/(v-b) - a*alpha/(v+pr.epsilon*b)/(v+pr.sigma*b)
    return pp
    
    
    
    
    