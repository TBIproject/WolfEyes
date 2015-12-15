# -*- coding: utf-8 -*-
from WolfEyes.lib.camera import *
import numpy as np
import time
import cv2

width, height = (640, 480)

# Création de la caméra
cam = Camera()
cam.init(0, width=width, height=height, exposure=-5)
cam.setFOV(horizontal=math.radians(92.0))
# cam.setImageVertBand(0.45, 0.5)
cam.setImageVertBand(0.3, 0.6)

def bouger_souris(x, y):
	# TODO
	print (x, y)
###

print 'looping...'
while 1:
	# On filme
	cam.getFrame()
	
	# Isolement
	r = cam.detectByRef(seuil=150)
	
	# Colonnage
	# cam.saber()
	
	# Détection
	cam.skywalker(offshore=3, minSize=10)
	
	# On bouge la souris si le doigt est détecté
	# if cam.finger: bouger_souris(cam.finger.x, 0)
	print cam.finger
	
	# Affichage
	cv2.imshow('source', cam.frame)
	cv2.imshow('reference', cam.reference)
	# for name, img in r.iteritems(): cv2.imshow('src1%s'%name, img)
	cv2.imshow('scan', cam.scan)
	
	# Input management
	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break # On quitte
		
	elif sKey == ord(' '):
		cam.setReference(count=10)
### END WHILE

# On ferme tout
Camera.closeCamApp()