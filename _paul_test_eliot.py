# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (1280, 720)
W, H = (640, 480)

# Création de la caméra
cam = Camera()
cam.init(0, width=W, height=H, exposure=-4)
cam.setFOV(horizontal=math.radians(92.0))
# cam.setImageVertBand(0.45, 0.5)
cam.setImageVertBand(0, 0.5)
cam.setAnoisek(radius=3)
cam.autoExposure()

biblur_params = (11, 50, 50)
cam.onFrameGet = lambda frame: cv2.bilateralFilter(frame, *biblur_params)

print 'looping...'
cam.setReference(count=10)
while 1:
	# On filme
	cam.getFrame()
	
	Y = cam.reference
	mY = Y.mean()
	
	X = cam.frame
	mX = X.mean()
	
	a = (Y - mY) / (X+0.0000001 - mX)
	b = Y - a*X
	
	# print a.mean()
	# print b.mean()
	
	cam.anoise(50)
	cam.arounder(
		quiet=True,
		maxCount=1000,
		minArea=200,
		maxDist=1,
		thick=1
	)
	
	# Affichage
	# cv2.imshow('reference', cam.reference)
	# cv2.imshow('complexe', cam.stream)
	cv2.imshow('source', cam.frame)
	cv2.imshow('source', cam.frame - b)
	
	# Input management
	if Camera.keyEvents(): break
### END WHILE

# On ferme tout
Camera.closeCamApp()