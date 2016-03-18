# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (1280, 720)
W, H = (640, 480)

# Création de la caméra
cam = Camera()
cam.init(0, width=W, height=H, exposure=-5)
cam.setFOV(horizontal=math.radians(92.0))
# cam.setImageVertBand(0.45, 0.5)
cam.setImageVertBand(0, 0.5)
cam.setAnoisek(radius=3)
# cam.autoExposure()

def extend_GRAY2BGR(img):
	return np.repeat(img[:, :, np.newaxis], 3, axis=2)

biblur_params = (11, 50, 50)
def image_to0(frame):
	frame = cv2.bilateralFilter(frame, *biblur_params)
	# max = extend_GRAY2BGR(frame.max(axis=2))
	# min = extend_GRAY2BGR(frame.min(axis=2))
	avg = extend_GRAY2BGR(frame.mean(axis=2))
	return frame.astype(np.float32) - avg.astype(np.float32)
def image_toAVG(frame):
	frame = cv2.bilateralFilter(frame, *biblur_params)
	return frame
cam.onFrameGet = image_toAVG

print 'looping...'
cam.setReference(count=10)
while 1:
	# On filme
	cam.getFrame()
	
	# print cam.frame
	# print cam.reference
	diff = cv2.absdiff(cam.frame, cam.reference)
	sdiff = diff.sum(axis=2)
	# sdiff = cf.Gamma(sdiff, 0.2)
	
	MAX = sdiff.max()
	MEAN = sdiff.mean()
	
	s = sdiff.mean() * 1.1 # Hell yea
	T = 0.2 * (MAX - MEAN) + MEAN
	# S, thresh = cv2.threshold(sdiff.astype(np.uint8), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	S, thresh = cv2.threshold(sdiff.astype(np.uint8), T, 255, cv2.THRESH_BINARY)
	printf('%10s / %s / %s\r' % (T, MEAN, MAX))
	# if S > s:
		# print 'OK'
		# cam._BINARY = thresh
	
	cam.anoise(50)
	cam.arounder(
		quiet=True,
		maxCount=1000,
		minArea=200,
		maxDist=1,
		thick=1
	)
	
	frame = cam.frame - extend_GRAY2BGR(cam.frame.min(axis=2))
	reference = cam.reference - extend_GRAY2BGR(cam.reference.min(axis=2))
	# print reference
	# print frame
	
	# Affichage
	# cv2.imshow('complexe', cam.stream)
	cv2.imshow('reference', reference.astype(np.uint8))
	cv2.imshow('source', frame.astype(np.uint8))
	cv2.imshow('sdiff', sdiff.astype(np.uint8))
	cv2.imshow('thresh', thresh)
	
	# Input management
	if Camera.keyEvents(): break
### END WHILE

# On ferme tout
Camera.closeCamApp()