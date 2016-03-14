# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (1280, 720)
W, H = (640, 480)
exp = -4

# Création de la caméra 1
cam = Camera()
cam.init(0, width=W, height=H)
cam.setFOV(horizontal=math.radians(92.0))
#cam1.setImageVertBand(0.45, 0.53)
cam.autoExposure()

tolerance = 20

cam.getFrame()
old_frame = cam.frame

print 'looping...'

while 1:
	cam.getFrame()
	out_mask_rgb = np.logical_or(cam.frame > (old_frame.astype(np.int32) + tolerance), cam.frame < (old_frame.astype(np.int32) - tolerance))
	out_mask_gray = cv2.cvtColor((out_mask_rgb.sum(axis=2) < 3).astype(np.uint8), cv2.COLOR_GRAY2BGR)
	
	from_old = old_frame & (out_mask_gray * 255)
	from_curr = cam.frame & (~out_mask_gray * 255)
	
	corrected_frame = from_old + from_curr

	# Affichage
	
	cv2.imshow('corrected_frame', corrected_frame)
	cv2.imshow('cam.frame', cam.frame)

	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break # On quitte
	
### END WHILE

# On ferme tout
Camera.closeCamApp()