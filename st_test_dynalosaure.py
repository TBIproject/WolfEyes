# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (1280, 720)
W, H = (640, 480)

# Création de la caméra
cam = Camera()
cam.init(0, width=W, height=H, exposure=-4)
cam.setFOV(horizontal=math.radians(92.0))

yolol = 20
				  
cam.getFrame()
ref = cam.frame
maxes = cam.frame
mines = cam.frame

for i in range(19):
	cam.getFrame()
	ref = ref / 2 + cam.frame / 2
	maxes = np.maximum(maxes, cam.frame)
	mines = np.minimum(mines, cam.frame)


print 'looping...'

while 1:
	cam.getFrame()
	valid_pixels_mask = np.logical_and(cam.frame >= mines, cam.frame <= maxes) * 255
	over_pixels_mask = np.logical_and(cam.frame > maxes, cam.frame <= maxes + yolol) * 255
	under_pixels_mask = np.logical_and(cam.frame >= mines - yolol, cam.frame < mines) * 255
	unknown_over_mask = (cam.frame > maxes + yolol) * 255
	unknown_under_mask = (cam.frame < mines - yolol) * 255
	corrected_frame = (cam.frame & valid_pixels_mask) + (maxes & over_pixels_mask) + (mines & under_pixels_mask) + (cam.frame & unknown_over_mask) + (cam.frame & unknown_under_mask)
	
	diff = cv2.absdiff(corrected_frame.astype(np.uint8), ref.astype(np.uint8))
	result = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
	result = (result > 20) * 255
	result = cv2.medianBlur(result.astype(np.uint8), 3)
	
	# Affichage
	cv2.imshow('cam', cam.frame)
	cv2.imshow('diff', diff.astype(np.uint8))
	cv2.imshow('result', result)
	
	# Input management
	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break # On quitte
	
### END WHILE

# On ferme tout
Camera.closeCamApp()