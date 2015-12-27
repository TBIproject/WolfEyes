# -*- coding: utf-8 -*-
from WolfEyes.work import *

width, height = (1280, 720)
width, height = (640, 480)

# Création de la caméra
cam = Camera()
cam.init(0, width=width, height=height, exposure=-10)
cam.setFOV(horizontal=math.radians(92.0))
# cam.setImageVertBand(0.45, 0.5)
cam.setImageVertBand(0, 0.5)

mouse.SMOOTH = 5

print 'looping...'
cam.setReference(count=10)
while 1:
	# On filme
	cam.getFrame()
	
	# Isolement
	r = cam.detectByRef(seuil=100)
	
	# Amélioration:
	cam.fgMagic()
	
	# Détection
	k = cam.arounder(
		maxCount=1000,
		minArea=16,
		maxDist=10,
		thick=1
	)
	
	# On bouge la souris si le doigt est détecté
	if cam.finger:
		finger = cam.finger
		finger.x = 1 - finger.x
		
		cursor = finger * mouse.SCREEN
		mouse.move(*~cursor)
		
		if cam.clic: printf('click\r')
	
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