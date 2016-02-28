# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (1280, 720)
W, H = (640, 480)

lk_params = dict( winSize  = (10, 10), 
                  maxLevel = 5, 
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))   

feature_params = dict( maxCorners = 3000, 
                       qualityLevel = 0.5,
                       minDistance = 3,
                       blockSize = 3)

# Création de la caméra
cam = Camera()
cam.init(0, width=W, height=H, exposure=-4)
cam.setFOV(horizontal=math.radians(92.0))
				  
cam.getFrame()
old_gray = cv2.cvtColor(cam.frame, cv2.COLOR_BGR2GRAY)
old_points = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

print 'looping...'

while 1:

	cam.getFrame()
	curr_gray = cv2.cvtColor(cam.frame, cv2.COLOR_BGR2GRAY)
	curr_points, stat, err = cv2.calcOpticalFlowPyrLK(old_gray, curr_gray, old_points, None, **lk_params)
	
	old_good_points = old_points[stat==1]
	curr_good_points = curr_points[stat==1]

	for old_point, curr_point in zip(old_good_points, curr_good_points):
		old_point = (int(old_point[0]),int(old_point[1]))
		cv2.circle(cam.frame, old_point, 15, (0,0,255), 2)
		curr_point = (int(curr_point[0]),int(curr_point[1]))
		cv2.circle(cam.frame, curr_point, 15, (0,255,0), 2)
		cv2.line(cam.frame, old_point, curr_point, (255,0,0), 2)
	
	# Affichage
	cv2.imshow('source', cam.frame)
	
	# Input management
	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break # On quitte
		
	elif sKey == ord(' '):
		cam.setReference(count=10)
		
	old_gray = curr_gray.copy()
	old_points = curr_points
	
### END WHILE

# On ferme tout
Camera.closeCamApp()