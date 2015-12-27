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

print 'looping...'
cam.setReference(count=10)
while 1:
	# On filme
	cam.getFrame()
	
	diff = cv2.absdiff(cam.frame, cam.reference)
	
	# Affichage
	cv2.imshow('source', cam.frame)
	cv2.imshow('reference', cam.reference)
	cv2.imshow('diff', diff)
	
	
	
	# Input management
	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break # On quitte
		
	elif sKey == ord(' '):
		cam.setReference(count=10)
### END WHILE

# On ferme tout
Camera.closeCamApp()