# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (1280, 720)
W, H = (640, 480)

# Création de la caméra
cam = Camera()
cam.init(0, width=W, height=H)#, exposure=-4)
cam.setFOV(horizontal=math.radians(92.0))
# cam.setImageVertBand(0.45, 0.5)
cam.setImageVertBand(0, 0.5)
cam.setAnoisek(radius=3)

mouse.SMOOTH = 5

print 'looping...'
cam.setReference(count=10)
while 1:
	for i in range(-10, -3):
		cam.setProp('exposure', i)
		for j in range(3): cam.getFrame()
		
		# On filme
		cam.getFrame()
		
		diff = cv2.absdiff(cam.frame, cam.reference)
		hist = histogram(cam.frame)
		h = imhist(cam.frame)
		print [i, histMean(h), cam.getProp('exposure')]
		
		# Affichage
		cv2.imshow('reference', cam.reference)
		cv2.imshow('source', cam.frame)
		cv2.imshow('diff', diff)
		cv2.imshow('hist', hist)
		
		# Input management
		sKey = Camera.waitKey(1000)
		if sKey == ord('q'): break # On quitte
			
		elif sKey == ord(' '):
			cam.setReference(count=10)
			
	if sKey == ord('q'): break
### END WHILE

# On ferme tout
Camera.closeCamApp()