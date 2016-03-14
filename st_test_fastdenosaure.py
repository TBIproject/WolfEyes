# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (1280, 720)
W, H = (640, 480)
exp = -4

# Création de la caméra 1
cam = Camera()
cam.init(0, width=W, height=H)
cam.setFOV(horizontal=math.radians(92.0))
cam.setImageVertBand(0.40, 0.50)
cam.autoExposure()

tolerance = 20

bufferSize = 9
buffer = []

for i in xrange(bufferSize):
	cam.getFrame()
	buffer.append(cam.frame)
	# buffer.append(cv2.cvtColor(cam.frame, cv2.COLOR_BGR2GRAY))
	
corrected_ref = cv2.fastNlMeansDenoisingColoredMulti(buffer, bufferSize - 1, 1, searchWindowSize = 9, h = 20)
# corrected_ref = cv2.fastNlMeansDenoisingMulti(buffer, bufferSize - 1, 1, searchWindowSize = 15, h = 20)
	
print 'looping...'

while 1:
	
	corrected_frame = cv2.fastNlMeansDenoisingColoredMulti(buffer, bufferSize - 1, 1, searchWindowSize = 9, h = 20)
	# corrected_frame = cv2.fastNlMeansDenoisingMulti(buffer, bufferSize - 1, 1, searchWindowSize = 15, h = 20)
	
	diff = cv2.absdiff(corrected_ref, corrected_frame)
	diff = cv2.cvtColor(diff.max(axis=2), cv2.COLOR_GRAY2BGR)
	diff = ((diff > 20) * 255).astype(np.uint8)
	
	# Affichage
	
	cv2.imshow('cam.frame', cam.frame)
	cv2.imshow('corrected_frame', corrected_frame)
	cv2.imshow('diff', diff)
	
	for i in xrange(bufferSize-1):
		buffer[i] = buffer[i+1]
	
	cam.getFrame()
	buffer[bufferSize-1] = cam.frame

	sKey = Camera.waitKey()
	if sKey == ord('q'):
		break # On quitte
	
### END WHILE

# On ferme tout
Camera.closeCamApp()