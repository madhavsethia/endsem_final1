# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 09:24:42 2014

@author: prasad
"""

import vis

planet=vis.sphere(pos=(0,0,0),radius=5,color=vis.color.red)
ball=vis.sphere(pos=(30,0,0),radius=0.5,color=vis.color.green)

from scipy.integrate import odeint 
import numpy as a 

def diff(r,t):
    R=r[0]
    y=r[1]
    dRdt=y
    dydt=-10/R
    
    return dRdt,dydt
    
X0=[0.01,10]
t=a.linspace(0,100,10000)
sol=odeint(diff,X0,t)
pos0=30
i=0
vel0=0
for i in range(10000):
    F=sol[i+2,1]
    dt=1
    vel=vel0+F*(dt)
    posch=pos0+(0.5*F*dt*dt)+vel*dt
    
    ball.pos=(posch,0,0)
    vel=vel0
    i=i+1
    
    vis.rate(100)
    
    
    
    
    

#import matplotlib.pyplot as plt 
#x = sol[:, 0]
#z = sol[:, 1]
#plt.plot(t,x,t,z)
