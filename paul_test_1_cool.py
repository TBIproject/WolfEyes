# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (1280, 720)
# W, H = (640, 480)

# Création de la caméra
cam = Camera()
cam.init(0, width=W, height=H, exposure=-6)
cam.setFOV(horizontal=math.radians(92.0))
cam.setImageVertBand(0.4, 0.5)
# cam.setImageVertBand(0, 0.5)
cam.setAnoisek(radius=3)
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
	
	gdiff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
	# n = 100
	# thresh = cv2.adaptiveThreshold(gdiff, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 2*n+1, 0)
	# for i in xrange(6): thresh = cv2.medianBlur(thresh, 5);
	
	zseqfijdzq = cf.Gamma(gdiff, 1.5)
	S, thresh = cv2.threshold(zseqfijdzq, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	cam._BINARY = thresh
	
	cam.anoise(40)
	
	cam.arounder()
	
	b = cam.frame[:,:,0]
	g = cam.frame[:,:,1]
	r = cam.frame[:,:,2]
	
	# bg = cv2.medianBlur(g, 3)
	dg = cf.Scharr(cam.frame, 1)
	# bb = cv2.GaussianBlur(b, (5, 5), 1)
	
	# dg = ((dg > 32) * 255).astype(np.uint8)
	
	# Affichage
	cv2.imshow('reference', cam.reference)
	cv2.imshow('source', cam.frame)
	
	if S > 30:
		cv2.imshow('qdzqzdqzqz', zseqfijdzq)
		cv2.imshow('thresh', thresh)
		cv2.imshow('gdiff', gdiff)
		cv2.imshow('diff', diff)
		cv2.imshow('hist', hist)
	
	cv2.imshow('oij', cam.stream)
	
	# Input management
	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break # On quitte
		
	elif sKey == ord(' '):
		cam.setReference(count=10)
### END WHILE

# On ferme tout
Camera.closeCamApp()