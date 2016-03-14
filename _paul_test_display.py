# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (1280, 720)
W, H = (640, 480)

# Création de la caméra
cam = Camera()
cam.init(0, width=W, height=H, exposure=-4)
cam.setFOV(horizontal=math.radians(92.0))
cam.setImageVertBand(0.45, 0.5)
# cam.setImageVertBand(0, 0.5)
cam.setAnoisek(radius=3)
# cam.autoExposure()

# Display fullscreen window
p = FullscreenCanvas(bg='#FFFFFF')
canvas = p.canvas
root = p.window

@staticmethod
def myEvents(k, cam):
	if k == 'q': return True # Stop
		
	elif k == 'o':
		cam.space.o = cam.finger.x
			
	elif k == 'i':
		cam.space.i = cam.finger.x
	
	elif k == 'j':
		cam.space.j = cam.finger.x
		
	elif k == ' ':
		cam.setReference(count=10)
		
	elif k == 'c':
		winsize = mouse.SCREEN
		cam.calibrate(True, w=winsize.x, h=winsize.y)
		
	elif k == '.':
		cam.Export('cam')
	
	elif k == '0':
		cam.Import('cam')
Camera.keyManagement = myEvents

print 'looping...'
cam.setReference(count=10)
while 1:
	# On filme
	cam.getFrame()
	
	p = cam.detectByRef(seuil=80)
	cam.anoise(50)
	cam.arounder(
		maxCount=1000,
		minArea=200,
		maxDist=1,
		thick=1
	)
	
	if cam.finger: print cam.fingerAbsoluteAngle
	
	# Affichage sur l'image de scan les points
	cam.drawSpace()
	
	canvas.delete("all")
	canvas.create_line(*(~(mouse.SCREEN/2.0) + ~cam.position), tags="pos");
	
	a = cam.fingerAbsoluteAngle
	if a:
		u = D2Point.createUnit(a)
		canvas.create_line(*(~cam.position + ~(cam.position + u * 10000)), tags='dir', fill='red')
	
	# Affichage
	# cv2.imshow('reference', cam.reference)
	cv2.imshow('complexe', cam.stream)
	# cv2.imshow('source', cam.frame)
	cv2.imshow('diff', p.AbsDiff)
	
	# Input management
	if Camera.keyEvents(): break
### END WHILE

# On ferme tout
Camera.closeCamApp()
root.destroy()