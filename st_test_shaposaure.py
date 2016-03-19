# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (1280, 720)
W, H = (640, 480)

blockSize = pyon(
	width = 5,
	height = 5,
)

spread = 20

# Création de la caméra
cam = Camera()
cam.init(0, width=W, height=H)
cam.autoExposure()
cam.setFOV(horizontal=math.radians(92.0))
cam.setImageVertBand(0.40, 0.50)

def toAVG(frame):
	frame = cv2.bilateralFilter(frame, 25, 10, 25)
	frame = cv2.medianBlur(frame, 5)
	return frame

cam.onFrameGet = toAVG

print 'looping...'

cam.setReference(count=10)
ref_deriv = (cam.reference.astype(np.float32))
ref_deriv = cf.Scharr(ref_deriv).sum(axis=2)

pute = 255 * 3

while 1:
	cam.getFrame()
	corrected_frame = cam.reference.copy()
	deriv = (cam.frame.astype(np.float32))
	deriv = cf.Scharr(deriv).sum(axis=2)
	
	#intersect = (((ref_deriv + deriv) > deriv.max()) * 255).astype(np.uint8)
	
	result = ((deriv + ref_deriv) / (pute * 2)).astype(np.float32)
	deriv = (deriv / pute).astype(np.float32)
	
	prod = 10 * deriv * (ref_deriv / pute)
	# result = (result + prod) / 2.0
	
	cv2.imshow('frame', cam.frame)
	cv2.imshow('deriv', deriv)
	cv2.imshow('result', result)
	cv2.imshow('intersect', prod)
	
	# Input management
	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break # On quitte
	
### END WHILE

# On ferme tout
Camera.closeCamApp()