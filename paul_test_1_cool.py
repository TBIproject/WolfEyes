# -*- coding: utf-8 -*-
from WolfEyes.work import *

# W, H = (1280, 720)
W, H = (640, 480)

# Création de la caméra
cam = Camera()
cam.init(0, width=W, height=H, exposure=-6)
cam.setFOV(horizontal=math.radians(92.0))
cam.setImageVertBand(0.4, 0.5)
# cam.setImageVertBand(0, 0.5)
cam.setAnoisek(radius=3)
# cam.setBlurSize(11)

mouse.SMOOTH = 5

def process(cam):
	diff = cv2.absdiff(cam.frame, cam.reference)
	hist = histogram(cam.frame)
	
	gdiff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
	# n = 100
	# thresh = cv2.adaptiveThreshold(gdiff, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 2*n+1, 0)
	# for i in xrange(6): thresh = cv2.medianBlur(thresh, 5);
	
	zseqfijdzq = cf.Gamma(gdiff, 1.5)
	S, thresh = cv2.threshold(zseqfijdzq, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	cam._BINARY = thresh
	
	b = cam.frame[:,:,0]
	g = cam.frame[:,:,1]
	r = cam.frame[:,:,2]
	
	# bg = cv2.medianBlur(g, 3)
	dg = cf.Scharr(cam.frame, 1)
	# bb = cv2.GaussianBlur(b, (5, 5), 1)
	
	# dg = ((dg > 32) * 255).astype(np.uint8)
	
	cv2.imshow('qdzqzdqzqz', zseqfijdzq)
	cv2.imshow('thresh', thresh)
	cv2.imshow('gdiff', gdiff)
	cv2.imshow('diff', diff)
	cv2.imshow('hist', hist)
###

def AdaptivThresh(frame, color = True):
	if color: frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	return cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

def meanThresh(cam, frames=10):
	M = 0.0;
	for i in xrange(frames):
		cam.getFrame()
		
		p = absdiffthresh(cam)
		M += p.seuil
		
		Camera.waitKey()
	return M / frames
###

def absdiffthresh(cam):
	diff = cv2.absdiff(cam.frame, cam.reference)
	gdiff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
	
	# gdiff = cf.Gamma(gdiff, 1)
	S, thresh = AdaptivThresh(gdiff, False)
	cam._BINARY = thresh
	
	return pyon(
		gray = gdiff,
		thresh = thresh,
		diff = diff,
		seuil = S
	)

print 'looping...'
cam.setReference(count=10)
mean = meanThresh(cam, 10)
while 1:
	# On filme
	cam.getFrame()
	
	hist = histogram(cam.frame)
	
	p = absdiffthresh(cam)
	S = p.seuil
	
	b = cam.frame[:,:,0]
	g = cam.frame[:,:,1]
	r = cam.frame[:,:,2]
	
	# bg = cv2.medianBlur(g, 3)
	dg = cf.Scharr(cam.frame, 1)
	# bb = cv2.GaussianBlur(b, (5, 5), 1)
	
	# dg = ((dg > 32) * 255).astype(np.uint8)
	
	print [S, mean]
	if S > 1.5 * mean:
		cam.anoise(50)
		
		cam.arounder(
			maxCount=500,
			minArea=36,
			maxDist=1,
			thick=2
		)
	###
	
	# Affichage
	cv2.imshow('reference', cam.reference)
	cv2.imshow('source', cam.frame)
	cv2.imshow('stream', cam.stream)
	
	cv2.imshow('thresh', p.thresh)
	cv2.imshow('gdiff', p.gray)
	cv2.imshow('diff', p.diff)
	cv2.imshow('hist', hist)
	
	# Input management
	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break # On quitte
		
	elif sKey == ord(' '):
		cam.setReference(count=10)
### END WHILE

# On ferme tout
Camera.closeCamApp()