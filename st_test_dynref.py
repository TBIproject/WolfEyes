# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (1280, 720)
W, H = (640, 480)

# Création de la caméra
cam = Camera()
cam.init(0, width=W, height=H, exposure=-6)
cam.setFOV(horizontal=math.radians(92.0))

print 'looping...'

cam.getFrame()
cumulative = cam.frame

cam.setReference(count=10)
bgref = cam.reference

while 1:
	# On filme
	cam.getFrame()
	
	cumulative = cumulative / 1.5 + cam.frame / 2.5
	#result = cv2.absdiff(cumulative, bgref)
	#result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
	#result = ((result > 20) * 255).astype(np.uint8)
	
	# Affichage
	cv2.imshow('source', cumulative)
	
	# Input management
	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break # On quitte
		
	elif sKey == ord(' '):
		cam.setReference(count=10)
### END WHILE

# On ferme tout
Camera.closeCamApp()