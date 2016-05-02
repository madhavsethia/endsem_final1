# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 12:24:08 2014

@author: IPC
"""
import scipy
import 


class EOS:
    def __init__(self, eos, molecule):
        self.typeEOS = eos
        self.typeMolecule = molecule
        self.R = 8314.0  #J/kmol/K
        self.getaandb()
    def getaandb(self):
        R = self.R
        typeEOS = self.typeEOS
        typeMolecule = self.typeMolecule
        Pc = typeMolecule.Pc
        Tc = typeMolecule.Tc
        OmegaA = typeEOS.OmegaA
        OmegaB = typeEOS.OmegaB
        self.a = OmegaA*(R*Tc)**2/Pc
        self.b = OmegaB*(R*Tc)/Pc   
    def alpha(self,T):
        Tc = self.typeMolecule.Tc
        acc = self.typeMolecule.acc
        return self.typeEOS.alpha(T/Tc, acc)        
    def P(self,T, v): 
        typeEOS = self.typeEOS; R = self.R
        a, b = self.a, self.b
        pp = R*T/(v-b) - a*self.alpha(T)/(v+typeEOS.epsilon*b)/(v+typeEOS.sigma*b)
        return pp
    def Z(self, T, P):
        R = self.R; a = self.a; b = self.b
        sigma = self.typeEOS.sigma; epsilon = self.typeEOS.epsilon
        alpha = self.alpha(T)
        p_p = P*b/R/T; a_p = P*a*alpha/R**2/T**2
        
        a3 = 1.0
        a2 = epsilon*p_p + p_p*sigma - p_p - 1.0
        a1 = a_p + epsilon*p_p**2*sigma - epsilon*p_p**2 - epsilon*p_p - p_p**2*sigma - p_p*sigma
        a0 = -a_p*p_p - epsilon*p_p**3*sigma - epsilon*p_p**2*sigma
        
        roots = scipy.roots([a3, a2, a1, a0])
        roots = [rt.real for rt in roots if abs(rt.imag) < 1e-16]
        if len(roots) == 3:
            return scipy.array([min(roots), max(roots)])
        elif len(roots) == 1:
            return scipy.array(roots)
        else:
            return []   
        
    def getPborder(self, T):
        a = self.a; b = self.b
        alpha = self.alpha(T)
        R = self.R; s = self.typeEOS.sigma; e = self.typeEOS.epsilon
        A = a*alpha/(s-e)/b/R/T
        
        a4 = 1.0
        a3 = 2*A*b*e - 2*A*b*s + 2*b*e + 2*b*s       
        a2 = A*b**2*e**2 - 4*A*b**2*e - A*b**2*s**2 + 4*A*b**2*s + b**2*e**2 + 4*b**2*e*s + b**2*s**2
        a1 = -2*A*b**3*e**2 + 2*A*b**3*e + 2*A*b**3*s**2 - 2*A*b**3*s + 2*b**3*e**2*s + 2*b**3*e*s**2
        a0 = A*b**4*e**2 - A*b**4*s**2 + b**4*e**2*s**2
        
        roots = scipy.roots([a4, a3, a2, a1, a0])
        roots = [x.real for x in roots if abs(x.imag) < 1e-16 and x.real > b]
        if len(roots) == 2:
            PP = [self.P(T, roots[0]), self.P(T, roots[1])]
            return True, min(PP), max(PP)
        else:
            return False, None, None


    
