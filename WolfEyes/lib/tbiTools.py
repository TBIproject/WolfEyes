# -*- coding: utf-8 -*-
import numpy as np
import sys

# PRINTF!!
def printf(txt):
	sys.stdout.write(txt)

# Dimensions d'une matrice (image)
def height(img): return np.shape(img)[0]
def width(img): return np.shape(img)[1]
def channels(img):
	shape = np.shape(img)
	return shape[2] if len(shape) > 2 else 1

# Image vide (easypeasy)
def Empty(**kargs):
	channels = kargs.get('channels', 3)
	height = kargs.get('height', 1)
	width = kargs.get('width', 1)
	return np.zeros((height, width, channels), np.uint8) if channels > 1 else np.zeros((height, width), np.uint8)
	
# Image vide depuis une autre image
def EmptyFrom(img, chan=None):
	if not chan: chan = channels(img)
	return Empty(height=height(img), width=width(img), channels=channels(img))