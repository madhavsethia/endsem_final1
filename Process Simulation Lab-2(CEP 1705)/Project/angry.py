# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 19:26:53 2014

@author: Administrator
"""

import visual
import math

scene=display(title='Space basket ball', x=0, y=0, width=1280, height=786)
scene.select()
scene.range=15000
launcher_pos=vector(-10000,0,0)
g=6.67e-11

def make_label(x=0, y=0, text= '', centered=False):
    l=None
    if centered:
        l= label(pos=(x,y), opacity=0, box=0, line=0)
    else:
        l= label(pos=(x,y), xoffset=1, opacity=0, box=0, line=0)
    l.text= text
    return l

class Earth:
    radius=1000
    density=4e11
    rotation=2*pi/10
    def __init__(self):
        self.planet=sphere(pos=(0,0,0),radius=self.radius, material=materials.earth)
        self.atm=sphere(pos=(0,0,0),radius=5*self.radius, color=color.blue, opacity=0.1)
        self.m=4.0/3.0*pi*math.pow(self.radius*1000, 3) * self.density
    def hit(self,o):
        if mag(self.planet.pos - o.pos) <= self.planet.radius:
            return True
    def is_in_range(self, o):
        if mag(self.atm.pos - o.pos) <= self.atm.radius:
            return True
    def gravity(self, o, dt):
        if self.is_in_range(o):
            a=g*1e-9*self.m / math.pow( mag (o.pos-self.planet.pos),2) * norm(self.planet.pos -o.pos)
            o.v+=a*dt     
    def rotate(self, dt):
        self.planet.rotate(angle=self.rotation*dt, axis=(0,1,0))
    

class Launcher:
    lp_size=500.0
    speed_scale=1.0
    def __init__(self, start_pos, on_launch):
       
        self.box=box(pos=start_pos, length=self.lp_size,
                     height=self.lp_size, width=self.lp_size,
               color=color.red)
        self.launch_point=start_pos - vector(self.lp_size/2, 0, 0)
        self.arrow=arrow(pos=start_pos, axis=(0,0,0), visible=False)
        self.pick=False
        self.drag_pos=None
        self.on_launch=on_launch

    def run(self,dt, m1):
        
        if m1 and m1.drag and m1.pick == self.box: 
            self.drag_pos = m1.pickpos # where on the ball
            self.pick = True # pick now true (not None)
            self.arrow.visible=True
        elif m1 and m1.drop: # released at end of drag
            self.pick = None # end dragging (None is false)
            self.arrow.visible=False
            self.launch(self.launch_point, self.arrow.axis/self.speed_scale)
        if self.pick:
            # project onto xy plane, even if scene rotated:
            new_pos = scene.mouse.project(normal=(0,0,1))
            if new_pos != self.drag_pos: # if mouse has moved
            
                self.arrow.pos = new_pos 
                self.arrow.axis=self.launch_point-self.arrow.pos  
                self.drag_pos = new_pos

    def launch(self, start, vect):
        print "Launching Space ball from %s with speed %s" % (str(start),
                                                              str(vect))
        self.on_launch(start, vect)
class Balls:
    size=100.0
    mass=1
    def __init__(self, planet):
        self.balls=[]
        self.planet=planet

    def add_ball(self,at_pos, with_speed):
        b=sphere(pos=at_pos, radius=self.size, color=color.orange,
                 make_trail=True, trail_type="points",
                 retain=40, interval=10)
        b.trail_object.size=1
        b.v=with_speed
        b.age=0
        self.balls.append(b)

    def move(self,dt):
        tbd=[]
        for b in self.balls:
            tbd=[]
            self.planet.gravity(b,dt)
            b.pos=b.pos+b.v*dt
            b.age+=dt
            if self.planet.hit(b):
                b.visible=False
                b.trail_object.visible=False
                tbd.append(b)
        for b in tbd:
            self.balls.remove(b)

def main_loop():
    while True:
        m1=None
        if scene.mouse.events:
            m1 = scene.mouse.getevent() # get event
        launcher.run(deltat, m1)
        balls.move(deltat)
        earth.rotate(deltat)
        rate(100)
        


earth=Earth()
balls=Balls(earth)
launcher=Launcher(launcher_pos, balls.add_ball)
deltat=1.0/100
make_label(-14000,8000,
"""Click on red box and drag left, then release to launch.
Click right mouse button and drag to rotate.
Click both mouse buttons and drag to zoom.""")
main_loop()