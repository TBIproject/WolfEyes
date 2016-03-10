# -*- coding: utf-8 -*-
from WolfEyes.work import *

W, H = (1280, 720)
W, H = (640, 480)

# Création de la caméra
cam = Camera()
cam.init(0, width=W, height=H)
cam.setFOV(horizontal=math.radians(92.0))
cam.setImageVertBand(0.45, 0.5)
# cam.setImageVertBand(0, 0.5)
cam.setAnoisek(radius=3)
cam.autoExposure()

# Display fullscreen window
p = FullscreenCanvas(bg='#FFFFFF')
canvas = p.canvas
root = p.window

print 'looping...'
cam.setReference(count=10)
while 1:
	# On filme
	cam.getFrame()
	canvas.delete("all")
	
	# Isolement
	r = cam.detectByRefAdv(
		seuil=100,
		coef=0
	)
	
	# Test du anoise
	cam.anoise(50)
	
	# Détection
	cam.arounder(
		maxCount=1000,
		minArea=36,
		maxDist=10,
		thick=1
	)
	
	# Affichage sur l'image de scan les points
	cam.drawSpace()
	
	canvas.create_line(*(~cam.position + ~(mouse.SCREEN/2.0)), tags="pos")
	
	a = cam.fingerAbsoluteAngle
	if a:
		u = D2Point.createUnit()
		print u
		canvas.create_line(*(~cam.position + ~(u * 10000)), tags='dir')
	
	# Affichage
	cv2.imshow('reference', cam.reference)
	cv2.imshow('complexe', cam.stream)
	cv2.imshow('source', cam.frame)
	
	# Input management
	if Camera.keyEvents(): break
### END WHILE

# On ferme tout
Camera.closeCamApp()
root.destroy()