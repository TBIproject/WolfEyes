# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (1280, 720)
W, H = (640, 480)

# Création de la caméra
cam = Camera()
cam.init(0, width=W, height=H, exposure=-6)
cam.setFOV(horizontal=math.radians(92.0))
cam.setImageVertBand(0, 0.5)
cam.setAnoisek(radius=3)

mouse.SMOOTH = 5
thresh = 15

# cam.onFrameGet = crash

print 'looping...'
cam.setReference(count=10)
while 1:
	# On filme
	cam.getFrame()
	
	"""
	scharr = cf.Scharr(cv2.cvtColor(cam.frame, cv2.COLOR_BGR2GRAY))
	_, area = cv2.threshold(scharr, thresh, 255, cv2.THRESH_BINARY_INV)
	mask = np.zeros(cam.frame.shape, cam.frame.dtype)
	for i in xrange(3): mask[:, :, i] = area;
	disp = mask & cam.frame"""
	
	
	
	# Affichage
	cv2.imshow('reference', cam.reference)
	cv2.imshow('source', cam.frame)
	
	# Input management
	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break # On quitte
		
	elif sKey == ord(' '):
		cam.setReference(count=10)
### END WHILE

# On ferme tout
Camera.closeCamApp()