# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (1280, 720)
W, H = (640, 480)

# Création de la caméra
cam = Camera()
cam.init(0, width=W, height=H, exposure=-4)
cam.setFOV(horizontal=math.radians(92.0))
				  
cam.getFrame()
ref = cam.frame
maxes = cam.frame
mines = cam.frame

for i in range(9):
	cam.getFrame()
	ref = ref / 2 + cam.frame / 2
	maxes = np.maximum(maxes, cam.frame)
	mines = np.minimum(mines, cam.frame)


print 'looping...'

while 1:
	cam.getFrame()
	valid_pixels_mask = np.logical_and(cam.frame >= mines, cam.frame <= maxes) * 255
	over_pixels_mask = (cam.frame > maxes) * 255
	under_pixels_mask = (cam.frame < mines) * 255
	result = (cam.frame & valid_pixels_mask) + (maxes & over_pixels_mask) + (mines & under_pixels_mask)
	
	# Affichage
	cv2.imshow('dsgdfg', cam.frame)
	cv2.imshow('source', result.astype(np.uint8))
	
	# Input management
	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break # On quitte
	
### END WHILE

# On ferme tout
Camera.closeCamApp()