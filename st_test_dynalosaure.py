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
tolerance_maxes = (maxes.astype(np.int32) + yolol).clip(0, 255).astype(np.uint8)
tolerance_mines = (mines.astype(np.int32) - yolol).clip(0, 255).astype(np.uint8)

for i in range(19):
	cam.getFrame()
	ref = ref / 2 + cam.frame / 2
	maxes = np.maximum(maxes, cam.frame)
	mines = np.minimum(mines, cam.frame)


print 'looping...'

while 1:
	cam.getFrame()
	valid_pixels_mask = np.logical_and(cam.frame > mines, cam.frame < maxes) * 255
	over_pixels_mask = np.logical_and(cam.frame >= maxes, cam.frame <= tolerance_maxes) * 255
	under_pixels_mask = np.logical_and(cam.frame >= tolerance_mines, cam.frame <= mines) * 255
	unknown_over_mask = (cam.frame > tolerance_maxes) * 255
	unknown_under_mask = (cam.frame < tolerance_mines) * 255
	corrected_frame = (cam.frame & valid_pixels_mask) + (maxes & over_pixels_mask) + (mines & under_pixels_mask) + (cam.frame & unknown_over_mask) + (cam.frame & unknown_under_mask)
	
	diff = cv2.absdiff(corrected_frame.astype(np.uint8), ref.astype(np.uint8))
	result = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
	result = (result > 20) * 255
	result = cv2.medianBlur(result.astype(np.uint8), 3)
	
	temoinosaure = cv2.absdiff(cam.frame, ref)
	temoinosaure = cv2.cvtColor(temoinosaure, cv2.COLOR_BGR2GRAY)
	temoinosaure = (temoinosaure > 20) * 255
	temoinosaure = cv2.medianBlur(temoinosaure.astype(np.uint8), 3)
	
	# Affichage
	cv2.imshow('cam', cam.frame)
	#cv2.imshow('diff', diff.astype(np.uint8))
	cv2.imshow('corrected_frame', corrected_frame.astype(np.uint8))
	cv2.imshow('result', result)
	cv2.imshow('temoinosaure', temoinosaure)
	
	# Input management
	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break # On quitte
	
### END WHILE

# On ferme tout
Camera.closeCamApp()