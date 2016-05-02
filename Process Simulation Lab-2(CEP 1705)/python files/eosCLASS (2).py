# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 13:01:24 2014

@author: vhd
"""
import scipy #for finding roots
class EOS:
    def __init__(self, eos, molecule): #constructor
        self.typeeos = eos
        self.typemolecule = molecule
        self.r = 8.314426 
        self.getaandb() #allows easy calculation of a and b on the fly
    def getaandb(self):
        r = self.r
        typeeos = self.typeeos
        typemolecule = self.typemolecule
        pc= typemolecule.pc
        tc= typemolecule.tc
        omegaA = typeeos.omegaA
        omegaB = typeeos.omegaB
        #acc=typemolecule.acc
        self.a=omegaA*(r*tc)**2/pc
        self.b = omegaB*(r*tc)/pc
        return self.a, self.b
    def alpha(self, t):
        typemolecule = self.typemolecule
        acc= typemolecule.acc
        tc= typemolecule.tc
        return self.typeeos.alpha(t/tc,acc)
    def p(self, t, v):
        typeeos = self.typeeos; #typemolecule = self.typemolecule
        a,b = self.getaandb()
        pp = self.r*t/(v-b)-a*self.alpha(t)/((v+typeeos.epsilon*b)*(v+typeeos.sigma*b))
        return pp
    def Z(self,t,p): # we pass p because in this case the pressure is the independent variable hence we don't use self.p
        #Z3+AZ2+BZ+C=0
        eps = self.typeeos.epsilon
        sig = self.typeeos.sigma
        pb = (p*self.b)/(self.r*t)
        ap = (p*self.a*self.alpha(t))/((self.r*t)**2)
        A = (eps+sig-1)*pb -1
        B= sig*eps*(pb**2)-(sig+eps)*(pb**2)-(sig+eps)*pb+ap
        C= -sig*eps*pb**3-sig*eps*pb**2-ap*pb
        roots = scipy.roots([1.0,A,B,C]) # gives all roots, even complex ones
        roots = [x.real for x in roots if abs(x.imag) < 1e-16] #.real and .imag are keywords coded in python
        return roots
    def getPborder(self,t): # this is used to get V where the dP/dv = 0. the input equation is the differentiated equation
        e = self.typeeos.epsilon
        s= self.typeeos.sigma
        A= -self.r*t*(self.b*self.typeeos.epsilon-self.typeeos.sigma)
        B = self.a*self.alpha(t)
        b = self.b
        C = -1
        a5 =A*b**4*e**2*s**2 + B*b**4*e**2 + C*b**4*s**2 
        a1 = (A + B + C)
        a2 = 2*A*b*e + 2*A*b*s + 2*B*b*e - 2*B*b + 2*C*b*s - 2*C*b
        a3 = A*b**2*e**2 + 4*A*b**2*e*s + A*b**2*s**2 + B*b**2*e**2 - 4*B*b**2*e + B*b**2 + C*b**2*s**2 - 4*C*b**2*s + C*b**2
        a4 = (2*A*b**3*e**2*s + 2*A*b**3*e*s**2 - 2*B*b**3*e**2 + 2*B*b**3*e - 2*C*b**3*s**2 + 2*C*b**3*s)
        vsol = scipy.roots([a1,a2,a3,a4,a5])
        return vsol
        #pp = self.p(t,vsol)
        #pp = [x.real for x in pp if abs(x.imag)<1e-19]
        #return pp
        
        #Making the program cool that's all :P
        #roots = scipy.roots([a1,a2,a3,a4,a5])
        #roots = [x.real for x in roots if abs(x.imag)<1e-19 and x>b ]
        #if len(roots) == 3:
        #    return [min(roots),max(roots)]
        #elif len(roots)==1:
        #    return [roots[0]]
        #else
        #   return []
            
    