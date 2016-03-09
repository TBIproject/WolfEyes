# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (1280, 720)
W, H = (640, 480)

blockSize = pyon(
	width = 8,
	height = 8,
)

spread = 10

# Création de la caméra
cam = Camera()
cam.init(0, width=W, height=H, exposure=-4)
cam.setFOV(horizontal=math.radians(92.0))
cam.setImageVertBand(0.40, 0.48)

cam.setReference(count=10)
ref_deriv = cf.Scharr(cam.reference)
ref_deriv = cf.Gamma(ref_deriv, 0.5)
ref_deriv_mask = ((ref_deriv > 50) * 255).astype(np.uint8)
ref_deriv = ref_deriv & ref_deriv_mask

print 'looping...'

while 1:
	cam.getFrame()
	corrected_frame = cam.reference.copy()
	deriv = cf.Scharr(cam.frame)
	deriv = cf.Gamma(deriv, 0.5)
	deriv_mask = ((deriv > 50) * 255).astype(np.uint8)
	deriv = deriv & deriv_mask
	
	for y in xrange(0, deriv.shape[0], blockSize.height):
		filling = False
		can_close = True
		for x in xrange(0, deriv.shape[1], blockSize.width):
			ref_deriv_part = ref_deriv[y:y+blockSize.height, x:x+blockSize.width]
			deriv_part = deriv[y:y+blockSize.height, x:x+blockSize.width]
			
			deriv_diff = abs(int(ref_deriv_part.sum()) - int(deriv_part.sum())) / float(blockSize.width * blockSize.height * 3 * 255)
			
			if deriv_diff >= 0.1:
				corrected_frame[y-spread:y+blockSize.height+spread, x-spread:x+blockSize.width+spread] = cam.frame[y-spread:y+blockSize.height+spread, x-spread:x+blockSize.width+spread]

				# if can_close:
					# filling = not filling
					# can_close = False
			# else:
				# can_close = True
				
			# if filling:
				# corrected_frame[y-spread:y+blockSize.height+spread, x-spread:x+blockSize.width+spread] = cam.frame[y-spread:y+blockSize.height+spread, x-spread:x+blockSize.width+spread]
			# end if
		# end if
	# end for
	
	diff = cv2.absdiff(corrected_frame, cam.reference)
	diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
	diff = ((diff > 10) * 255).astype(np.uint8)
	
	cam._BINARY = diff.copy();
	
	cam.arounder(
		maxCount=1000,
		minArea=64,
		maxDist=5,
		thick=1
	)
	
	cv2.imshow('frame', cam.frame)
	cv2.imshow('deriv', deriv)
	cv2.imshow('corrected_frame', corrected_frame)
	cv2.imshow('diff', diff)
	cv2.imshow('stream', cam.stream)
	
	# Input management
	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break # On quitte
	
### END WHILE

# On ferme tout
Camera.closeCamApp()