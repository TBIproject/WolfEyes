# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (1280, 720)
W, H = (640, 480)

# Création de la caméra
cam = Camera()
cam.init(0, width=W, height=H, exposure=-6)
cam.setFOV(horizontal=math.radians(92.0))
# cam.setImageVertBand(0.45, 0.5)
cam.setImageVertBand(0, 0.5)
# cam.setBlurSize(11)

mouse.SMOOTH = 5
stats = Statos(count=50)

print 'looping...'
cam.setReference(count=10)
while 1:
	# On filme
	cam.getFrame()
	
	# Affichage
	cv2.imshow('source', cam.frame)
	
	max = stats.feed(cam.frame)
	cv2.imshow('mean', stats.mean)
	if stats.DONE:
		cv2.imshow('max', max)
		
		diff = cv2.absdiff(stats.mean, cam.frame)
		ok = diff.sum(axis=2) >= max.sum(axis=2)+1
		
		cv2.imshow('diff', diff)
		cv2.imshow('thresh', (ok * 255).astype(np.uint8))
	
	# Input management
	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break # On quitte
		
	elif sKey == ord(' '):
		# cam.setReference(count=10)
		stats.reset()
### END WHILE

# On ferme tout
Camera.closeCamApp()