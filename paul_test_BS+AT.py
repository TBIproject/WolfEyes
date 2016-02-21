# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (640, 240)

# Création de la caméra
cam = Camera()
cam.init(0, width=W, height=H, exposure=-6)
cam.setFOV(horizontal=math.radians(92.0))
cam.setImageVertBand(0, 0.5)

stats = Statos(count=50)

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
	
	# """[1] Fingers in the noise...
	
	# Différence entre normalisations
	black = grounder(frame)
	bref = grounder(ref)
	
	max = stats.feed(black)
	cv2.imshow('mean', stats.mean)
	if stats.DONE:
		cv2.imshow('max', max)
		
		diff = cv2.absdiff(stats.mean, black)
		sdiff = diff.sum(axis=2)
		ok = sdiff >= max.sum(axis=2)+1
		
		cv2.imshow('diff', diff)
		cv2.imshow('sdiff', (sdiff / 3.0).astype(np.uint8))
		cv2.imshow('thresh', (ok * 255).astype(np.uint8))
		
	"""#[1]endcomment"""
	
	# Source image
	cv2.imshow('source', frame)
	
	# Input management
	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break # On quitte
		
	elif sKey == ord(' '):
		cam.setReference(count=10)
### END WHILE

# On ferme tout
Camera.closeCamApp()