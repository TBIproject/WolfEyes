# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (1280, 720)
W, H = (640, 480)
blockSize = (10,10)

# Création de la caméra
cam = Camera()
cam.init(0, width=W, height=H, exposure=-4)
cam.setFOV(horizontal=math.radians(92.0))
#cam.setImageVertBand(0.45, 0.51)

cam.setReference(count=10)
ref_deriv = cf.Scharr(cam.reference)

ref_deriv_part = ref_deriv[0:blockSize[1], 0:blockSize[0]]
print(float(ref_deriv_part.sum()) / float((blockSize[1] * blockSize[0]) * 3))

print 'looping...'

while 1:
	cam.getFrame()
	corrected_frame = cam.reference
	deriv = cf.Scharr(cam.frame)
	
	
	
	for y in xrange(0, deriv.shape[1], blockSize[1]):
		for x in xrange(0, deriv.shape[0], blockSize[0]):
			ref_deriv_part = ref_deriv[y:y+blockSize[1], x:x+blockSize[0]]
			deriv_part = deriv[y:y+blockSize[1], x:x+blockSize[0]]
		#end if
	#end for
	
	cv2.imshow('diff', deriv)
	
	# Input management
	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break # On quitte
	
### END WHILE

# On ferme tout
Camera.closeCamApp()