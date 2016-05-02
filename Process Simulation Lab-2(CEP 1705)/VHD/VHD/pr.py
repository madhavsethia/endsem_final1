# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 12:45:34 2014

@author: IPC
"""

OmegaA = 0.457
OmegaB = 0.0777
sigma = 1.0 + 2.0**0.5
epsilon = 1.0 - 2.0**0.5

def k(acc):
    kappa = 0.37464 + 1.5422*acc - 0.2699*acc**2
    return kappa

def alpha(Tr, acc):
    alf = (1 + k(acc)*(1-Tr**0.5))**2
    return alf