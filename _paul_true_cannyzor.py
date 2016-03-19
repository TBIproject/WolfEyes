# -*- coding: utf-8 -*-
from WolfEyes import *

W, H = (1280, 720)
W, H = (640, 480)

# Création de la caméra
cam = Camera()
cam.init(0, width=W, height=H, exposure=-6)
cam.setFOV(horizontal=math.radians(92.0))
# cam.setImageVertBand(0.45, 0.5)
cam.setImageVertBand(0, 0.5)
cam.setAnoisek(radius=3)
# cam.autoExposure(start=-10)

biblur_params = (11, 50, 50)
def image_toAVG(frame):
	frame = cv2.bilateralFilter(frame, *biblur_params)
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# frame = cv2.bilateralFilter(frame, *biblur_params)
	# frame = cv2.medianBlur(frame, 5)
	return frame
	
# Blblblblblbll
cam.onFrameGet = image_toAVG

print 'looping...'
cam.setReference(count=10)
while 1:
	# On filme
	cam.getFrame()
	frame = cam.frame
	
	# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	frame = cv2.Canny(frame, 30, 25)
	
	# Affichage
	# cv2.imshow('complexe', cam.stream)
	cv2.imshow('reference', cam.reference)
	cv2.imshow('source', cam.frame)
	cv2.imshow('canny', frame)
	
	# Input management
	if Camera.keyEvents(): break
### END WHILE

# On ferme tout
Camera.closeCamApp()