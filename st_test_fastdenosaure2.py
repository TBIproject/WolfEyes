# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (1280, 720)
W, H = (640, 480)
exp = -4

# Création de la caméra 1
cam = Camera()
cam.init(0, width=W, height=H, exposure=-4)
cam.setFOV(horizontal=math.radians(92.0))
cam.setImageVertBand(0.40, 0.50)
cam.autoExposure()
cam.setReference(count=10)

corrected_ref = cv2.fastNlMeansDenoisingColored(cam.reference, searchWindowSize = 9, h = 40)
hsv_ref = cv2.cvtColor(corrected_ref, cv2.COLOR_BGR2HSV)
hsv_ref[:,:,2] = 255
hsv_ref = cv2.cvtColor(hsv_ref, cv2.COLOR_HSV2BGR)
	
print 'looping...'

while 1:
	cam.getFrame()
	
	corrected_frame = cv2.fastNlMeansDenoisingColored(cam.frame, searchWindowSize = 9, h = 40)
	
	hsv = cv2.cvtColor(corrected_frame, cv2.COLOR_BGR2HSV)
	hsv[:,:,2] = 255
	hsv = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
	
	diff = cv2.absdiff(hsv, hsv_ref)
	diff = cv2.cvtColor(diff.max(axis=2), cv2.COLOR_GRAY2BGR)
	diff = ((diff > 20) * 255).astype(np.uint8)
	
	# Affichage
	
	cv2.imshow('cam.frame', cam.frame)
	cv2.imshow('corrected_frame', corrected_frame)
	cv2.imshow('diff', diff)

	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break # On quitte
	
### END WHILE

# On ferme tout
Camera.closeCamApp()