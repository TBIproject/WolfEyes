# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (640, 240)

# Création de la caméra
cam = Camera()
cam.init(0, width=W, height=H, exposure=-6)
cam.setFOV(horizontal=math.radians(92.0))
cam.setImageVertBand(0, 0.5)

SIZE = 1000
BLACK_THRESH = 0.05
cv2.namedWindow('blackthresh')
cv2.createTrackbar('bthresh', 'blackthresh', int(BLACK_THRESH*SIZE), SIZE, lambda x: None)

# Pouet
cam.getFrame()

# stats
mean = np.zeros((H, W, 3), np.uint16)
stat = np.zeros((H, W, 3), np.uint8)

print 'looping...'
cam.setReference(count=10)
while 1:
	# On filme
	cam.getFrame()
	frame = cam.frame
	ref = cam.reference
	
	# Magic!
	"""[1] This is true magic !
	deriv = cf.Scharr(frame)
	fderiv = cf.Scharr(ref)
	
	# print mean.shape, deriv.shape, frame.shape
	mean += deriv
	dmean = mean / float(mean.max())
	
	# Difference entre dérivations
	# diff = np.abs(deriv.astype(int) - fderiv.astype(int)).astype(np.uint8)
	diff = cv2.absdiff(deriv, fderiv)
	"""#[1]endcomment"""
	
	# """[2] Fingers in the noise...
	BLACK_THRESH = cv2.getTrackbarPos('bthresh', 'blackthresh')/float(SIZE)
	
	# Différence entre normalisations
	black = grounder(frame)
	bref = grounder(ref)
	bdiff = cv2.absdiff(black, bref)
	bsum = (1.0/3) * (bdiff[:,:,0] + bdiff[:,:,1] + bdiff[:,:,2])
	bthresh = (bsum > BLACK_THRESH).astype(np.float32)
	"""#[2]endcomment"""
	
	# Display
	cv2.imshow('source', frame)
	# cv2.imshow('deriv', deriv)
	# cv2.imshow('diff', diff)
	cv2.imshow('black', black)
	cv2.imshow('blackdiff', bdiff)
	cv2.imshow('blacksum', bsum)
	cv2.imshow('blackthresh', bthresh)
	
	# Input management
	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break # On quitte
		
	elif sKey == ord(' '):
		cam.setReference(count=10)
### END WHILE

# On ferme tout
Camera.closeCamApp()