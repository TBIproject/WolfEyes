# -*- coding: utf-8 -*-
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

def Deriv(img):
	pass
###

def Scharr(img, dt=1):
	
	# Images
	result = np.zeros(img.shape, np.int16)
	cvt = img
	
	# Dérivation(s)
	for x in xrange(dt):
		cvt = cvt.astype(np.int16)
		x = cv2.filter2D(cvt, -1, ScharrX)
		y = cv2.filter2D(cvt, -1, ScharrY)
		
		# 16 * 2 * 255 = 8160 max
		result = (np.abs(x) + np.abs(y)) / 32
		cvt = result
	
	return result
###

def Gamma(img, gamma=1):
	pass
###