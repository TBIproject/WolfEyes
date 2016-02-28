# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (1280, 720)
W, H = (640, 480)

lk_params = dict( winSize  = (15, 15), 
                  maxLevel = 2, 
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))   

feature_params = dict( maxCorners = 100, 
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7)

# Création de la caméra
cam = Camera()
cam.init(0, width=W, height=H, exposure=-4)
cam.setFOV(horizontal=math.radians(92.0))

cam.getFrame()
prev_gray = cv2.cvtColor(cam.frame, cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(cam.frame)
hsv[...,1] = 255

print 'looping...'

while 1:
	cam.getFrame()
	next_gray = cv2.cvtColor(cam.frame, cv2.COLOR_BGR2GRAY)

	flow = cv2.calcOpticalFlowFarneback(prev_gray, next_gray, None, 0.5, 3, 15, 1, 5, 1.2, 0)

	mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])

	hsv[...,0] = ang*180/np.pi/2
	hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
	rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

	cv2.imshow('frame2',rgb)

	# Input management
	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break # On quitte
		
	elif sKey == ord(' '):
		cam.setReference(count=10)
		
	prev_gray = next_gray
	
### END WHILE

# On ferme tout
Camera.closeCamApp()