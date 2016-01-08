# -*- coding: utf-8 -*-
from WolfEyes.work import *

# Format
width, height = (640, 480)

# Création des caméras

cam1 = Camera()
cam1.init(0, width=width, height=height)
cam1.setFOV(horizontal=math.radians(92.0))
cam1.setImageVertBand(0.44, 0.49)
cam1.setAnoisek(radius=3)

cam2 = Camera() # miss scotch
cam2.init(1, width=width, height=height)
cam2.setFOV(horizontal=math.radians(92.0))
cam2.setImageVertBand(0.44, 0.49)
cam2.setAnoisek(radius=3)

# Parametre de deplacement de la souris
mouse.SMOOTH = 5

# Bords de l'image
BORDERS = pyon()
COEFS = pyon()

# Image processing function
def process(cam):

	# Isolement
	cam.detectByRef(seuil=50)
	
	# Amélioration:
	cam.fgMagic()
	
	# Test du anoise
	cam.anoise(150, 150)
	
	# Détection
	cam.arounder(
		maxCount=1000,
		minArea=36,
		maxDist=10,
		thick=1
	)
	
### END

# Start
print 'looping...'
cam1.setReference(count=10)
cam2.setReference(count=10)
while 1:
	# On filme
	cam1.getFrame()
	cam2.getFrame()
	
	# Traitement
	Camera.asyncProcess(func=process)
	
	# On bouge la souris si le doigt est détecté
	click, mpos = cam1 % cam2
	if mpos:
		mpos.y = 1 - mpos.y
		
		if COEFS.ok:
			mpos.x = COEFS.ax * mpos.x + COEFS.bx
			mpos.y = COEFS.ay * mpos.y + COEFS.by
		
		cursor = mpos * mouse.SCREEN
		printf('cursor: %s\r' % str(~cursor))
		mouse.move(*~cursor)
		
		if click:
			printf('click\r')
	
	# Affichage sur l'image de scan les points
	cam1.drawSpace()
	cam2.drawSpace()
	
	# Affichage
	cv2.imshow('stream1', cam1.stream)
	cv2.imshow('stream2', cam2.stream)
	
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
		
		elif sKey == ord('5'): print BORDERS
		
		elif sKey == ord('b'):
			print BORDERS
			COEFS.ax = 1.0 / (BORDERS.right - BORDERS.left)
			COEFS.bx = -BORDERS.left
			COEFS.ay = 1.0 / (BORDERS.top - BORDERS.bottom)
			COEFS.by = -BORDERS.bottom
			COEFS.ok = True
			print COEFS
		
		elif sKey == ord('n'): COEFS = pyon()
			
	# Oops
	except Exception as e: print e
### END WHILE

# On ferme tout
Camera.closeCamApp()