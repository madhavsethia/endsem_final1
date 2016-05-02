# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 11:11:06 2014

@author: vhd
"""

acc=0.212
OmegaA=0.42748
OmegaB=0.08644
sigma=1
epsilon=0
Tr=0.85
R=8314.0
def k(acc):
    kappa=0.48+1.574*acc-0.176*acc**2
    return kappa
def alpha(Tr,acc):
    alpha=(1+k(acc))*(1-Tr**0.5)**2
    return alpha
    