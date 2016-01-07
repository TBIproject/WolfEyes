# -*- coding: utf-8 -*-
from WolfEyes.work import *

# Format
width, height = (640, 480)

# Création des caméras

cam1 = Camera()
cam1.init(0, width=width, height=height)
cam1.setFOV(horizontal=math.radians(92.0))
cam1.setImageVertBand(0.46, 0.51)
cam1.setAnoisek(radius=3)

cam2 = Camera() # miss scotch
cam2.init(1, width=width, height=height)
cam2.setFOV(horizontal=math.radians(92.0))
cam2.setImageVertBand(0.46, 0.51)
cam2.setAnoisek(radius=3)

# Parametre e deplacement de la souris
mouse.SMOOTH = 5

# Bords de l'image
BORDERS = pyon()
COEFS = pyon()

# Start
print 'looping...'
# cam1.setReference(count=10)
# cam2.setReference(count=10)
while 1:
	# On filme
	cam1.getFrame()
	cam2.getFrame()
	
	# Isolement
	# r = cam.detectByRef(seuil=30)
	
	# Amélioration:
	cam1.fgMagic()
	cam2.fgMagic()
	
	# Test du anoise
	cam1.anoise(100)
	cam2.anoise(100)
	
	# Détection
	cam1.arounder(
		maxCount=1000,
		minArea=36,
		maxDist=10,
		thick=1
	)
	
	cam2.arounder(
		maxCount=1000,
		minArea=36,
		maxDist=10,
		thick=1
	)
	
	# On bouge la souris si le doigt est détecté
	click, mpos = cam1 % cam2
	if mpos:
		mpos.y = 1 - mpos.y
		
		if COEFS.by:
			mpos.x = COEFS.ax * mpos.x + COEFS.bx
			mpos.y = COEFS.ay * mpos.y + COEFS.by
		
		cursor = mpos * mouse.SCREEN
		printf('cursor: %s\r' % cursor)
		mouse.move(*~cursor)
		
		if click:
			printf('click\r')
	
	# Affichage sur l'image de scan les points
	cam1.drawSpace()
	cam2.drawSpace()
	
	# Affichage complexe
	stream1 = np.bitwise_or(np.bitwise_and((np.logical_not(cam1.scan) * 255).astype(np.uint8), cam1.frame), cam1.scan)
	stream2 = np.bitwise_or(np.bitwise_and((np.logical_not(cam2.scan) * 255).astype(np.uint8), cam2.frame), cam2.scan)
	
	# Affichage
	cv2.imshow('stream1', stream1)
	cv2.imshow('stream2', stream2)
	
	try:# Input management
		sKey = Camera.waitKey()
		if sKey == ord('q'):
			break # On quitte
			
		elif sKey == ord(' '):
			cam1.setReference(count=10)
			cam2.setReference(count=10)
		
		elif sKey == ord('o'):
			cam1.space.o = cam1.finger.x
			cam2.space.o = cam2.finger.x
			
		elif sKey == ord('i'):
			cam1.space.i = cam1.finger.x
			cam2.space.i = cam2.finger.x
		
		elif sKey == ord('j'):
			cam1.space.j = cam1.finger.x
			cam2.space.j = cam2.finger.x
		
		elif sKey == ord('c'):
			cam1.calibrate(True)
			cam2.calibrate(True)
		
		elif sKey == ord('4'): BORDERS.left = mpos.x
		elif sKey == ord('6'): BORDERS.right = mpos.x
		
		elif sKey == ord('8'): BORDERS.top = mpos.y
		elif sKey == ord('2'): BORDERS.bottom = mpos.y
		
		elif sKey == ord('b'):
			print BORDERS
			COEFS.ax = 1.0 / (BORDERS.right - BORDERS.left)
			COEFS.bx = -BORDERS.left
			COEFS.ay = 1.0 / (BORDERS.top - BORDERS.bottom)
			COEFS.by = -BORDERS.bottom
		
		elif sKey == ord('n'): COEFS = pyon()
			
	# Oops
	except Exception as e: print e
### END WHILE

# On ferme tout
Camera.closeCamApp()