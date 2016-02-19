# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (1280, 720)
W, H = (640, 480)

# Création de la caméra
cam = Camera()
cam.init(0, width=W, height=H, exposure=-6)

hand_cascade = cv2.CascadeClassifier('hands.xml')

print 'looping...'
cam.setReference(count=10)
while 1:
	# On filme
	cam.getFrame()
	gray = cv2.cvtColor(cam.frame, cv2.COLOR_BGR2GRAY)
	
	hand = hand_cascade.detectMultiScale(gray, 1.3, 3)
	
	for (x,y,w,h) in hand:
		cv2.rectangle(cam.frame,(x,y),(x+w,y+h),(0,255,0),2)
	
	cv2.imshow('source', cam.frame)
	
	# Input management
	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break # On quitte
		
	elif sKey == ord(' '):
		cam.setReference(count=10)
### END WHILE

# On ferme tout
Camera.closeCamApp()