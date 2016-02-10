# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (640, 240)

# Création de la caméra
cam = Camera()
cam.init(0, width=W, height=H, exposure=-6)
cam.setFOV(horizontal=math.radians(92.0))
cam.setImageVertBand(0, 0.5)

mouse.SMOOTH = 5

# Pouet
cam.getFrame()

# stats
mean = np.zeros((H, W, 3), np.uint16)
stat = np.zeros((H, W, 3), np.uint8)

print 'looping...'
cam.setReference(count=10)
while 1:
	# On filme
	cam.getFrame()
	frame = cam.frame
	
	#Magic!
	deriv = cf.Scharr(frame)
	# print mean.shape, deriv.shape, frame.shape
	mean += deriv
	
	dmean = mean / float(mean.max())
	
	# Display
	cv2.imshow('source', frame)
	cv2.imshow('deriv', deriv)
	
	# Input management
	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break # On quitte
		
	elif sKey == ord(' '):
		cam.setReference(count=10)
### END WHILE

# On ferme tout
Camera.closeCamApp()