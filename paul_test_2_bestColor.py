# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (1280, 720)
W, H = (640, 480)

# Création de la caméra
cam = Camera()
cam.init(0, width=W, height=H, exposure=-6)
cam.setFOV(horizontal=math.radians(92.0))
# cam.setImageVertBand(0.45, 0.5)
cam.setImageVertBand(0, 0.5)
# cam.setBlurSize(11)

mouse.SMOOTH = 5
stats = Statos(count=50)

print 'looping...'
cam.setReference(count=10)
while 1:
	# On filme
	cam.getFrame()
	# cam.equalize();
	
	# Affichage
	cv2.imshow('source', cam.frame)
	
	max = stats.feed(cam.frame)
	cv2.imshow('mean', stats.mean)
	if stats.DONE:
		inv = 255 - stats.mean
		cv2.imshow('best', inv)
		
		diff = cv2.absdiff(stats.mean, cam.frame)
		cv2.imshow('diff', diff)
		
	# Input management
	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break # On quitte
		
	elif sKey == ord(' '):
		stats.reset()
### END WHILE

# On ferme tout
Camera.closeCamApp()