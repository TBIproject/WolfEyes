# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (1280, 720)
W, H = (640, 480)

# Création de la caméra
cam = Camera()
cam.init(0, width=W, height=H)
cam.autoExposure()
cam.setFOV(horizontal=math.radians(92.0))
#cam.setImageVertBand(0.42, 0.50)

print 'looping...'

while 1:
	cam.getFrame()
	bi = cv2.bilateralFilter(cam.frame, 11, 50, 50)
	hsv = cv2.cvtColor(bi, cv2.COLOR_BGR2HSV)
	hsv[:,:,2] = 255
	hsv = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
	weird = (((hsv[:,:,0]**2 + hsv[:,:,1]**2) ** 0.5) * (2**0.5)).astype(np.uint8) # FUCK YOU HSV ~ POL
	
	cv2.imshow('frame', cam.frame)
	cv2.imshow('bi', bi)
	cv2.imshow('hsv', hsv)
	cv2.imshow('weird', weird)
	
	# Input management
	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break # On quitte
	
### END WHILE

# On ferme tout
Camera.closeCamApp()