# -*- coding: utf-8 -*-
from WolfEyes.work import *

width, height = (1280, 720)
width, height = (640, 480)

# Création de la caméra
cam = Camera()
cam.init(0, width=width, height=height)
cam.setFOV(horizontal=math.radians(92.0))
# cam.setImageVertBand(0.45, 0.5)
cam.setImageVertBand(0, 0.5)

cam.setAnoisek(radius=3)

mouse.SMOOTH = 5

print 'looping...'
cam.setReference(count=10)
while 1:
	# On filme
	cam.getFrame()
	
	# Isolement
	r = cam.detectByRef(seuil=30)
	
	# Test du anoise
	cam.anoise(150, 150)
	
	"""
	kernel = np.array([
		[0, 0.5, 1, 0.5, 0],
		[0.5, 1, 1, 1, 0.5],
		[1, 1, 0, 1, 1],
		[0.5, 1, 1, 1, 0.5],
		[0, 0.5, 1, 0.5, 0]
	], np.float32)
	kernel /= kernel.sum()
	
	test = ((cv2.filter2D(cam.binary, -1, kernel) > 255/3.0) * 255).astype(np.uint8)
	# """
	
	# Amélioration:
	# cam.fgMagic()
	
	# Détection
	k = cam.arounder(
		maxCount=1000,
		minArea=36,
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
	
	# Affichage sur l'image de scan les points
	cam.drawSpace()
	
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
	
	elif sKey == ord('o'):
		cam.space.o = cam.finger.x
		
	elif sKey == ord('i'):
		cam.space.i = cam.finger.x
	
	elif sKey == ord('j'):
		cam.space.j = cam.finger.x
### END WHILE

# On ferme tout
Camera.closeCamApp()