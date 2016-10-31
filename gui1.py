"""<title>Hello World</title>
The simplest possble gui app that can be made.
Unfortunately, you have to CTRL-C from the command line to quit it.
GUI will initialize the screen for you.
"""

import pygame
from pygame.locals import *

import sys; sys.path.insert(0, "..")

from pgu import gui


app = gui.Desktop()

app.connect(gui.QUIT, app.quit, None)

c = gui.Table(width=200,height=120)

def cb():
    print(size.value, text.value, select.value)
    app.quit()

def updateSize():
    print((str(size.value)))


text = gui.TextArea(value="", width=150, height=70)
        
btn = gui.Button("Quit")
btn.connect(gui.CLICK, cb)

size = gui.HSlider(value=23,min=0,max=100,size=20,height=16,width=120)
size.connect(gui.CHANGE, updateSize)

c.tr()  
c.td(gui.Label("Select"))
select = gui.Select()

for i in range(1, 5):
    select.add(str(i),i)

    

select.connect(gui.CHANGE, cb)
c.td(select,colspan=3)

c.tr()
c.td(gui.Label("Button"))
c.td(btn, colspan = 3)

c.tr()
c.td(gui.Label("Size of board"))
c.td(size, colspan = 3)
c.td(gui.Label(str(size.value)))


c.tr()
c.td(gui.Label("Text area"))
c.td(text, colspan = 5)

c.tr()


app.run(c)
