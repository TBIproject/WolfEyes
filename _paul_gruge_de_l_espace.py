# -*- coding: utf-8 -*-
from WolfEyes import *

W, H = (1280, 720)
W, H = (640, 480)

# Création de la caméra
cam = Camera()
cam.init(0, width=W, height=H, exposure=-20)
cam.setFOV(horizontal=math.radians(92.0))
# cam.setImageVertBand(0.45, 0.5)
cam.setImageVertBand(0, 0.5)
cam.setAnoisek(radius=3)

biblur_params = (11, 50, 50)
def bibi(frame):
	frame = cv2.bilateralFilter(frame, *biblur_params)
	return frame
cam.onFrameGet = bibi

print 'looping...'
while 1:
	# On filme
	cam.getFrame()
	
	r = cam.spotDetector()
	# cam.anoise(0)
	cam.spotLocalizator(
		maxCount=100,
		minArea=4,
		thick=3
	)
	
	# Affichage
	# cv2.imshow('thresh', r.thresh * 255)
	cv2.imshow('complexe', cam.stream)
	# cv2.imshow('scan', cam.scan)
	# cv2.imshow('bin', cam.binary)
	# cv2.imshow('r', cam.frame[:,:,2])
	
	# Input management
	if Camera.keyEvents(): break
### END WHILE

# On ferme tout
Camera.closeCamApp()