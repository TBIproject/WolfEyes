from WolfEyes.lib.camera import *
import WolfEye.MouseControl as mouse
import math
import time
import cv2

cam1 = Camera()
cam1.init(0, exposure=-5, width=1920, height=1080)
cam1.setBlurSize(3)

cam2 = Camera()
cam2.init(1, exposure=-5, width=1920, height=1080)
cam2.setBlurSize(3)

cam1.setImageVertBand(0.45, 0.5)
cam2.setImageVertBand(0.45, 0.5)
cam1.setFOV(horizontal=math.radians(92.0))
cam2.setFOV(horizontal=math.radians(92.0))

REF_COUNT = 8

CONTROL = False

while 1:
	cam1.getFrame()
	cam2.getFrame()
	
	r = cam1.detectByRef(seuil=150)
	cam2.detectByRef(seuil=150)
	
	cam1.skywalker(offshore=5, minSize=15)
	cam2.skywalker(offshore=5, minSize=15)
	
	click, finger = cam1 % cam2
	if finger: print finger
	if click: mouse.click(*finger.pos, click)
	
	cv2.imshow('cam1', cam1.frame)
	cv2.imshow('cam1s', cam1.scan)
	cv2.imshow('cam2', cam2.frame)
	cv2.imshow('cam2s', cam2.scan)
	# for k, v in r.iteritems(): cv2.imshow(k, v)
	
	# Input management
	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break
		
	elif sKey == ord(' '):
		print
		cam1.calibrate(True)
		cam2.calibrate(True)
		print
	
	elif sKey == ord('c'):
		print
		CONTROL = not CONTROL
		print 'CONTROL is %s' % CONTROL
		print
	
	elif sKey == ord('r'):
		cam1.setReference(count=REF_COUNT)
		cam2.setReference(count=REF_COUNT)
	
	elif sKey == ord('a'):
		print
		print (math.degrees(cam1.fingerAbsoluteAngle), math.degrees(cam2.fingerAbsoluteAngle))
		print
		
	elif sKey == ord('o'):
		print 'o'
		cam1.space.o = cam1.finger.x
		cam2.space.o = cam2.finger.x
	
	elif sKey == ord('i'):
		print 'i'
		cam1.space.i = cam1.finger.x
		cam2.space.i = cam2.finger.x
	
	elif sKey == ord('j'):
		print 'j'
		cam1.space.j = cam1.finger.x
		cam2.space.j = cam2.finger.x

Camera.closeCamApp()