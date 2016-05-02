# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 19:26:53 2014

@author: Administrator
"""
play=0

if play==0:
    

     from visual import *
import math
import time

scene=display(title='Space hoops', x=0, y=0,z=0, width=1380, height=786) #scene
scene.select()
scene.range=30000
launcher_pos=vector(-17000,0,0)
g=6.67e-11 #constant



rules= label(pos=(0,0,0),text="""THIS IS SPACE HOOPS !
YOU HAVE 5 BALLS TO FIRE
TO FIRE- CLICK ON THE BLUE BOX AND DRAG IT LIKE A SLING SHOT
YOUR AIM- TO SCORE BY SHOOTING THE BALL THROUGH THE HOOP""" )

time.sleep(6)
rules.visible=False

ball_c=label(pos=(-10000,10000,0),text='')

win = label (pos = (0,10000,0), text = '',opacity=0, box=0, line=0)


class Earth:
    radius1=200
    density1=30e11
    rotation1=2*pi/10
    radius2=1000
    density2=4e11
    rotation2=2*pi/10
    l=6
    def __init__(self):
        self.planet1=sphere(pos=(-14000,0,0),radius=self.radius1, material=materials.marble, color=color.red)
        self.atm1=sphere(pos=(-14000,0,0),radius=self.l*self.radius1, color=color.blue, opacity=0.1)
        self.m1=4.0/3.0*pi*math.pow(self.radius1*1000, 3) * self.density1
        self.planet2=sphere(pos=(1000,0,0),radius=self.radius2, material=materials.earth)
        self.atm2=sphere(pos=(1000,0,0),radius=10*self.radius2, color=color.blue, opacity=0.1)
        self.m2=4.0/3.0*pi*math.pow(self.radius2*1000, 3) * self.density2
        self.t=self.planet1.pos[0]+(self.l*self.radius1)
    def hit(self,o):
        if o.pos[0]<self.t:
            if mag(self.planet1.pos - o.pos) <= self.planet1.radius: #for the ball to stop moving when it hits the earth
                return True
        else:
            if mag(self.planet2.pos - o.pos) <= self.planet2.radius: #for the ball to stop moving when it hits the earth
                return True
            
    def is_in_range(self, o): # defining the field where gravitation is there
        if o.pos[0]<self.t:        
            if mag(self.atm1.pos - o.pos) <= self.atm1.radius:
                return True
        else:
            if mag(self.atm2.pos - o.pos) <= self.atm2.radius:
                return True
    def gravity(self, o, dt):
        if self.is_in_range(o):
            if o.pos[0]<self.t:   
                a=g*1e-9*self.m1 / math.pow( mag (o.pos-self.planet1.pos),2) * norm(self.planet1.pos -o.pos)
                o.v+=a*dt
            else:
                a=g*1e-9*self.m2 / math.pow( mag (o.pos-self.planet2.pos),2) * norm(self.planet2.pos -o.pos)
                o.v+=a*dt
    def rotate(self, dt):
        self.planet2.rotate(angle=self.rotation1*dt, axis=(0,1,0)) #rotation for asthetics
        
    
    

class Launcher:
    lp_size=500.0
    speed_scale=1.0
    def __init__(self, start_pos, on_launch):
       
        self.box=box(pos=start_pos, length=self.lp_size,
                     height=self.lp_size, width=self.lp_size, color=color.blue)
        self.launch_point=start_pos
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
        self.p=0

    def add_ball(self,at_pos, with_speed):
        b=sphere(pos=at_pos, radius=self.size, color=color.orange, make_trail=True, trail_type="points",
                 retain=400, interval=10)
        b.trail_object.size=1
        b.v=with_speed
        self.balls.append(b)
        self.p=self.p+1 #counts the balls
        ball_c.text='balls left- %s'%(str(5-self.p))
        

    def move(self,dt):
        for b in self.balls:    
            if self.p<=500:                        
                self.planet.gravity(b,dt)
                b.pos=b.pos+b.v*dt  
                if self.planet.hit(b):
                    self.balls.remove(b)
                if ((((b.pos[0]-cyl.pos[0])**2)/(0.1*cyl.radius**2))+(((b.pos[1]-cyl.pos[1])**2)/(0.98*cyl.radius**2)))<=1:
                    cyl.color=color.blue
                    self.balls.remove(b)
            else:
                 ball_c.visible=False               
                 win.text='YOU LOSE!!!...TRY AGAIN'
                 break

#this is where we run all the functions              
  
def main_loop():
    while true:
        m1=None
        if scene.mouse.events:
            m1 = scene.mouse.getevent() # get event
        launcher.run(deltat, m1)
        balls.move(deltat)
        earth.rotate(deltat)
        if cyl.color==color.blue:
            win.text='YOU WON!!!!'
            break
        
        rate(100)

#definig objects
        
earth=Earth()
balls=Balls(earth)
launcher=Launcher(launcher_pos, balls.add_ball)
deltat=0.01
cyl=ring(pos=(14000,3000,0),radius=900,color=color.yellow) #the hoop

main_loop()

