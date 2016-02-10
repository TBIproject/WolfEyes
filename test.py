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

print 'looping...'
cam.setReference(count=10)
while 1:
	# On filme
	cam.getFrame()
	# cam.equalize();
	
	diff = cv2.absdiff(cam.frame, cam.reference)
	hist = histogram(cam.frame)
	
	b = cam.frame[:,:,0]
	g = cam.frame[:,:,1]
	r = cam.frame[:,:,2]
	
	hb = histogram(b)
	hg = histogram(g)
	hr = histogram(r)
	
	bg = cv2.medianBlur(g, 3)
	# dg = cv2.Sobel(cam.frame, cv2.CV_64F, 1, 1, ksize=-1)
	dg = cf.Scharr(cam.frame, 1)
	bb = cv2.GaussianBlur(b, (5, 5), 1)
	lapl = cf.Laplacian(cam.frame)
	
	# dg = ((dg > 32) * 255).astype(np.uint8)
	
	# Affichage
	cv2.imshow('source', cam.frame)
	# cv2.imshow('reference', cam.reference)
	# cv2.imshow('diff', diff)
	cv2.imshow('qzdqzdqzd', hist)
	cv2.imshow('Laplacian', lapl)
	# cv2.imshow('r', r)
	cv2.imshow('g', g)
	# cv2.imshow('b', b)
	cv2.imshow('bg', bg)
	# cv2.imshow('bb', bb)
	cv2.imshow('dg', dg)
	
	# Input management
	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break # On quitte
		
	elif sKey == ord(' '):
		cam.setReference(count=10)
### END WHILE

# On ferme tout
Camera.closeCamApp()