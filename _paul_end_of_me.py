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
# cam.autoExposure(start=-10)

def grayExpansion(img):
	sum = img.sum(axis=2)
	return sum / sum.max()

biblur_params = (11, 50, 50)
def image_toAVG(frame):
	frame = cv2.bilateralFilter(frame, *biblur_params).astype(np.float32) / 255
	return frame
	
# Blblblblblbll
cam.onFrameGet = image_toAVG

print 'looping...'
cam.setReference(count=10)
while 1:
	# On filme
	cam.getFrame()
	img = cam.frame
	
	a = cam.frame
	b = cam.reference
	for i in xrange(1):
		diff = cv2.absdiff(a, b)
	diff = grayExpansion(diff)
	
	# Affichage
	# cv2.imshow('complexe', cam.stream)
	cv2.imshow('reference', cam.reference)
	cv2.imshow('source', cam.frame)
	cv2.imshow('w00t', img)
	cv2.imshow('diff', diff)
	
	# Input management
	if Camera.keyEvents(): break
### END WHILE

# On ferme tout
Camera.closeCamApp()