from WolfEye.lib.camera import *
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
# test.setBlurSize(3)
cam1.setFOV(horizontal=math.radians(92.0))
cam2.setFOV(horizontal=math.radians(92.0))

a, b = 17, 240

while 1:
	cam1.getFrame()
	cam2.getFrame()
	
	# r = cam1.detectByColor(hueLowMax=a, hueHighMin=b, blur=True)
	# cam2.detectByColor(hueLowMax=a, hueHighMin=b, blur=True)
	
	r = cam1.detectByRef(seuil=150)
	cam2.detectByRef(seuil=150)
	
	# r = cam1.detectHybrid()
	# cam2.detectHybrid()
	
	cam1.skywalker(offshore=5, minSize=15)
	cam2.skywalker(offshore=5, minSize=15)
	
	finger = cam1 % cam2
	# if finger: print finger
	
	cv2.imshow('cam1', cam1.frame)
	cv2.imshow('cam1s', cam1.scan)
	cv2.imshow('cam2', cam2.frame)
	cv2.imshow('cam2s', cam2.scan)
	for k, v in r.iteritems(): cv2.imshow(k, v)
	
	# Input management
	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break
		
	elif sKey == ord(' '):
		print
		cam1.calibrate(True)
		cam2.calibrate(True)
		print
	
	elif sKey == ord('r'):
		cam1.setReference()
		cam2.setReference()
	
	elif sKey == ord('a'):
		print
		print math.degrees(cam1.fingerAbsoluteAngle)
		# print cam2.fingerAbsoluteAngle
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