# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (1280, 720)
W, H = (640, 480)
exp = -4

# Création de la caméra 1
cam1 = Camera()
cam1.PYON.gamma = 0.1
cam1.init(0, width=W, height=H)
cam1.setFOV(horizontal=math.radians(92.0))
cam1.setImageVertBand(0.40, 0.50)
cam1.autoExposure()
cam1.setReferenceSP()

# Création de la caméra 2
cam2 = Camera()
cam2.PYON.gamma = 0.1
cam2.init(1, width=W, height=H)
cam2.setFOV(horizontal=math.radians(92.0))
cam2.setImageVertBand(0.40, 0.50)
cam2.autoExposure()
cam2.setReferenceSP()

cam1.PYON.thresh = 10
cam1.PYON.spread = 10
cam1.PYON.deriv_diff_thresh = 0.03
cam1.PYON.blockSize = pyon(width = 5, height = 5)

cam2.PYON.thresh = 10
cam2.PYON.spread = 10
cam2.PYON.deriv_diff_thresh = 0.03
cam2.PYON.blockSize = pyon(width = 5, height = 5)

mouse.SMOOTH = 2

print 'looping...'

while 1:
	Camera.AsyncProcess(func=cam1.st, cams=[cam1, cam2])
	
	# Affichage sur l'image de scan les points
	cam1.drawSpace()
	cam2.drawSpace()
	
	click, mpos = cam1 % cam2
	if mpos is not None:
		mpos.y = mouse.SCREEN.y - mpos.y
		
		mouse.move(*~mpos)
		
		if click: printf('click\r')
	
	# Affichage
	cv2.imshow('cam1', cam1.stream)
	cv2.imshow('cam2', cam2.stream)

	try:# Input management
		sKey = Camera.waitKey()
		if sKey == ord('q'):
			break # On quitte
			
		elif sKey == ord('.'):
			cam1.Export('cam1')
			cam2.Export('cam2')
			
		elif sKey == ord('0'):
			cam1.Import('cam1')
			cam2.Import('cam2')
			
		elif sKey == ord(' '):
			cam1.setReferenceSP()
			cam2.setReferenceSP()
		
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
			cam1.calibrate(True, h=mouse.SCREEN.y, w=mouse.SCREEN.x)
			cam2.calibrate(True, h=mouse.SCREEN.y, w=mouse.SCREEN.x)
			
	# Oops
	except Exception as e: print e
	
### END WHILE

# On ferme tout
Camera.closeCamApp()