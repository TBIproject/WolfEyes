# -*- coding: utf-8 -*-
from WolfEyes.work import *

width, height = (1280, 720)

# Création de la caméra
cam = Camera()
cam.init(0, width=1280, height=720, exposure=-5)
cam.setFOV(horizontal=math.radians(92.0))
cam.setImageVertBand(0.45, 0.5)

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
	
	# Paramétrage
	cam.setBloberUp(
		Convexity=True,
		maxConvexity=0.8
	)
	
	# Détection
	# cam.skywalker(offshore=3, minSize=10)
	k = cam.blober()
	
	# On bouge la souris si le doigt est détecté
	# if cam.finger: bouger_souris(cam.finger.x, 0)
	
	# Affichage
	cv2.imshow('source', cam.frame)
	cv2.imshow('reference', cam.reference)
	for name, img in k.iteritems(): cv2.imshow('src1%s'%name, img)
	cv2.imshow('scan', cam.scan)
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