# -*- coding: utf-8 -*-
from pymouse import PyMouse

# Objet général
PYMOUSE = PyMouse()

SCREEN_WIDTH, SCREEN_HEIGHT = PYMOUSE.screen_size()

# Boutons
LEFT = 1
RIGHT = 2
MIDDLE = 3

# Lock
DRAG = False

def click(x, y, b=LEFT):
	PYMOUSE.click(x, y, b)
###	

def mouse_down(x, y, b=LEFT):
	PYMOUSE.press(x, y, b)
###

def mouse_up(x, y, b=LEFT):
	PYMOUSE.release(x, y, b)
###

def move(x, y):
	PYMOUSE.move(x, y)
###

def drag(x, y, click):
	if DRAG: # Si on est en train de glisser
		
		# Si on clique toujours
		if click: move(x, y)
		
		else: # Si on arrête la glisse :O
			DRAG = False
			mouse_up(x, y)
	
	# Si c'est le premier clic
	else: mouse_down(x, y)
###