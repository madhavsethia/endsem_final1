# -*- coding: utf-8 -*-
"""
Created on Sat May 10 07:50:25 2014

@author: Administrator
"""

from visual import *
import time
time.sleep(2)
p = label(text='THIS IS SPACE HOOPS')
time.sleep(2)
p.text=("""THIS IS SPACE LOOPS 
SELECT THE LEVEL YOU WANNA PLAY""")
time.sleep(2)
p.text=("""THIS IS SPACE HOOPS 
SELECT THE LEVEL YOU WANNA PLAY
BEGINNERS- HIT 1
PROS- HIT 2""")
time.sleep(2)
p.text=("""THIS IS SPACE HOOPS 
SELECT THE LEVEL YOU WANNA PLAY
BEGINNERS- HIT 1
PROS- HIT 2
SO WHICH WILL IT BE ?""")

while True:
    rate(30)
    if scene.kb.keys: # event waiting to be processed?
        s = scene.kb.getkey() # get keyboard info
        if s==str(1):
            import lvl1
            time.sleep(0.5)
        if s==str(2):
            import lvl2
            time.sleep(0.5)
            