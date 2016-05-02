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
        
        #Making the program cool, that's all :P
        #roots = scipy.roots([a1,a2,a3,a4,a5])
        #roots = [x.real for x in roots if abs(x.imag)<1e-19 and x>b ]
        #if len(roots) == 3:
        #    return [min(roots),max(roots)]
        #elif len(roots)==1:
        #    return [roots[0]]
        #else
        #   return []
    def gibbs(self,P,T,v):
        from scipy import log
        eps = self.typeEOS.epsilon
        sig = self.typeEOS.sigma
        gib1 = self.R*T*log((v-self.b/v))
        gib2 = self.alpha(T)*self.a*log((v+eps*self.b)/(v+sig*self.b))/((sig-eps)*self.b)
        return gib1-gib2
    def solution(self,t,p):
         from pylab import sqrt        
         while 1>0:        
             v= self.b*1.1
             typeeos = self.typeeos; #typemolecule = self.typemolecule
             e= typeeos.epsilon
             s = typeeos.sigma
             r= self.r
             alpha = self.alpha(t)
             a,b = self.getaandb()
             pb = (p*self.b)/(self.r*t)
             ap = (p*self.a*self.alpha(t))/((self.r*t)**2)
             A = 1        
             B = (e+s-1)*pb -1
             C= s*e*(pb**2)-(s+e)*(pb**2)-(s+e)*pb+ap
             D = -s*e*pb**3-s*e*pb**2-ap*pb
             for i in range(0,1000):
                 v = v - ((self.r*t/(v-b)-a*self.alpha(t)/((v+typeeos.epsilon*b)*(v+typeeos.sigma*b)))-p)/(a*alpha/((b*e + v)*(b*s + v)**2) + a*alpha/((b*e + v)**2*(b*s + v)) - r*t/(-b + v)**2)
             Z = (p*v)/(r*t)
             b1 = (A/B)+Z
             a1= 1
             c1 = (A/D)/Z
             v1 = (-b1 + pylab.sqrt(-b1*b1-4*a1*c1))/(2*a1)
             v2 = (-b1 - pylab.sqrt(-b1*b1-4*a1*c1))/(2*a1)
             varray = (v,v1,v2)
             for i in range(0,2):
                 for j in range(i+1,2):
                     if(varray(i)>varray(j)):
                             temp = varray(i)
                             varray(i) = varray(j)
                             varray(j) = temp
             error = ((p*(varray(1)-varray(0)))-(self.gibbs(p,t,varray(1))-self.gibbs(p,t,varray(0))))-(((self.gibbs(p,t,varray(2)))-self.gibbs(p,t,varray(1)))-(p*(varray(2)-varray(1))))
             if(abs(error)>1e-2):
                 if(error>0):
                     p = p/pylab.sqrt(error)
                 else:
                     p = p*pylab.sqrt(error)
             else:
                 break
         return p
         #bends method   