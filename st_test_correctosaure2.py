# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (1280, 720)
W, H = (640, 480)
exp = -4

# Création de la caméra 1
cam = Camera()
cam.init(0, width=W, height=H, exposure=-4)
cam.setFOV(horizontal=math.radians(92.0))
#cam1.setImageVertBand(0.45, 0.53)
#cam.autoExposure()
cam.setReference(count=10)

tolerance = 20

cam.getFrame()
old_frame = cam.frame

print 'looping...'

while 1:
	cam.getFrame()
	out_mask_rgb = np.logical_or(cam.frame > (old_frame.astype(np.int32) + tolerance), cam.frame < (old_frame.astype(np.int32) - tolerance))
	out_mask_gray = cv2.cvtColor(((out_mask_rgb.sum(axis=2) <= 1) * 255).astype(np.uint8), cv2.COLOR_GRAY2BGR)
	
	from_old = cv2.GaussianBlur(old_frame, (5, 5), 3) & out_mask_gray
	from_curr = cam.frame & cv2.bitwise_not(out_mask_gray)
	
	corrected_frame = from_old + from_curr
	old_frame = corrected_frame
	
	diff = cv2.absdiff(cam.reference, corrected_frame)
	diff = cv2.cvtColor(diff.max(axis=2), cv2.COLOR_GRAY2BGR)
	diff = ((diff > 20) * 255).astype(np.uint8)
	
	# Affichage
	
	cv2.imshow('diff', diff)
	cv2.imshow('corrected_frame', corrected_frame)
	cv2.imshow('cam.frame', cam.frame)

	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break # On quitte
	
### END WHILE

# On ferme tout
Camera.closeCamApp()