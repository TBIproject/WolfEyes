# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (1280, 720)
W, H = (640, 480)

# Création de la caméra
cam = Camera()
cam.init(0, width=W, height=H, exposure=-4)
cam.setFOV(horizontal=math.radians(92.0))
# cam.setImageVertBand(0.45, 0.5)
cam.setImageVertBand(0, 0.5)
cam.setAnoisek(radius=3)
cam.autoExposure()

def image_process(frame):
	frame = cv2.bilateralFilter(frame, *biblur_params).astype(np.float32)
	frame -= extend_GRAY2RGB(frame.mean(axis=2, dtype=np.float32))
	frame /= 255.0
	return frame
### END PROCESS
biblur_params = (11, 50, 50)
cam.onFrameGet = image_process

print 'looping...'
cam.setReference(count=10)
while 1:
	# On filme
	cam.getFrame()
	
	pixel_ratio = cam.reference / (cam.frame+1)
	pixel_rmean = pixel_ratio.mean()
	print pixel_rmean
	ref = cam.reference * pixel_rmean
	absdiff = cv2.absdiff(ref, cam.frame)
	
	cam.anoise(30)
	cam.arounder(
		maxCount=1000,
		minArea=200,
		maxDist=1,
		thick=1
	)
	
	# Affichage
	# cv2.imshow('reference', cam.reference)
	# cv2.imshow('complexe', cam.stream)
	# cv2.imshow('source', cam.frame)
	cv2.imshow('absdiff', absdiff)
	
	# Input management
	if Camera.keyEvents(): break
### END WHILE

# On ferme tout
Camera.closeCamApp()