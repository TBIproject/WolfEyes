# -*- coding: utf-8 -*-
"""Curstom filter library"""
import numpy as np
import cv2

ScharrX = np.array([
	[3, 0, -3],
	[10, 0, -10],
	[3, 0, -3]
])

ScharrY = np.array([
	[3, 10, 3],
	[0, 0, 0],
	[-3, -10, -3]
])

###############################################################

#						W	I	P

###############################################################

# Custom pseudo-derivation method
def Deriv(img, kx=None, ky=None, dt=1):
	# Images
	x = y = img.astype(np.float32)
	if kx is None: kx = ScharrX
	if ky is None: ky = ScharrY
	
	# Dérivation(s)
	# 16 * 2 * 255 = 8160 max
	for i in xrange(dt):
		# On remet sur 255
		x = cv2.filter2D(x, -1, ScharrX) / 16.0
		y = cv2.filter2D(y, -1, ScharrY) / 16.0
	###
	
	return x, y
###

def Scharr(img, dt=1):
	result = np.zeros(img.shape, np.int16)
	
	x, y = Deriv(img, ScharrX, ScharrY, dt)
	
	result = (np.abs(x) + np.abs(y)) / 2.0
	return result.astype(np.uint8)
###

def Laplacian(img):
	return np.abs(cv2.filter2D(img.astype(np.int16), -1, np.array([
		[0, 0.5, 0],
		[0.5, 0, -0.5],
		[0, -0.5, 0]
	]))).astype(np.uint8)
###

def Gamma(img, gamma=1):
	return (((img / 255.0) ** gamma) * 255).astype(np.uint8)
###

def Gamma2(img, gamma=1):
	return ((img ** gamma) / (255.0 ** (gamma - 1))).astype(np.uint8)
###