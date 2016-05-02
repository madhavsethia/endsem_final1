# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 11:16:15 2014

@author: vhd
"""


R=8314.0
typeEOS='junk'
typeMolecule='junk'
class EOS:
   def  __init__(self.eos,Molecule):
        self.typeEOS=eos
        self.typeMolecule=Molecule
        self.R=8314
        self.getaandb()
   def  getaandb():
        R=self.R
        typeEOS=self.typeEOS
        typemolecule=self.typeMolecule
        Pc=typeMolecule.Pc
        Tc=typeMolecule.Tc
        OmegaA=typeEOS.OmegaA
        OmegaB=typeEOS.OmegaB
        self.a=OmegaA*(R*Tc)**2/(Pc)
        self.b=OmegaB*(R*Tc/Pc)
        return a,b
   def  alpha(self,T):
        R=self.R
        Tc=self.typemolecule.Tc
        acc=self.typemolecule.acc
        return self.typeEOS.alpha(T/Tc,acc)
   def P(self,T,v):
        typeEOS=self.typeEOS;R=self.R
        a,b=self.a,self.b
        pp=R*T/(v-b)-a*self.alpha(T)/(v+typeEOS.epsilon*b)/(v+typeEOS.sigma*b)
        return pp

    