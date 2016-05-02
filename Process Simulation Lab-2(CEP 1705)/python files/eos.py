# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 11:16:15 2014

@author: vhd
"""

R=8314.0
def getaandb(T,typeEOS,typemolecule):
    Pc=typemolecule.Pc
    Tc=typemolecule.Tc
    OmegaA=typesrk.OmegaA
    OmegaB=typesrk.OmegaB
    acc=typemolecule.acc
    alpha=typeEOS.alpha(T/Tc,acc)
    a=OmegaA*(R*Tc)**2/(Pc)
    b=OmegaB*(R*Tc/Pc)
    return a,b,alpha
    
def P(T,v,typeEOS,typrmolecule):
    a,b,alpha=getaandb(T,typeEOS,typemolecule)
    pp=R*T/(v-b)-a*alpha/(v+typeEOS.epsilon*b)/(v+typeEOS.sigma*b)
    return pp

    