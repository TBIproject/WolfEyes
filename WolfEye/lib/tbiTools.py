# -*- coding: utf-8 -*-
import numpy as np
import sys

# PRINTF!!
def printf(txt):
	sys.stdout.write(txt)

# USELESS !!!!
# Pour récupérer facilement les kargs
def arg(kargs, key, default=None):
	raise Exception("Utilisez '[dictObject].get(value, default)' plutot !!")
	# return kargs[key] if key in kargs else default

# Dimensions d'une matrice (image)
def height(img): return np.shape(img)[0]
def width(img): return np.shape(img)[1]

# Image vide (easypeasy)
def Empty(): return np.zeros((1, 1), np.uint8)