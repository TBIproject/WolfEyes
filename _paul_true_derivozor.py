# -*- coding: utf-8 -*-
from WolfEyes import *

W, H = (1280, 720)
W, H = (640, 480)

# Création de la caméra
cam = Camera()
cam.init(0, width=W, height=H, exposure=-6)
cam.setFOV(horizontal=math.radians(92.0))
# cam.setImageVertBand(0.45, 0.5)
cam.setImageVertBand(0, 0.5)
cam.setAnoisek(radius=3)
# cam.autoExposure(start=-10)

biblur_params = (11, 50, 50)
gaussblur_params = ((5,5), 10)
def image_to0(frame):
	frame = cv2.bilateralFilter(frame, *biblur_params)
	# max = extend_GRAY2BGR(frame.max(axis=2))
	# min = extend_GRAY2BGR(frame.min(axis=2))
	avg = extend_GRAY2BGR(frame.mean(axis=2))
	return frame.astype(np.float32) - avg.astype(np.float32)
	
def image_toAVG(frame):
	frame = cv2.bilateralFilter(frame, *biblur_params)
	frame = cv2.medianBlur(frame, 5)
	return frame
	
# Blblblblblbll
cam.onFrameGet = image_toAVG
dilate = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
d2coef = 3

def accentuate(deriv):
	# On utilise la dérivée seconde pour marquer les arrêtes
	# deriv_ = cf.Scharr(deriv).sum(axis=2).astype(np.float32) / 3 / 255
	deriv_ = cf.Scharr(deriv).astype(np.float32) / 255
	deriv = (deriv / 255 - d2coef * deriv_).clip(0, 1)
	return deriv

# ZDQQDZZZZZDZDZDZ
def process(deriv, d=False):
	# On traite la dérivée pour obtenir les contours
	img = deriv.sum(axis=2).astype(np.float32) / 3
	img = cf.Gamma(img, 0.5, np.float32)
	img = accentuate(img)
	
	# Stats
	MEAN = img.mean()
	MAX = img.max()
	
	# Seuillage
	# if d: print MEAN
	# t, img = cv2.threshold(img, 0.4 * (MAX - MEAN) + MEAN, 1, cv2.THRESH_BINARY)
	return img

print 'looping...'
cam.setReference(count=10)
while 1:
	# On filme
	cam.getFrame()
	
	dr = cf.Scharr(cam.reference)
	df = cf.Scharr(cam.frame)
	
	# a = dr.mean() / df.mean()
	# df *= a
	
	ref = process(dr)
	frame = process(df, True)
	
	fref = cv2.GaussianBlur(ref, *gaussblur_params)
	fframe = cv2.GaussianBlur(frame, *gaussblur_params)
	
	diff = cv2.absdiff(ref, frame)
	diff2 = accentuate(diff * 255)
	# diff = cv2.medianBlur(diff, 5)
	# diff = cv2.medianBlur(diff, 5)
	
	fdiff = cv2.absdiff(fref, fframe)
	
	# ddiff = diff
	# ddiff = cv2.dilate(ddiff, dilate)
	# ddiff = cv2.dilate(ddiff, dilate)
	
	# Affichage
	# cv2.imshow('complexe', cam.stream)
	cv2.imshow('reference', cam.reference)
	cv2.imshow('source', cam.frame)
	
	cv2.imshow('ref', ref)
	cv2.imshow('frame', frame)
	cv2.imshow('diff', diff)
	cv2.imshow('diff2', diff2)
	# cv2.imshow('ddiff', ddiff)
	# cv2.imshow('fdiff', fdiff)
	
	# Input management
	if Camera.keyEvents(): break
### END WHILE

# On ferme tout
Camera.closeCamApp()