# -*- coding: utf-8 -*-
"""Easy mouse controller"""

from pymouse import PyMouse
from D2Point import *

# Objet général
PYMOUSE = PyMouse()

# Dimensions de l'écran
SCREEN = D2Point(*PYMOUSE.screen_size())

# Boutons
LEFT = 1
RIGHT = 2
MIDDLE = 3

# Lock
DRAG = False

# Lissage du mouvement
SMOOTH = 2

def position():
	"""Return current mouse's position"""
	return D2Point(*PYMOUSE.position())
###

def smoothed(x, y):
	"""Return smoothed position depending on mouse current pos"""
	pos = position()
	vect = D2Point(x, y) - pos
	vect.length = vect.length/SMOOTH
	return pos + vect
###

def click(x, y, b=LEFT):
	"""Click with mouse's button 'b'"""
	x, y = ~smoothed(x, y).int
	PYMOUSE.click(x, y, b)
###	

def mouse_down(x, y, b=LEFT):
	"""Press down mouse's button 'b'"""
	x, y = ~smoothed(x, y).int
	PYMOUSE.press(x, y, b)
###

def mouse_up(x, y, b=LEFT):
	"""Release up mouse's button 'b'"""
	x, y = ~smoothed(x, y).int
	PYMOUSE.release(x, y, b)
###

def move(x, y):
	"""Move mouse according to smoothing"""
	x, y = ~smoothed(x, y).int
	PYMOUSE.move(int(x), int(y))
###

def drag(click, x, y):
	"""Memorize mouse click up/down and drags stuff
	 - click: is the user still clicking ?
	"""
	x, y = ~smoothed(x, y).int
	if DRAG: # Si on est en train de glisser
		
		# Si on clique toujours
		if click: move(x, y)
		
		else: # Si on arrête la glisse :O
			DRAG = False
			mouse_up(x, y)
	
	# Si c'est le premier clic
	else: mouse_down(x, y)
###