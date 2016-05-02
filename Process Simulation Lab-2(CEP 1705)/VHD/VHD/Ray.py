# -*- coding: utf-8 -*-
"""
Created on Wed Feb 05 10:40:50 2014

@author: IPC
"""
import scipy, scipy.linalg
import pylab
class Line:
    def __init__(self, p1, p2):
        p1 = scipy.array(p1)
        p2 = scipy.array(p2)
        dp = p2 - p1
        self.length = scipy.linalg.norm(dp)
        self.p0 = p1
        self.d = dp/self.length
        self.color = 'black'
    def draw(self):
        p1 = self.p0
        p2 = self.p0 + self.d*self.length
        xx = [p1[0], p2[0]]
        yy = [p1[1], p2[1]]
        pylab.plot(xx, yy, color=self.color)
        pylab.scatter(xx, yy, color=self.color,s=5)

class Ray(Line):
    def __init__(self, p0, d):
        p0 = scipy.array(p0)
        d = scipy.array(d)
        Line.__init__(self, p0, p0+d)
        self.color = 'red'


        
p1 = [-1, 0]; p2 = [1, 0]
line = Line(p1, p2)
ray1 = Ray([0,1], [0.0, -1])
line.draw()
ray1.draw()
pylab.show()