# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 11:16:00 2014

@author: IPC
"""

OmegaA = 0.42748
OmegaB = 0.08644
sigma = 1.0
epsilon = 0.0
def k(acc):
    kappa =  0.48 + 1.574*acc - 0.176*acc**2
    return kappa

def alpha(Tr, acc):
    alf = (1 + k(acc)*(1-Tr**0.5))**2
    return alf
