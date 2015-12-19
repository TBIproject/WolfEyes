# -*- coding: utf-8 -*-
from pymouse import PyMouse
from D2Point import *

# Objet g�n�ral
PYMOUSE = PyMouse()

# Dimensions de l'�cran
SCREEN = D2Point(*PYMOUSE.screen_size())

# Boutons
LEFT = 1
RIGHT = 2
MIDDLE = 3

# Lock
DRAG = False

# Lissage du mouvement
SMOOTH = 1

def position():
	return D2Point(*PYMOUSE.position())
###

def smoothed(x, y):
	pos = position()
	vect = D2Point(x, y) - pos
	vect.length = vect.length/SMOOTH
	return pos + vect
###

def click(x, y, b=LEFT):
	x, y = ~smoothed(x, y).int
	PYMOUSE.click(x, y, b)
###	

def mouse_down(x, y, b=LEFT):
	x, y = ~smoothed(x, y).int
	PYMOUSE.press(x, y, b)
###

def mouse_up(x, y, b=LEFT):
	x, y = ~smoothed(x, y).int
	PYMOUSE.release(x, y, b)
###

def move(x, y):
	x, y = ~smoothed(x, y).int
	PYMOUSE.move(int(x), int(y))
###

def drag(click, x, y):
	x, y = ~smoothed(x, y).int
	if DRAG: # Si on est en train de glisser
		
		# Si on clique toujours
		if click: move(x, y)
		
		else: # Si on arr�te la glisse :O
			DRAG = False
			mouse_up(x, y)
	
	# Si c'est le premier clic
	else: mouse_down(x, y)
###