# -*- coding: utf-8 -*-
from WolfEyes.lib.camera import *
import numpy as np
import time
import cv2

width, height = (1280, 720)
width, height = (640, 480)

# Création de la caméra
cam = Camera()
cam.init(0, width=width, height=height, exposure=-5)
cam.setFOV(horizontal=math.radians(92.0))
# cam.setImageVertBand(0.45, 0.5)

print 'looping...'
while 1:
	# On filme
	cam.getFrame()
	
	# Isolement
	r = cam.detectByRef(seuil=100)
	
	# Détection
	k = {}
	try:
		k = cam.arounder(
			maxCount=1000,
			minArea=50,
			maxDist=100,
			thick=1
		)
	except: print 'zblah'
	
	# On bouge la souris si le doigt est détecté
	# if cam.finger: bouger_souris(cam.finger.x, 0)
	
	# Affichage
	cv2.imshow('source', cam.frame)
	cv2.imshow('reference', cam.reference)
	for name, img in k.iteritems(): cv2.imshow('src1%s'%name, img)
	cv2.imshow('bin', cam.binary)
	
	# Input management
	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break # On quitte
		
	elif sKey == ord(' '):
		cam.setReference(count=10)
### END WHILE

# On ferme tout
Camera.closeCamApp()